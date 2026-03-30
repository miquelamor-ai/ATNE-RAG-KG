"""
eval_db.py — Gestió de la base de dades SQLite per a resultats d'avaluació A/B.

Emmagatzema els resultats de l'experiment comparatiu (Hardcoded vs RAG)
amb tres taules: runs, casos individuals per branca, i comparacions.

Ús com a mòdul:
    from eval_db import init_db, create_run, insert_case, ...

Ús standalone (crea la BD buida):
    python eval_db.py
"""

import json
import sqlite3
import time
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓ
# ═══════════════════════════════════════════════════════════════════════════════

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "tests" / "results" / "evaluations.db"

# ═══════════════════════════════════════════════════════════════════════════════
# ESQUEMA
# ═══════════════════════════════════════════════════════════════════════════════

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS eval_runs (
    run_id              TEXT PRIMARY KEY,
    timestamp           TEXT NOT NULL,
    branch_a            TEXT NOT NULL DEFAULT 'hardcoded',
    branch_b            TEXT NOT NULL DEFAULT 'rag',
    total_cases         INTEGER NOT NULL DEFAULT 0,
    notes               TEXT
);

CREATE TABLE IF NOT EXISTS eval_cases (
    id                          INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id                      TEXT NOT NULL,
    cas_id                      TEXT NOT NULL,
    branca                      TEXT NOT NULL,
    text_id                     TEXT,
    perfil_id                   TEXT,
    etapa                       TEXT,
    genere                      TEXT,
    mecr                        TEXT,
    dua                         TEXT,
    perfils_actius              TEXT,
    -- Retrieval
    recall                      REAL,
    instruccions_absents        TEXT,
    -- Forma
    f1_longitud_frase           REAL,
    f2_titols                   INTEGER,
    f3_negretes                 INTEGER,
    f4_llistes                  INTEGER,
    f5_prellico                 INTEGER,
    puntuacio_forma             REAL,
    -- Fons (LLM judge)
    c1_coherencia               INTEGER,
    c1_justificacio             TEXT,
    c2_adequacio_perfil         INTEGER,
    c2_justificacio             TEXT,
    c3_preservacio_curricular   INTEGER,
    c3_justificacio             TEXT,
    c4_adequacio_mecr           INTEGER,
    c4_justificacio             TEXT,
    c5_prellico_funcional       INTEGER,
    c5_justificacio             TEXT,
    c6_coherencia_creuament     INTEGER,
    c6_justificacio             TEXT,
    puntuacio_fons              REAL,
    -- Filter stats
    total_instruccions_enviades INTEGER,
    instruccions_sempre         INTEGER,
    instruccions_nivell         INTEGER,
    instruccions_perfil         INTEGER,
    instruccions_condicional    INTEGER,
    instruccions_suprimides     INTEGER,
    -- Prompt and output
    system_prompt_length        INTEGER,
    system_prompt               TEXT,
    text_adaptat_length         INTEGER,
    text_adaptat                TEXT,
    temps_generacio             REAL,

    FOREIGN KEY (run_id) REFERENCES eval_runs(run_id)
);

CREATE TABLE IF NOT EXISTS eval_comparisons (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id              TEXT NOT NULL,
    cas_id              TEXT NOT NULL,
    text_id             TEXT,
    perfil_id           TEXT,
    millor_forma        TEXT,
    motiu_forma         TEXT,
    millor_fons         TEXT,
    motiu_fons          TEXT,
    veredicte           TEXT,
    motiu_veredicte     TEXT,
    prompt_hc_coherent  INTEGER,
    prompt_rag_coherent INTEGER,

    FOREIGN KEY (run_id) REFERENCES eval_runs(run_id)
);

CREATE INDEX IF NOT EXISTS idx_cases_run ON eval_cases(run_id);
CREATE INDEX IF NOT EXISTS idx_cases_cas ON eval_cases(cas_id);
CREATE INDEX IF NOT EXISTS idx_cases_branca ON eval_cases(branca);
CREATE INDEX IF NOT EXISTS idx_comparisons_run ON eval_comparisons(run_id);
CREATE INDEX IF NOT EXISTS idx_comparisons_cas ON eval_comparisons(cas_id);
"""


# ═══════════════════════════════════════════════════════════════════════════════
# INICIALITZACIÓ
# ═══════════════════════════════════════════════════════════════════════════════

def init_db(db_path: Path | None = None) -> sqlite3.Connection:
    """
    Inicialitza la base de dades SQLite. Crea les taules si no existeixen.

    Args:
        db_path: ruta al fitxer .db (per defecte tests/results/evaluations.db)

    Returns:
        connexió sqlite3 amb row_factory = sqlite3.Row
    """
    path = db_path or DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(SCHEMA_SQL)
    conn.commit()
    return conn


# ═══════════════════════════════════════════════════════════════════════════════
# RUNS
# ═══════════════════════════════════════════════════════════════════════════════

def create_run(
    conn: sqlite3.Connection,
    notes: str = "",
    branch_a: str = "hardcoded",
    branch_b: str = "rag",
    total_cases: int = 0,
) -> str:
    """
    Crea un nou run d'avaluació amb un ID basat en el timestamp.

    Args:
        conn: connexió a la BD
        notes: comentaris opcionals sobre el run
        branch_a: nom de la primera branca (per defecte 'hardcoded')
        branch_b: nom de la segona branca (per defecte 'rag')
        total_cases: nombre total de casos previstos

    Returns:
        run_id generat (ex: "20260329_153000")
    """
    run_id = time.strftime("%Y%m%d_%H%M%S")
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    conn.execute(
        """INSERT INTO eval_runs (run_id, timestamp, branch_a, branch_b, total_cases, notes)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (run_id, timestamp, branch_a, branch_b, total_cases, notes),
    )
    conn.commit()
    return run_id


def get_all_runs(conn: sqlite3.Connection) -> list[dict]:
    """
    Retorna tots els runs ordenats per timestamp descendent.

    Returns:
        llista de dicts amb les dades de cada run
    """
    rows = conn.execute(
        "SELECT * FROM eval_runs ORDER BY timestamp DESC"
    ).fetchall()
    return [dict(r) for r in rows]


# ═══════════════════════════════════════════════════════════════════════════════
# CASES
# ═══════════════════════════════════════════════════════════════════════════════

# Columnes de la taula eval_cases (sense id, que és autoincrement)
_CASE_COLUMNS = [
    "run_id", "cas_id", "branca", "text_id", "perfil_id",
    "etapa", "genere", "mecr", "dua", "perfils_actius",
    "recall", "instruccions_absents",
    "f1_longitud_frase", "f2_titols", "f3_negretes", "f4_llistes", "f5_prellico",
    "puntuacio_forma",
    "c1_coherencia", "c1_justificacio",
    "c2_adequacio_perfil", "c2_justificacio",
    "c3_preservacio_curricular", "c3_justificacio",
    "c4_adequacio_mecr", "c4_justificacio",
    "c5_prellico_funcional", "c5_justificacio",
    "c6_coherencia_creuament", "c6_justificacio",
    "puntuacio_fons",
    "total_instruccions_enviades", "instruccions_sempre",
    "instruccions_nivell", "instruccions_perfil",
    "instruccions_condicional", "instruccions_suprimides",
    "system_prompt_length", "system_prompt", "text_adaptat_length", "text_adaptat",
    "temps_generacio",
]


def _serialize_json_fields(data: dict) -> dict:
    """
    Serialitza a JSON els camps que contenen llistes o dicts.
    Retorna una còpia del dict amb els valors convertits.
    """
    result = dict(data)
    for key in ("perfils_actius", "instruccions_absents"):
        val = result.get(key)
        if val is not None and not isinstance(val, str):
            result[key] = json.dumps(val, ensure_ascii=False)
    return result


def insert_case(conn: sqlite3.Connection, run_id: str, case_data: dict) -> int:
    """
    Insereix una fila a eval_cases per a un cas individual d'una branca.

    Args:
        conn: connexió a la BD
        run_id: identificador del run
        case_data: dict amb les dades del cas (claus = noms de columna)

    Returns:
        id de la fila inserida
    """
    data = _serialize_json_fields(case_data)
    data["run_id"] = run_id

    cols = [c for c in _CASE_COLUMNS if c in data]
    placeholders = ", ".join(["?"] * len(cols))
    col_names = ", ".join(cols)
    values = [data[c] for c in cols]

    cursor = conn.execute(
        f"INSERT INTO eval_cases ({col_names}) VALUES ({placeholders})",
        values,
    )
    conn.commit()
    return cursor.lastrowid


def get_cases_by_run(conn: sqlite3.Connection, run_id: str) -> list[dict]:
    """
    Retorna tots els casos d'un run determinat.

    Args:
        run_id: identificador del run

    Returns:
        llista de dicts amb les dades de cada cas
    """
    rows = conn.execute(
        "SELECT * FROM eval_cases WHERE run_id = ? ORDER BY cas_id, branca",
        (run_id,),
    ).fetchall()
    results = []
    for r in rows:
        d = dict(r)
        # Deserialitzar camps JSON
        for key in ("perfils_actius", "instruccions_absents"):
            if d.get(key) and isinstance(d[key], str):
                try:
                    d[key] = json.loads(d[key])
                except (json.JSONDecodeError, TypeError):
                    pass
        results.append(d)
    return results


# ═══════════════════════════════════════════════════════════════════════════════
# COMPARISONS
# ═══════════════════════════════════════════════════════════════════════════════

_COMPARISON_COLUMNS = [
    "run_id", "cas_id", "text_id", "perfil_id",
    "millor_forma", "motiu_forma",
    "millor_fons", "motiu_fons",
    "veredicte", "motiu_veredicte",
    "prompt_hc_coherent", "prompt_rag_coherent",
]


def insert_comparison(conn: sqlite3.Connection, run_id: str, comparison_data: dict) -> int:
    """
    Insereix una fila a eval_comparisons per a la comparació d'un cas.

    Args:
        conn: connexió a la BD
        run_id: identificador del run
        comparison_data: dict amb les dades de comparació (claus = noms de columna)

    Returns:
        id de la fila inserida
    """
    data = dict(comparison_data)
    data["run_id"] = run_id

    cols = [c for c in _COMPARISON_COLUMNS if c in data]
    placeholders = ", ".join(["?"] * len(cols))
    col_names = ", ".join(cols)
    values = [data[c] for c in cols]

    cursor = conn.execute(
        f"INSERT INTO eval_comparisons ({col_names}) VALUES ({placeholders})",
        values,
    )
    conn.commit()
    return cursor.lastrowid


def get_comparisons_by_run(conn: sqlite3.Connection, run_id: str) -> list[dict]:
    """
    Retorna totes les comparacions d'un run determinat.

    Args:
        run_id: identificador del run

    Returns:
        llista de dicts amb les dades de cada comparació
    """
    rows = conn.execute(
        "SELECT * FROM eval_comparisons WHERE run_id = ? ORDER BY cas_id",
        (run_id,),
    ).fetchall()
    return [dict(r) for r in rows]


# ═══════════════════════════════════════════════════════════════════════════════
# RESUM I EXPORTACIÓ
# ═══════════════════════════════════════════════════════════════════════════════

def get_run_summary(conn: sqlite3.Connection, run_id: str) -> dict:
    """
    Genera estadístiques agregades d'un run.

    Inclou mitjanes de forma i fons per branca, distribució de veredictes,
    i resum de retrieval recall.

    Args:
        run_id: identificador del run

    Returns:
        dict amb les estadístiques del run
    """
    # Dades del run
    run_row = conn.execute(
        "SELECT * FROM eval_runs WHERE run_id = ?", (run_id,)
    ).fetchone()
    if not run_row:
        return {"error": f"Run {run_id} no trobat"}

    run_info = dict(run_row)

    # Estadístiques per branca
    branches = {}
    for branca in ("hardcoded", "rag"):
        row = conn.execute(
            """SELECT
                COUNT(*) as n,
                AVG(puntuacio_forma) as avg_forma,
                AVG(puntuacio_fons) as avg_fons,
                AVG(recall) as avg_recall,
                AVG(f1_longitud_frase) as avg_f1,
                AVG(f2_titols) as avg_f2,
                AVG(f3_negretes) as avg_f3,
                AVG(f4_llistes) as avg_f4,
                AVG(f5_prellico) as avg_f5,
                AVG(c1_coherencia) as avg_c1,
                AVG(c2_adequacio_perfil) as avg_c2,
                AVG(c3_preservacio_curricular) as avg_c3,
                AVG(c4_adequacio_mecr) as avg_c4,
                AVG(c5_prellico_funcional) as avg_c5,
                AVG(system_prompt_length) as avg_prompt_len,
                AVG(text_adaptat_length) as avg_text_len,
                AVG(temps_generacio) as avg_temps
            FROM eval_cases
            WHERE run_id = ? AND branca = ?""",
            (run_id, branca),
        ).fetchone()
        branches[branca] = dict(row) if row else {}

    # Distribució de veredictes
    veredictes = conn.execute(
        """SELECT veredicte, COUNT(*) as n
           FROM eval_comparisons
           WHERE run_id = ?
           GROUP BY veredicte""",
        (run_id,),
    ).fetchall()
    veredicte_dist = {r["veredicte"]: r["n"] for r in veredictes}

    # Distribució de millor_forma i millor_fons
    forma_dist_rows = conn.execute(
        """SELECT millor_forma, COUNT(*) as n
           FROM eval_comparisons
           WHERE run_id = ?
           GROUP BY millor_forma""",
        (run_id,),
    ).fetchall()
    forma_dist = {r["millor_forma"]: r["n"] for r in forma_dist_rows}

    fons_dist_rows = conn.execute(
        """SELECT millor_fons, COUNT(*) as n
           FROM eval_comparisons
           WHERE run_id = ?
           GROUP BY millor_fons""",
        (run_id,),
    ).fetchall()
    fons_dist = {r["millor_fons"]: r["n"] for r in fons_dist_rows}

    # Coherència dels prompts
    coherence = conn.execute(
        """SELECT
            AVG(prompt_hc_coherent) as hc_coherent_pct,
            AVG(prompt_rag_coherent) as rag_coherent_pct,
            COUNT(*) as n
        FROM eval_comparisons
        WHERE run_id = ?""",
        (run_id,),
    ).fetchone()

    return {
        "run": run_info,
        "branches": branches,
        "veredictes": veredicte_dist,
        "millor_forma": forma_dist,
        "millor_fons": fons_dist,
        "coherencia_prompts": dict(coherence) if coherence else {},
    }


def export_run_json(conn: sqlite3.Connection, run_id: str) -> dict:
    """
    Exporta totes les dades d'un run en un sol dict (per a visualització o arxiu).

    Inclou: informació del run, tots els casos, totes les comparacions i el resum.

    Args:
        run_id: identificador del run

    Returns:
        dict complet amb totes les dades del run
    """
    summary = get_run_summary(conn, run_id)
    if "error" in summary:
        return summary

    cases = get_cases_by_run(conn, run_id)
    comparisons = get_comparisons_by_run(conn, run_id)

    return {
        "run_id": run_id,
        "summary": summary,
        "cases": cases,
        "comparisons": comparisons,
        "export_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# STANDALONE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"Inicialitzant base de dades: {DB_PATH}")
    conn = init_db()
    print("Taules creades correctament.")

    # Mostrar info
    tables = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ).fetchall()
    print(f"Taules: {', '.join(r['name'] for r in tables)}")

    runs = get_all_runs(conn)
    if runs:
        print(f"Runs existents: {len(runs)}")
        for r in runs:
            print(f"  - {r['run_id']} ({r['total_cases']} casos) {r.get('notes', '')}")
    else:
        print("Cap run registrat encara.")

    conn.close()
    print("Fet.")
