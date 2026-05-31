"""Pilot 2026-05-31 — JSON estructurat vs prompt descriptiu+directiva Python per a BASTIDES.

Extensió del pilot glossari. Bastides comparteix agent_role=complements amb glossari
i té la peculiaritat que actualment el system prompt combina:
  1) SKILL.md body (descriptiu canon)
  2) prompt_adapter.md llescat per nivell (descriptiu)
  3) Directiva Python explícita a build_complements_prompt (els "_bastides_moments")
La directiva Python es va afegir el 31/05 com a workaround perquè el LLM relabela
la secció ## Bastides com a ## Preguntes quan els ítems estaven en forma de pregunta.

Aquest pilot mesura si la rúbrica JSON estructurada amb checks operatius
(imperativitat, max 3 ítems, format estructural fix, pausa obligatòria B1+)
pot SUBSTITUIR la directiva Python sense pèrdua de qualitat.

Casos:
  1. bastides_A1  — primaria 3r · A1 · sense altres complements
  2. bastides_B1  — ESO 2n · B1 · sense altres complements

Variants:
  A · GPT-4o + descriptiu+directiva Python (baseline actual)
  B · GPT-4o + JSON estructurat (sense directiva Python)
  C · Gemma 4 + JSON estructurat (sense directiva Python)

2 reps cada → 12 crides totals.

Ús:
  python tests/pilot_glossari_2026_05_31/pilot_bastides.py
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

from adaptation.prompt_builder import build_complements_prompt
from adaptation.llm_clients import _call_llm
from adaptation.post_process import clean_gemini_output, _post_process_llm_output


PILOT_DIR = Path(__file__).resolve().parent
RUBRICA_JSON_PATH = PILOT_DIR / "rubrica_bastides_lectura.json"


CASES = {
    "bastides_A1": {
        "label": "Bastides lectura · A1 · primària 3r",
        "profile": {"caracteristiques": {}},
        "context": {"etapa": "Primària", "materia": "ciències socials", "curs": "3r"},
        "params": {
            "mecr_sortida": "A1",
            "dua": "Core",
            "genere_discursiu": "divulgatiu",
            "lang": "ca",
            "complements": {"bastides": True},
        },
        "adapted": """# El cicle de l'aigua

L'aigua canvia de forma quan fa calor o quan fa fred.

Quan fa calor, l'aigua del mar es transforma en vapor.
El vapor puja cap al cel.

Al cel, el vapor es transforma en gotes petites.
Les gotes petites fan els núvols.

Quan els núvols són grans, les gotes cauen com a pluja.
La pluja torna a fer rius i mar.

Aquest cicle es repeteix sempre.
""",
        "validators": {
            "must_have_h2_any_of": ["## Suports per llegir", "## Suports de lectura", "## Bastides"],
            "must_have_h3_all": ["Abans", "Durant", "Després"],
            "max_items_per_h3": 3,
            "must_contain_in_despres_any_of": ["El text parla de", "text parla"],
            "marca_pausa_no_obligatoria": True,
        },
    },

    "bastides_B1": {
        "label": "Bastides lectura · B1 · ESO 2n",
        "profile": {"caracteristiques": {}},
        "context": {"etapa": "ESO", "materia": "història", "curs": "2n"},
        "params": {
            "mecr_sortida": "B1",
            "dua": "Core",
            "genere_discursiu": "divulgatiu",
            "lang": "ca",
            "complements": {"bastides": True},
        },
        "adapted": """# L'Edat Mitjana al regne d'Aragó

L'Edat Mitjana va ser un període que va durar gairebé mil anys, del segle V al segle XV.

Al regne d'Aragó, la societat estava dividida en tres estaments. Els nobles tenien les terres i el poder militar. El clergat dirigia l'Església i tenia molta influència. El poble treballava les terres dels nobles i pagava impostos.

Aquesta divisió no era casual: l'Església la justificava com un ordre natural establert per Déu. Aquest discurs ideològic legitimava una desigualtat profunda i feia molt difícil que els treballadors qüestionessin la seva situació.

A partir del segle XII, però, van començar a néixer les ciutats. A les ciutats vivien comerciants i artesans, gent que no encaixava bé dins dels tres estaments tradicionals. Aquesta nova classe, anomenada burgesia, anava guanyant pes econòmic i, amb el temps, qüestionaria l'ordre feudal.

L'Edat Mitjana, doncs, no va ser una època immòbil: va començar amb un món rural i feudal i va acabar amb el naixement d'una societat urbana i comercial que prepararia el Renaixement.
""",
        "validators": {
            "must_have_h2_any_of": ["## Bastides — Estratègia lectora", "## Bastides", "## Suports de lectura"],
            "must_have_h3_all": ["Abans", "Durant", "Després"],
            "max_items_per_h3": 3,
            "must_contain_in_durant_any_of": ["⏸", "atura't", "Atura't", "ATURA"],
            "must_contain_in_abans_any_of": ["hipòtesi", "Crec que", "crec que"],
        },
    },
}


# ── Construcció dels prompts ───────────────────────────────────────────────

def build_prompt_A_descriptiu(case_key: str) -> str:
    """Variant A — el sistema actual amb skill + directiva Python."""
    import os
    os.environ["ATNE_USE_SKILLS"] = "true"
    os.environ["ATNE_USE_PROMPT_ADAPTER"] = "true"
    c = CASES[case_key]
    return build_complements_prompt(c["profile"], c["context"], c["params"])


def build_prompt_B_C_json(case_key: str) -> str:
    """Variants B i C — només el JSON de bastides, sense directiva Python ni skill."""
    c = CASES[case_key]
    rubrica = json.loads(RUBRICA_JSON_PATH.read_text(encoding="utf-8"))

    mecr = c["params"]["mecr_sortida"]
    lang = c["params"].get("lang", "ca")
    dua = c["params"].get("dua", "Core")
    nivell_data = rubrica["levels"].get(mecr, {})
    override_dua = rubrica["case_overrides"]["DUA_acces_nivell_baix_no_escriptura_autonoma"]
    override_actiu = (
        dua == override_dua["trigger"]["dua_equals"]
        and mecr in override_dua["trigger"]["mecr_in"]
    )

    # Triar títol segons regla DUA+MECR (canonic SKILL.md)
    if dua == "Accés" or mecr in ("pre-A1", "A1", "A2"):
        titol = "## Suports per llegir"
    else:
        titol = "## Bastides — Estratègia lectora"

    prompt = f"""Ets un generador de bastides de lectura per a textos educatius adaptats.

REPS un text ja adaptat. GENERA NOMÉS la secció `{titol}` amb les 3 subseccions
obligatòries Abans / Durant / Després. Cap altra secció. Llengua: català.

REGLES (rúbrica estructurada — segueix-les literalment):

```json
{json.dumps({
    "nivell_actiu": mecr,
    "dua": dua,
    "lang": lang,
    "constraints_nivell": nivell_data,
    "titol_obligatori": titol,
    "transversals": rubrica["transversals"],
    "override_dua_actiu": override_actiu,
    "override_dua_definicio": override_dua if override_actiu else None,
}, ensure_ascii=False, indent=2)}
```

PROCEDIMENT OBLIGATORI:

1. Comença amb `{titol}` (exactament així, sense emojis ni variacions).
2. Afegeix exactament 3 subseccions H3: `### Abans`, `### Durant`, `### Després`.
3. A cada subsecció, posa entre 1 i {nivell_data.get("abans", {}).get("max_items", 3)} ítems com a llista (cada ítem amb `- ` al davant).
4. CRÍTIC — CADA ÍTEM ÉS UNA INSTRUCCIÓ IMPERATIVA, MAI UNA PREGUNTA:
   ✅ Bé: "Mira el títol i predigues de què parlarà."
   ❌ Mal: "Què saps del tema?" ← això és pregunta, va al complement preguntes_comprensio
   Cap ítem pot acabar amb "?" ni començar amb "Què/Per què/Com/Quan/On/Qui".
5. {f"A B1+: a `### Durant` ha de aparèixer una marca de PAUSA (⏸ o 'Atura't aquí')" if mecr in ("B1", "B2", "C1+") else f"A {mecr}: NO cal marca de pausa explícita."}
6. {f"A A1: a `### Després` ha d'aparèixer EXACTAMENT la frase-buit «El text parla de ___»." if mecr == "A1" else "Segueix els elements obligatoris del nivell"}
7. El propòsit de lectura ha de referenciar contingut concret del text actual, no ser genèric.

OUTPUT: només la secció markdown completa amb {titol} i les 3 subseccions. Res més."""
    return prompt


# ── Extractors ─────────────────────────────────────────────────────────────

def extract_bastides_section(text: str) -> str | None:
    # Detectem qualsevol dels títols canon
    patterns = [
        r"^##\s+Suports\s+per\s+llegir\b[^\n]*$",
        r"^##\s+Suports\s+de\s+lectura\b[^\n]*$",
        r"^##\s+Bastides\b[^\n]*$",
    ]
    m = None
    for p in patterns:
        m = re.search(p, text, re.MULTILINE | re.IGNORECASE)
        if m:
            break
    if not m:
        return None
    nxt = re.search(r"^##\s", text[m.end():], re.MULTILINE)
    end = m.end() + nxt.start() if nxt else len(text)
    return text[m.start():end]


def extract_h3_sections(section: str) -> dict[str, str]:
    """Extrau {h3_name: body} de les 3 subseccions Abans/Durant/Després."""
    result: dict[str, str] = {}
    h3_matches = list(re.finditer(r"^###\s+(.+?)\s*$", section, re.MULTILINE))
    for i, m in enumerate(h3_matches):
        name = m.group(1).strip()
        # Normalitzem accents: Després/Despres → Després
        name_norm = name.lower().replace("é", "e").replace("è", "e")
        if "abans" in name_norm:
            key = "Abans"
        elif "durant" in name_norm:
            key = "Durant"
        elif "despr" in name_norm:
            key = "Després"
        else:
            continue
        start = m.end()
        end = h3_matches[i + 1].start() if i + 1 < len(h3_matches) else len(section)
        result[key] = section[start:end].strip()
    return result


def count_items_in_h3(body: str) -> int:
    """Compta ítems llista (`- ` al començament de línia)."""
    return sum(1 for ln in body.splitlines() if re.match(r"^\s*[-*]\s+\S", ln))


def items_in_h3(body: str) -> list[str]:
    items = []
    for ln in body.splitlines():
        m = re.match(r"^\s*[-*]\s+(.+)$", ln)
        if m:
            items.append(m.group(1).strip())
    return items


def score_run(raw_output: str, case_key: str) -> dict:
    c = CASES[case_key]
    val = c["validators"]
    clean = _post_process_llm_output(clean_gemini_output(raw_output), lang=c["params"].get("lang", "ca"))
    section = extract_bastides_section(clean)
    if section is None:
        return {"ok": False, "reason": "secció ## Bastides/Suports ABSENT", "section": None}
    h3 = extract_h3_sections(section)

    fails = []

    # Check 1: presència 3 subseccions
    missing_h3 = [h for h in val["must_have_h3_all"] if h not in h3]
    if missing_h3:
        fails.append(f"manca H3: {missing_h3}")

    # Check 2: max items per seccio
    max_items = val["max_items_per_h3"]
    excess = {h: count_items_in_h3(body) for h, body in h3.items()
              if count_items_in_h3(body) > max_items}
    if excess:
        fails.append(f"excés items: {excess}")

    # Check 3: imperativitat (cap ítem acaba amb "?" o comença amb pronom interrogatiu)
    PREGUNTA_RE = re.compile(r"^(Què|Per què|Com|Quan|On|Qui|Quin|Quina|Per a què)\b", re.IGNORECASE)
    preguntes = []
    for h, body in h3.items():
        for it in items_in_h3(body):
            it_stripped = it.rstrip(" *_`")
            if it_stripped.endswith("?") or PREGUNTA_RE.match(it_stripped):
                preguntes.append(f"{h}: {it[:60]}…")
    if preguntes:
        fails.append(f"preguntes detectades ({len(preguntes)}): {preguntes[:2]}")

    # Check 4: frase-buit A1 al Despres
    if "must_contain_in_despres_any_of" in val:
        body_des = h3.get("Després", "")
        if not any(s.lower() in body_des.lower() for s in val["must_contain_in_despres_any_of"]):
            fails.append(f"manca frase-buit a Després")

    # Check 5: pausa B1+
    if "must_contain_in_durant_any_of" in val:
        body_dur = h3.get("Durant", "")
        if not any(s.lower() in body_dur.lower() for s in val["must_contain_in_durant_any_of"]):
            fails.append(f"manca marca pausa a Durant")

    # Check 6: hipòtesi a Abans (B1+)
    if "must_contain_in_abans_any_of" in val:
        body_ab = h3.get("Abans", "")
        if not any(s.lower() in body_ab.lower() for s in val["must_contain_in_abans_any_of"]):
            fails.append(f"manca hipòtesi a Abans")

    ok = not fails
    return {
        "ok": ok,
        "reason": "OK" if ok else " | ".join(fails),
        "h3_keys": list(h3.keys()),
        "h3_counts": {h: count_items_in_h3(b) for h, b in h3.items()},
        "section": section,
        "items_preguntes": preguntes,
    }


# ── Variants ──────────────────────────────────────────────────────────────

VARIANTS = {
    "A": {"label": "GPT-4o + descriptiu+directiva Python (baseline)", "model": "gpt-4o",
          "system_builder": build_prompt_A_descriptiu},
    "B": {"label": "GPT-4o + JSON (sense directiva)",                "model": "gpt-4o",
          "system_builder": build_prompt_B_C_json},
    "C": {"label": "Gemma 4 + JSON (sense directiva)",               "model": "gemma4",
          "system_builder": build_prompt_B_C_json},
}


def run_case_variant(case_key: str, variant_key: str, reps: int) -> list[dict]:
    v = VARIANTS[variant_key]
    c = CASES[case_key]
    system = v["system_builder"](case_key)
    user = f"TEXT ADAPTAT:\n{c['adapted']}\n\nGenera la secció de bastides segons la rúbrica."
    print(f"   [{variant_key}] sys={len(system)}ch  ", end="", flush=True)
    rs = []
    for k in range(reps):
        t0 = time.time()
        try:
            raw = _call_llm(v["model"], system, user)
            r = score_run(raw, case_key)
            r["raw"] = raw
        except Exception as e:
            r = {"ok": False, "reason": f"EXCEPCIÓ: {type(e).__name__}: {e}"}
        r["elapsed_s"] = round(time.time() - t0, 1)
        rs.append(r)
        icon = "OK" if r.get("ok") else "FAIL"
        print(f"r{k+1}={icon}({r['elapsed_s']}s)", end=" ", flush=True)
    n_ok = sum(1 for r in rs if r.get("ok"))
    print(f"→ {n_ok}/{reps}")
    return rs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=2)
    ap.add_argument("--only", type=str, default="A,B,C")
    ap.add_argument("--cases", type=str, default="bastides_A1,bastides_B1")
    ap.add_argument("--dump", action="store_true")
    args = ap.parse_args()

    variant_keys = [k.strip().upper() for k in args.only.split(",") if k.strip()]
    case_keys = [k.strip() for k in args.cases.split(",") if k.strip()]

    print(f"\nPILOT BASTIDES 2026-05-31 — JSON vs (descriptiu+directiva Python)")
    print(f"  Casos:    {case_keys}")
    print(f"  Variants: {variant_keys}")
    print(f"  Reps:     {args.reps}")

    all_results: dict = {}
    for case_key in case_keys:
        c = CASES[case_key]
        print(f"\n{'='*72}\n  CAS: {case_key} — {c['label']}\n{'='*72}")
        all_results[case_key] = {}
        for vk in variant_keys:
            all_results[case_key][vk] = run_case_variant(case_key, vk, args.reps)

    print(f"\n{'='*72}\n  RESUM AGREGAT\n{'='*72}")
    totals = {v: [0, 0] for v in variant_keys}
    for case_key in case_keys:
        cells = []
        for vk in variant_keys:
            rs = all_results[case_key][vk]
            n_ok = sum(1 for r in rs if r.get("ok"))
            cells.append(f"{vk}={n_ok}/{len(rs)}")
            totals[vk][0] += n_ok
            totals[vk][1] += len(rs)
        print(f"  {case_key:<18} " + "  ".join(cells))
    print(f"  {'TOTAL':<18} " + "  ".join(f"{vk}={t[0]}/{t[1]}" for vk, t in totals.items()))

    print(f"\n{'='*72}\n  DETALL FALLADES\n{'='*72}")
    any_fail = False
    for case_key in case_keys:
        for vk in variant_keys:
            for i, r in enumerate(all_results[case_key][vk]):
                if not r.get("ok"):
                    any_fail = True
                    print(f"  ✗ {case_key}/{vk}/rep{i+1}: {r['reason']}")
                    if r.get("h3_counts"):
                        print(f"      items: {r['h3_counts']}")
    if not any_fail:
        print("  (cap fallada)")

    if args.dump:
        out = PILOT_DIR / f"resultats_bastides_{int(time.time())}.json"
        dump = {ck: {vk: [{k: v for k, v in r.items() if k != "raw"} for r in rs]
                     for vk, rs in vd.items()}
                for ck, vd in all_results.items()}
        out.write_text(json.dumps(dump, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n[dump] {out}")

    n_total_ok = sum(t[0] for t in totals.values())
    n_total = sum(t[1] for t in totals.values())
    sys.exit(0 if n_total_ok > n_total / 2 else 1)


if __name__ == "__main__":
    main()
