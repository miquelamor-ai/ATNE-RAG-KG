"""Pilot v2 — validar rubrica_glossari_v2.json (opció E: Auto + post-edició).

Diferència clau amb v1: SENSE case_overrides amb llistes finites. La rúbrica
nova confia que el LLM seleccioni només termes CALP/tècnics/poc freqüents
(més BICS amb L1 si nouvingut). La vàlvula humana queda al Pas 3.

Hipòtesi a validar:
  - Cas titella (A1 1r primària, sense L1): el LLM no ha d'incloure "mitja, botons,
    agulla, fil" si la rúbrica diu "només tècnic/CALP/poc freqüent". Esperat:
    fallback o ≤2 termes tècnics reals (titella, farciment-borderline).
  - Cas fotosintesi (A2 ESO 1r, L1=àrab): taula amb 3 o 4 columnes (L1+translit
    si àrab activa transliteració). Esperat: termes tècnics + cols extra.
  - Cas democracia (B1 ESO 4t, sense L1): taula 2 cols normal. Esperat: termes
    polítics + 10-12 entries.

Variants:
  Bv2 · GPT-4o + JSON v2 (sense case_overrides)
  Cv2 · Gemma 4 + JSON v2

Ús:
  python tests/pilot_glossari_2026_05_31/pilot_v2.py
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

try:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env")
except ImportError:
    pass

from adaptation.llm_clients import _call_llm
from adaptation.post_process import clean_gemini_output, _post_process_llm_output

PILOT_DIR = Path(__file__).resolve().parent
RUBRICA_V2_PATH = PILOT_DIR / "rubrica_glossari_v2.json"

# Reaprofito els 3 casos del pilot.py
CASES = {
    "titella": {
        "profile": {"caracteristiques": {"dislexia": {"actiu": True, "grau": "moderat"}}},
        "context": {"etapa": "Primària", "materia": "manualitats", "curs": "1r"},
        "mecr": "A1",
        "adapted": """# Com fer un titella de mitja

Necessites:
- Una mitja vella
- Dos botons
- Una agulla i fil
- Una mica de farciment

Passos:
1. Posa el farciment dins de la mitja.
2. Lliga el cap amb un fil.
3. Cus dos botons per fer els ulls.
4. Dibuixa la boca amb un retolador.

Ja tens el teu titella.
""",
        "expectativa": "≤2 termes tècnics o fallback. NO ha de sortir mitja/botons/agulla/fil.",
        "quotidianes_que_no_haurien_de_sortir": {"mitja", "botó", "botons", "agulla",
                                                  "agulles", "fil", "retolador", "ulls",
                                                  "boca", "cap", "vella"},
    },
    "fotosintesi": {
        "profile": {"caracteristiques": {"nouvingut": {"actiu": True, "L1": "àrab"}}},
        "context": {"etapa": "ESO", "materia": "ciències naturals", "curs": "1r"},
        "mecr": "A2",
        "adapted": """# La fotosíntesi de les plantes

Les plantes fan el seu propi menjar. Aquest procés es diu fotosíntesi.

Per fer la fotosíntesi, les plantes necessiten tres coses:
- Llum del sol
- Aigua
- Diòxid de carboni de l'aire

Les fulles són on passa la fotosíntesi. Tenen una substància verda anomenada clorofil·la. La clorofil·la captura la llum del sol.

L'aigua entra per les arrels. El diòxid de carboni entra per uns forats petits a les fulles, anomenats estomes.

Amb aquests tres ingredients, la planta fa glucosa. La glucosa és com el sucre que dona energia a la planta. Com a residu, la planta allibera oxigen a l'aire.
""",
        "expectativa": "Taula 4 cols (Terme | Explicació | L1 àrab | Transliteració). Termes tècnics + alguns BICS si activen TOLC.",
        "termes_tecnics_esperats": {"fotosíntesi", "clorofil·la", "estomes", "glucosa", "diòxid de carboni"},
    },
    "democracia": {
        "profile": {"caracteristiques": {"tdah": {"actiu": True, "grau": "lleu"}}},
        "context": {"etapa": "ESO", "materia": "història", "curs": "4t"},
        "mecr": "B1",
        "adapted": """# La democràcia atenenca

Atenes va ser la primera ciutat on hi va haver democràcia. Va passar al segle V abans de Crist.

La paraula democràcia ve del grec: "demos" vol dir poble i "kratos" vol dir poder.

A la democràcia atenenca, els ciutadans es reunien a l'àgora, la plaça pública. Allà debatien les lleis i feien votacions.

No tothom era ciutadà. Només els homes adults nascuts a Atenes podien votar. Les dones, els esclaus i els estrangers (anomenats metecs) no tenien drets polítics.

La màxima institució era l'eclèsia. També hi havia un consell anomenat bulé, format per 500 ciutadans escollits per sorteig.

Polítics famosos com Pèricles van impulsar reformes. Per exemple, va introduir el misthos: pagar als ciutadans pobres perquè poguessin assistir a l'assemblea.
""",
        "expectativa": "Taula 2 cols normal. 10-12 termes polítics. SENSE cols L1/transliteració.",
        "termes_esperats": {"democràcia", "àgora", "eclèsia", "bulé", "metecs", "misthos"},
    },
}


def build_prompt_v2(case_key: str) -> str:
    """System prompt amb la rúbrica v2 simplificada."""
    c = CASES[case_key]
    rubrica = json.loads(RUBRICA_V2_PATH.read_text(encoding="utf-8"))

    mecr = c["mecr"]
    lang = "ca"
    profile = c["profile"]
    chars = profile.get("caracteristiques", {})
    nouvingut = chars.get("nouvingut", {})
    L1 = nouvingut.get("L1", "") if nouvingut.get("actiu") else ""

    nivell_data = rubrica["levels"].get(mecr, {})
    alfabets_no_llatins = rubrica["alfabets_no_llatins_que_activen_translit"]
    L1_no_llati = bool(L1) and any(a in L1.lower() for a in alfabets_no_llatins)

    # Determinar format columnes
    if not L1:
        format_cols = "2_cols (Terme | Explicació)"
        cols_header = "| Terme | Explicació |"
        cols_sep = "| :--- | :--- |"
    elif L1 and not L1_no_llati:
        format_cols = f"3_cols (Terme | Explicació | Traducció {L1})"
        cols_header = f"| Terme | Explicació | Traducció ({L1}) |"
        cols_sep = "| :--- | :--- | :--- |"
    else:
        format_cols = f"4_cols (Terme | Explicació | Traducció {L1} alfabet original | Transliteració)"
        cols_header = f"| Terme | Explicació | Traducció ({L1}) | Transliteració |"
        cols_sep = "| :--- | :--- | :--- | :--- |"

    # Determinar perfil de selecció
    aacc_actiu = chars.get("altes_capacitats", {}).get("actiu") or chars.get("aacc", {}).get("actiu")
    if aacc_actiu:
        perfil_sel = "alumne_AACC_o_capacitat_alta"
    elif L1:
        perfil_sel = "alumne_nouvingut_amb_L1"
    else:
        perfil_sel = "alumne_general"

    regla_sel = rubrica["regla_seleccio_per_perfil"][perfil_sel]

    prompt = f"""Ets un generador de glossari per a textos educatius adaptats.

REPS un text ja adaptat. GENERA NOMÉS la secció `## Glossari` (cap altra secció,
cap pròleg). Llengua de sortida: català.

PRINCIPI RECTOR:
{rubrica["principi_general"]["regla_seleccio_simple"]}

REGLA SELECCIÓ PER A AQUEST PERFIL ({perfil_sel}):

```json
{json.dumps(regla_sel, ensure_ascii=False, indent=2)}
```

PARÀMETRES DEL NIVELL {mecr}:

```json
{json.dumps(nivell_data, ensure_ascii=False, indent=2)}
```

FORMAT DE LA TAULA OBLIGATORI: {format_cols}

Capçalera exacta:
{cols_header}
{cols_sep}

CRITERIS TRANSVERSALS (obligatoris):
- No-circularitat: el terme MAI dins la pròpia definició.
- Llengua definició: català. MAI mots d'altres llengües dins la cel·la 'Explicació'
  (excepte la traducció a la columna L1 / Transliteració).
- Fidelitat: tots els termes han d'aparèixer literalment al text adaptat.
- Format: comença amb `## Glossari` (cap subtítol H3).

PROCEDIMENT:

1. Identifica candidats: paraules del text que CALDRIA explicar per al nivell {mecr}.
2. Filtra segons la 'regla seleccio per a aquest perfil':
   - Inclou només si compleix algun dels criteris d'inclou_si.
   - Descarta si està a exclou_explicitament.
3. Tria entre {nivell_data.get("min_terms", 5)} i {nivell_data.get("max_terms", 8)} termes ordenats per rellevància.
4. Defineix cada terme amb max {nivell_data.get("max_paraules_definicio", 8)} paraules en català senzill.
5. {f"Tradueix cada terme a {L1} en alfabet original a la columna 'Traducció ({L1})'." if L1 else "No afegeixis cap columna addicional."}
6. {f"Afegeix transliteració llatina aproximada a la columna 'Transliteració' (només per a alumnes que estan aprenent l'alfabet llatí)." if L1_no_llati else ""}

NOTA IMPORTANT: el docent podrà esborrar entries que no consideri necessàries al Pas 3.
No t'esforcis a ser perfecte — proposa una primera versió raonable.

OUTPUT: només la secció markdown `## Glossari` amb la taula. Res més."""
    return prompt


# ── Extractor i scorer ────────────────────────────────────────────────────

def extract_glossari_section(text: str) -> str | None:
    m = re.search(r"^## Glossari\b[^\n]*$", text, re.MULTILINE | re.IGNORECASE)
    if not m:
        return None
    nxt = re.search(r"^## ", text[m.end():], re.MULTILINE)
    end = m.end() + nxt.start() if nxt else len(text)
    return text[m.start():end]


def count_table_columns(section: str) -> int:
    """Detecta el nombre de columnes de la primera fila de capçalera."""
    for line in section.splitlines():
        line = line.strip()
        if line.startswith("|") and "|" in line[1:]:
            cells = [c.strip() for c in line.strip("|").split("|")]
            if cells and "terme" in cells[0].lower():
                return len(cells)
    return 0


def extract_terms(section: str) -> list[str]:
    terms = []
    for line in section.splitlines():
        line = line.strip()
        if not line.startswith("|") or "|" not in line[1:]:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        t = cells[0].strip()
        if re.match(r"^[-:\s]+$", t) or t.lower() in ("terme", "term"):
            continue
        t = re.sub(r"[*_`]", "", t).strip().lower()
        if t:
            terms.append(t)
    return terms


def score_run_v2(raw: str, case_key: str) -> dict:
    c = CASES[case_key]
    clean = _post_process_llm_output(clean_gemini_output(raw), lang="ca")
    section = extract_glossari_section(clean)
    if section is None:
        return {"ok": False, "reason": "secció absent", "section": None}
    cols = count_table_columns(section)
    terms = extract_terms(section)

    # Checks per cas
    fails = []
    if "quotidianes_que_no_haurien_de_sortir" in c:
        quot = sorted(set(terms) & c["quotidianes_que_no_haurien_de_sortir"])
        if quot:
            fails.append(f"quotidianes={quot}")

    # Cas fotosintesi: ha de tenir 4 cols (L1=àrab)
    if case_key == "fotosintesi":
        if cols != 4:
            fails.append(f"cols={cols} (esperat 4 per àrab)")
        # Comprovar que hi ha algun terme tècnic esperat
        if not any(te in " ".join(terms) for te in c["termes_tecnics_esperats"]):
            fails.append("manquen termes tècnics esperats")

    # Cas democracia: ha de tenir 2 cols (sense L1)
    if case_key == "democracia":
        if cols != 2:
            fails.append(f"cols={cols} (esperat 2 sense L1)")

    return {
        "ok": not fails,
        "reason": "OK" if not fails else " | ".join(fails),
        "cols": cols,
        "n_terms": len(terms),
        "terms": terms,
        "section": section,
    }


# ── Variants ──────────────────────────────────────────────────────────────

VARIANTS = {
    "Bv2": {"label": "GPT-4o + JSON v2 (sense case_overrides)", "model": "gpt-4o"},
    "Cv2": {"label": "Gemma 4 + JSON v2",                       "model": "gemma4"},
}


def run_variant(case_key: str, variant_key: str, reps: int) -> list[dict]:
    v = VARIANTS[variant_key]
    system = build_prompt_v2(case_key)
    user = f"TEXT ADAPTAT:\n{CASES[case_key]['adapted']}\n\nGenera la secció ## Glossari."
    print(f"   [{variant_key}] sys={len(system)}ch  ", end="", flush=True)
    rs = []
    for k in range(reps):
        t0 = time.time()
        try:
            raw = _call_llm(v["model"], system, user)
            r = score_run_v2(raw, case_key)
            r["raw"] = raw
        except Exception as e:
            r = {"ok": False, "reason": f"EXC: {type(e).__name__}: {str(e)[:80]}"}
        r["elapsed_s"] = round(time.time() - t0, 1)
        rs.append(r)
        icon = "OK" if r.get("ok") else "FAIL"
        extra = f" cols={r.get('cols','?')} n={r.get('n_terms','?')}"
        print(f"r{k+1}={icon}({r['elapsed_s']}s,{extra})", end=" ", flush=True)
    n_ok = sum(1 for r in rs if r.get("ok"))
    print(f"→ {n_ok}/{reps}")
    return rs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=2)
    ap.add_argument("--cases", type=str, default="titella,fotosintesi,democracia")
    ap.add_argument("--dump", action="store_true")
    args = ap.parse_args()

    case_keys = [k.strip() for k in args.cases.split(",") if k.strip()]
    variant_keys = ["Bv2", "Cv2"]

    print(f"\nPILOT v2 — opció E (rúbrica simplificada, vàlvula humana al Pas 3)")
    print(f"  Casos:    {case_keys}")
    print(f"  Variants: {variant_keys}")
    print(f"  Reps:     {args.reps}")

    all_results: dict = {}
    for case_key in case_keys:
        c = CASES[case_key]
        print(f"\n{'='*72}\n  CAS: {case_key} ({c['mecr']})\n  Esperat: {c['expectativa']}\n{'='*72}")
        all_results[case_key] = {}
        for vk in variant_keys:
            all_results[case_key][vk] = run_variant(case_key, vk, args.reps)

    # Resum
    print(f"\n{'='*72}\n  RESUM v2\n{'='*72}")
    totals = {v: [0, 0] for v in variant_keys}
    for case_key in case_keys:
        cells = []
        for vk in variant_keys:
            rs = all_results[case_key][vk]
            n_ok = sum(1 for r in rs if r.get("ok"))
            cells.append(f"{vk}={n_ok}/{len(rs)}")
            totals[vk][0] += n_ok
            totals[vk][1] += len(rs)
        print(f"  {case_key:<14} " + "  ".join(cells))
    print(f"  {'TOTAL':<14} " + "  ".join(f"{vk}={t[0]}/{t[1]}" for vk, t in totals.items()))

    # Detall
    print(f"\n{'='*72}\n  DETALL\n{'='*72}")
    for case_key in case_keys:
        for vk in variant_keys:
            for i, r in enumerate(all_results[case_key][vk]):
                status = "✓" if r.get("ok") else "✗"
                print(f"  {status} {case_key}/{vk}/rep{i+1}: {r['reason']}")
                if r.get("terms"):
                    print(f"      termes ({r['n_terms']}): {r['terms'][:8]}{'...' if len(r['terms']) > 8 else ''}")

    if args.dump:
        out = PILOT_DIR / f"resultats_v2_{int(time.time())}.json"
        dump = {ck: {vk: [{k: v for k, v in r.items() if k != "raw"} for r in rs]
                     for vk, rs in vd.items()}
                for ck, vd in all_results.items()}
        out.write_text(json.dumps(dump, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n[dump] {out}")

    sys.exit(0)


if __name__ == "__main__":
    main()
