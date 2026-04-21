"""
Bateria de tests automatics contra /api/adapt del Cloud Run.

Executa 10 perfils representatius amb 2 models (Gemma 4 31B, Gemma 3 27B),
recull els JSONs d'auditoria (prompt + adapted_raw + adapted_output),
detecta divergencies sospitoses entre raw i output, i genera un report
markdown amb alertes.

Us:
    python tests/test_pipeline_corpus.py --token "eyJ..." --admin-password "..."
    python tests/test_pipeline_corpus.py --token "eyJ..." --admin-password "..." --only gemma4

Token JWT: obte'l del DevTools (Application -> Local Storage -> atne_jwt).
Caduca en ~1h.

Admin password: la mateixa que uses a /admin/ per veure l'Historial.
Necessari per cridar /api/audit/* i obtenir els JSONs d'adapted_raw.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import unicodedata
from datetime import datetime
from pathlib import Path

import requests

BASE_URL = "https://atne-1050342211642.europe-west1.run.app"

TEXT_INPUT = """## Ecosistemes: la vida en interacció

Un **ecosistema** és un sistema natural format per un conjunt d'**organismes vius** (components biòtics) i el **medi físic** on viuen (components abiòtics), que interactuen entre ells. Aquesta interacció és essencial per al manteniment de la vida i l'equilibri del sistema.

Els **components biòtics** inclouen tots els éssers vius: plantes, animals, microorganismes (bacteris, fongs, virus...). Es classifiquen segons el seu paper en l'ecosistema:

* **Productors**: són els organismes autòtrofs, com les plantes, que obtenen l'energia del sol a través de la **fotosíntesi** i la transformen en matèria orgànica. Són la base de la cadena tròfica.
* **Consumidors**: són els organismes heteròtrofs que s'alimenten d'altres organismes.
* **Descompositors**: són els organismes que s'alimenten de la matèria orgànica morta, descomponent-la i alliberen nutrients al medi.

Els **components abiòtics** són els factors físics i químics que influeixen en els organismes vius: llum solar, temperatura, aigua, sòl, aire.

La **xarxa tròfica** representa les relacions alimentàries entre els organismes d'un ecosistema. L'energia flueix a través de la xarxa tròfica, des dels productors fins als consumidors i, finalment, als descomponedors."""

# ══ 10 perfils representatius ══════════════════════════════════════════════
PROFILES = [
    {
        "slug": "01_tdah_combinat",
        "nom": "Test TDAH Combinat",
        "caracteristiques": {
            "tdah": {"actiu": True, "grau": "moderat", "subtipus": "Combinat"},
        },
        "mecr": "B1",
    },
    {
        "slug": "02_dislexia_moderada",
        "nom": "Test Dislexia",
        "caracteristiques": {
            "dislexia": {"actiu": True, "grau": "moderat", "tipus": "fonologica"},
        },
        "mecr": "B1",
    },
    {
        "slug": "03_nouvingut_xines_3m",
        "nom": "Test Nouvingut Xines",
        "caracteristiques": {
            "nouvingut": {
                "actiu": True,
                "l1": "Xinès mandarí",
                "pais": "Xina",
                "mesos_catalunya": 3,
                "alfabet_llati": False,
                "alfabetitzacio_l1": True,
                "escolaritzacio": "regular",
            },
        },
        "mecr": "A2",
    },
    {
        "slug": "04_nouvingut_frances_12m",
        "nom": "Test Nouvingut Frances",
        "caracteristiques": {
            "nouvingut": {
                "actiu": True,
                "l1": "Francès",
                "pais": "França",
                "mesos_catalunya": 12,
                "alfabet_llati": True,
                "alfabetitzacio_l1": True,
                "escolaritzacio": "regular",
            },
        },
        "mecr": "B1",
    },
    {
        "slug": "05_tdah_mes_dislexia",
        "nom": "Test TDAH + Dislexia",
        "caracteristiques": {
            "tdah": {"actiu": True, "grau": "moderat", "subtipus": "Desatent"},
            "dislexia": {"actiu": True, "grau": "lleu", "tipus": "superficial"},
        },
        "mecr": "B1",
    },
    {
        "slug": "06_nouvingut_mes_tdah",
        "nom": "Test Nouvingut + TDAH",
        "caracteristiques": {
            "nouvingut": {
                "actiu": True,
                "l1": "Àrab",
                "pais": "Marroc",
                "mesos_catalunya": 6,
                "alfabet_llati": False,
                "alfabetitzacio_l1": True,
                "escolaritzacio": "regular",
            },
            "tdah": {"actiu": True, "grau": "moderat", "subtipus": "Combinat"},
        },
        "mecr": "A2",
    },
    {
        "slug": "07_tea_nivell1",
        "nom": "Test TEA N1",
        "caracteristiques": {
            "tea": {"actiu": True, "suport_nivell": "baix"},
        },
        "mecr": "B1",
    },
    {
        "slug": "08_aacc",
        "nom": "Test AACC",
        "caracteristiques": {
            "altes_capacitats": {"actiu": True},
        },
        "mecr": "B2",
    },
    {
        "slug": "09_di_lleugera",
        "nom": "Test DI Lleugera",
        "caracteristiques": {
            "di": {"actiu": True, "grau": "lleuger"},
        },
        "mecr": "A2",
    },
    {
        "slug": "10_grup_multinivell",
        "nom": "Test Grup 3r ESO",
        "caracteristiques": {},
        "group": True,
        "levels": ["basic", "standard", "advanced"],
        "mecr": "B1",
    },
]

MODELS = [
    ("gemma4", "gemma-4-31b-it"),
    ("gemma3", "gemma-3-27b-it"),
]

# ══ Request helpers ════════════════════════════════════════════════════════

def _headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


def admin_login(session: requests.Session, password: str) -> bool:
    """Fa login admin i guarda el cookie atne_admin a la sessio."""
    try:
        resp = session.post(
            f"{BASE_URL}/api/admin/login",
            json={"password": password},
            timeout=15,
        )
        return resp.status_code == 200
    except requests.RequestException:
        return False


def _build_payload(profile_def: dict, model: str) -> dict:
    """Construeix el payload esperat per /api/adapt."""
    is_group = profile_def.get("group", False)
    base_profile = {
        "nom": profile_def["nom"],
        "caracteristiques": profile_def.get("caracteristiques", {}),
        "canal_preferent": "text",
        "observacions": "",
        "_via": "diagnostic",
        "group": is_group,
    }
    if is_group:
        base_profile["members"] = [
            {"pid": "basic", "nivell": "basic"},
            {"pid": "standard", "nivell": "standard"},
            {"pid": "advanced", "nivell": "advanced"},
        ]

    params = {
        "mecr_sortida": profile_def["mecr"],
        "levels": profile_def.get("levels", ["single"]),
        "complements": {
            "glossari": True,
            "esquema_visual": True,
            "bastides": True,
            "pictogrames": True,
            "preguntes_comprensio": True,
        },
    }
    return {
        "text": TEXT_INPUT,
        "profile": base_profile,
        "context": {
            "materia": "Història",
            "nivell_curs": "3r ESO",
            "titol": "## Ecosistemes: la vida en interacció",
        },
        "params": params,
        "model": model,
    }


def _call_adapt_sse(session: requests.Session, token: str, payload: dict,
                     timeout: int = 300) -> tuple[bool, str]:
    """Crida SSE bloquejant a /api/adapt. Retorna (ok, error_msg)."""
    url = f"{BASE_URL}/api/adapt"
    try:
        resp = session.post(
            url, headers=_headers(token), json=payload,
            stream=True, timeout=timeout,
        )
    except requests.RequestException as e:
        return False, f"Exception: {type(e).__name__}: {e}"
    if resp.status_code != 200:
        body = resp.text[:500] if resp.text else ""
        return False, f"HTTP {resp.status_code}: {body}"
    # Consumeix el stream fins al 'done' global
    got_done = False
    for line in resp.iter_lines(decode_unicode=True):
        if not line:
            continue
        if line.startswith("data: "):
            try:
                ev = json.loads(line[6:])
            except Exception:
                continue
            if ev.get("type") == "done":
                got_done = True
                break
    if not got_done:
        return False, "SSE closed without 'done' event"
    return True, ""


def _fetch_audit_list(session: requests.Session, token: str,
                      retries: int = 3) -> list[dict]:
    """Agafa la llista recent d'adaptacions."""
    for i in range(retries):
        try:
            resp = session.get(
                f"{BASE_URL}/api/audit/adaptations",
                headers=_headers(token), timeout=30,
            )
            if resp.status_code == 200:
                return resp.json().get("adaptations", [])
        except requests.RequestException:
            pass
        time.sleep(2)
    return []


def _fetch_audit_detail(session: requests.Session, token: str, adapt_id: str,
                        retries: int = 3) -> dict | None:
    """Agafa el detall complet d'una adaptació."""
    for i in range(retries):
        try:
            resp = session.get(
                f"{BASE_URL}/api/audit/adaptations/{adapt_id}",
                headers=_headers(token), timeout=30,
            )
            if resp.status_code == 200:
                return resp.json().get("data")
        except requests.RequestException:
            pass
        time.sleep(2)
    return None


# ══ Detector de divergencies raw vs output ════════════════════════════════

def _tokenize_words(s: str) -> list[str]:
    """Tokens de paraules (ignora puntuacio)."""
    return re.findall(r"[A-Za-zÀ-ÿ]{2,}", s)


def _norm_accent(w: str) -> str:
    """Treure accents per comparar paraules amb/sense accent."""
    nfkd = unicodedata.normalize("NFKD", w.lower())
    return nfkd.encode("ascii", "ignore").decode("ascii")


def diff_raw_vs_output(raw: str, output: str) -> list[dict]:
    """Detecta canvis sospitosos entre raw i output.

    Retorna llista d'alertes:
    - llm_error: l'LLM ha retornat un missatge d'error (raw buit)
    - missing_word: paraula del raw que no apareix a l'output
    - broken_word: token a l'output que no existeix al raw ni sembla catala
    - backtick_loss: triple backticks perduts
    - emoji_mutation: emojis que han canviat
    """
    alerts = []

    # 0. Deteccio de FAIL silencios del LLM
    if not raw or len(raw) < 100:
        if output.startswith("Error en la generació"):
            alerts.append({
                "type": "llm_error",
                "severity": "err",
                "output_msg": output[:250],
            })
            return alerts  # no sentit continuar amb altres detectors
        alerts.append({
            "type": "empty_raw",
            "severity": "err",
            "raw_len": len(raw) if raw else 0,
            "output_sample": output[:250] if output else "",
        })
        return alerts

    # 1. Paraules del raw que no apareixen a l'output (ni amb/sense accent)
    raw_words = set(_norm_accent(w) for w in _tokenize_words(raw) if len(w) >= 4)
    out_words = set(_norm_accent(w) for w in _tokenize_words(output) if len(w) >= 4)
    missing = raw_words - out_words
    # Filtrem les que son variants amb/sense accent (ja cobertes per norm)
    if missing:
        # Nomes alertem si son mes de 3 (LT pot treure algunes paraules com correccio)
        if len(missing) > 3:
            alerts.append({
                "type": "missing_words",
                "severity": "warn",
                "count": len(missing),
                "sample": sorted(missing)[:10],
            })

    # 2. Triple backticks perduts
    raw_bt3 = raw.count("```")
    out_bt3 = output.count("```")
    if raw_bt3 > out_bt3:
        alerts.append({
            "type": "backtick_loss",
            "severity": "err",
            "raw_count": raw_bt3,
            "output_count": out_bt3,
        })

    # 3. Negretes markdown desaparegudes
    raw_bold = raw.count("**")
    out_bold = output.count("**")
    if raw_bold - out_bold > 4:  # tolerancia petita
        alerts.append({
            "type": "bold_loss",
            "severity": "warn",
            "raw_count": raw_bold,
            "output_count": out_bold,
        })

    # 4. Longitud drasticament diferent (post-process redueix una mica pero no molt)
    raw_len = len(raw)
    out_len = len(output)
    if raw_len > 0:
        diff_pct = abs(raw_len - out_len) / raw_len * 100
        if diff_pct > 10:
            alerts.append({
                "type": "length_diff",
                "severity": "warn",
                "raw_len": raw_len,
                "output_len": out_len,
                "diff_pct": round(diff_pct, 1),
            })

    # 5. Paraules trencades classiques: caracters inserits al mig
    # Busquem patrons com "mandarí.ors", "visnatura.comanat" (caracter estrany al mig)
    suspicious_pattern = re.compile(r"\b[A-Za-zÀ-ÿ]{2,}[.|)'|][A-Za-zÀ-ÿ]{2,}\b")
    suspicious_matches = suspicious_pattern.findall(output)
    # Filtrem coses legítimes com apostrofs
    real_bugs = [m for m in suspicious_matches
                 if "'" not in m and "." in m[1:-1]]
    if real_bugs:
        alerts.append({
            "type": "broken_words",
            "severity": "err",
            "count": len(real_bugs),
            "sample": real_bugs[:10],
        })

    return alerts


# ══ Verificacio d'instruccions esperades ═════════════════════════════════

EXPECTED_INSTRUCTION_PATTERNS = {
    "tdah": ["TDAH:", "tdah", "atenció", "micro-blocs"],
    "dislexia": ["dislèxia", "dislexia", "fonològic"],
    "nouvingut": ["PERSONA-AUDIENCE", "nouvingut"],
    "tea": ["TEA", "estructura", "literal"],
    "altes_capacitats": ["altes capacitats", "enriquiment", "AACC"],
    "di": ["discapacitat intel", "DI"],
}

def check_prompt_coherence(profile_def: dict, system_prompt: str) -> list[dict]:
    """Verifica que els perfils actius apareixen al prompt."""
    alerts = []
    chars = profile_def.get("caracteristiques", {})
    for cond, attrs in chars.items():
        if not (isinstance(attrs, dict) and attrs.get("actiu")):
            continue
        patterns = EXPECTED_INSTRUCTION_PATTERNS.get(cond, [])
        if patterns and not any(p.lower() in system_prompt.lower() for p in patterns):
            alerts.append({
                "type": "missing_condition_in_prompt",
                "severity": "err",
                "condition": cond,
                "expected_any": patterns,
            })
    return alerts


# ══ Execucio principal ═════════════════════════════════════════════════════

def run_test_case(session: requests.Session, token: str, profile_def: dict,
                  model_alias: str, model_id: str, out_dir: Path) -> dict:
    print(f"  · {profile_def['slug']} / {model_alias}...", end="", flush=True)
    t0 = time.time()
    payload = _build_payload(profile_def, model_id)

    ok, err = _call_adapt_sse(session, token, payload)
    if not ok:
        print(f" FAIL ({err[:80]})")
        return {"slug": profile_def["slug"], "model": model_alias,
                "ok": False, "error": err, "elapsed": time.time() - t0}

    # Espera 3s perque Supabase persisteixi
    time.sleep(3)
    lst = _fetch_audit_list(session, token)
    if not lst:
        print(" FAIL (audit list buida)")
        return {"slug": profile_def["slug"], "model": model_alias,
                "ok": False, "error": "audit list empty"}

    # Agafa la mes recent (la primera)
    latest = lst[0]
    detail = _fetch_audit_detail(session, token, latest["id"])
    if not detail:
        print(" FAIL (detail buit)")
        return {"slug": profile_def["slug"], "model": model_alias,
                "ok": False, "error": "audit detail empty"}

    # Guarda el JSON
    out_file = out_dir / f"{profile_def['slug']}__{model_alias}.json"
    out_file.write_text(json.dumps(detail, ensure_ascii=False, indent=2),
                        encoding="utf-8")

    # Analitza
    diff_alerts = diff_raw_vs_output(
        detail.get("adapted_raw", ""),
        detail.get("adapted_output", ""),
    )
    prompt_alerts = check_prompt_coherence(
        profile_def,
        detail.get("system_prompt", ""),
    )
    all_alerts = diff_alerts + prompt_alerts

    elapsed = time.time() - t0
    status = "OK" if not all_alerts else f"⚠ {len(all_alerts)} alertes"
    print(f" {status} ({elapsed:.0f}s)")

    return {
        "slug": profile_def["slug"],
        "model": model_alias,
        "ok": True,
        "alerts": all_alerts,
        "n_instructions": detail.get("n_instructions"),
        "instruction_ids": detail.get("instruction_ids", []),
        "raw_len": detail.get("adapted_raw_len", 0),
        "output_len": detail.get("adapted_output_len", 0),
        "prompt_len": detail.get("system_prompt_len", 0),
        "elapsed": round(elapsed, 1),
        "json_file": str(out_file.name),
    }


def generate_report(results: list[dict], out_dir: Path) -> None:
    lines = [
        f"# ATNE Pipeline Corpus Report — {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        f"**Total tests**: {len(results)}",
        f"**OK**: {sum(1 for r in results if r.get('ok') and not r.get('alerts'))}",
        f"**Amb alertes**: {sum(1 for r in results if r.get('ok') and r.get('alerts'))}",
        f"**Errors**: {sum(1 for r in results if not r.get('ok'))}",
        "",
        "## Taula resum",
        "",
        "| Perfil | Model | Status | Alertes | Prompt (paraules) | Raw→Output (chars) | Temps |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in results:
        if not r.get("ok"):
            status = f"❌ {r.get('error', '')[:40]}"
            alerts_str = "-"
            prompt = "-"
            sizes = "-"
        else:
            alerts_str = (f"⚠ {len(r['alerts'])}" if r["alerts"] else "✅ 0")
            status = "OK"
            prompt = str(r.get("prompt_len", "?"))
            sizes = f"{r.get('raw_len')} → {r.get('output_len')}"
        lines.append(
            f"| {r['slug']} | {r['model']} | {status} | {alerts_str} | "
            f"{prompt} | {sizes} | {r.get('elapsed', '-')}s |"
        )

    lines.extend(["", "## Alertes per test", ""])
    any_alert = False
    for r in results:
        if not r.get("ok") or not r.get("alerts"):
            continue
        any_alert = True
        lines.append(f"### {r['slug']} / {r['model']}")
        lines.append("")
        for a in r["alerts"]:
            sev = "🔴" if a.get("severity") == "err" else "🟡"
            details = {k: v for k, v in a.items() if k != "type" and k != "severity"}
            lines.append(f"- {sev} **{a['type']}**: {json.dumps(details, ensure_ascii=False)}")
        lines.append(f"- JSON: [`{r['json_file']}`]({r['json_file']})")
        lines.append("")
    if not any_alert:
        lines.append("*Cap alerta detectada.*")

    report_file = out_dir / "report.md"
    report_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n📄 Report: {report_file}")


def main() -> int:
    global BASE_URL
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", help="JWT Supabase (del localStorage atne_jwt)")
    parser.add_argument("--token-file", help="Fitxer amb el token")
    parser.add_argument("--admin-password", help="Password admin per /api/audit/*")
    parser.add_argument("--only", choices=["gemma4", "gemma3"],
                        help="Limitar a un sol model")
    parser.add_argument("--only-profile", help="Limitar a un slug de perfil")
    parser.add_argument("--base-url", default=BASE_URL)
    parser.add_argument("--output", default="tests/results")
    args = parser.parse_args()

    BASE_URL = args.base_url

    # Carregar token
    token = None
    if args.token:
        token = args.token.strip().lstrip("\ufeff")
    elif args.token_file:
        # utf-8-sig descarta el BOM si el fitxer es va crear amb encoding UTF-8 BOM
        token = Path(args.token_file).read_text(encoding="utf-8-sig").strip().lstrip("\ufeff")
    else:
        token = os.environ.get("ATNE_TEST_JWT", "").strip().lstrip("\ufeff") or None
    if not token:
        print("ERROR: cal --token, --token-file o env ATNE_TEST_JWT", file=sys.stderr)
        return 2

    admin_pwd = args.admin_password or os.environ.get("ATNE_ADMIN_PASSWORD", "").strip()
    if not admin_pwd:
        print("ERROR: cal --admin-password o env ATNE_ADMIN_PASSWORD", file=sys.stderr)
        return 2

    # Sessio compartida (guarda el cookie admin entre crides)
    session = requests.Session()

    # Login admin
    if not admin_login(session, admin_pwd):
        print("ERROR: login admin fallit (password incorrecte o ADMIN_PASSWORD no configurat al servidor)")
        return 3

    # Verifica JWT + admin cookie
    probe = session.get(f"{BASE_URL}/api/audit/adaptations",
                        headers=_headers(token), timeout=15)
    if probe.status_code != 200:
        print(f"ERROR: verificacio fallida (HTTP {probe.status_code})")
        print(probe.text[:300])
        return 3

    # Output dir
    ts = datetime.now().strftime("%Y-%m-%d_%H%M")
    out_dir = Path(args.output) / ts
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output: {out_dir}")

    # Filtrar models i perfils
    models_to_run = [(a, m) for (a, m) in MODELS if not args.only or a == args.only]
    profiles_to_run = [p for p in PROFILES if not args.only_profile or p["slug"] == args.only_profile]

    print(f"\nPerfils: {len(profiles_to_run)} · Models: {len(models_to_run)} · "
          f"Total crides: {len(profiles_to_run) * len(models_to_run)}\n")

    results = []
    for alias, mid in models_to_run:
        print(f"=== Model: {alias} ({mid}) ===")
        for prof in profiles_to_run:
            r = run_test_case(session, token, prof, alias, mid, out_dir)
            results.append(r)
        print()

    # Guarda results.json
    results_file = out_dir / "results.json"
    results_file.write_text(json.dumps(results, ensure_ascii=False, indent=2),
                            encoding="utf-8")

    # Genera report.md
    generate_report(results, out_dir)

    # Estadistiques finals
    n_ok = sum(1 for r in results if r.get("ok") and not r.get("alerts"))
    n_warn = sum(1 for r in results if r.get("ok") and r.get("alerts"))
    n_err = sum(1 for r in results if not r.get("ok"))
    print(f"\n✅ OK: {n_ok} · ⚠ Amb alertes: {n_warn} · ❌ Errors: {n_err}")
    return 0 if n_err == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
