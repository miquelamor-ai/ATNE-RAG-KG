"""Pilot 2026-05-31 — JSON estructurat vs prompt descriptiu per a glossari.

Decisió arquitectònica oberta del 31/05: A (reescriptura M3 imperatiu) vs B
(compilador descriptiu→imperatiu) vs C (rúbrica JSON). Aquest pilot dona dades
empíriques sobre C amb 2 models diferents (GPT-4o de pagament + Gemma 4 free)
sobre MÚLTIPLES casos i nivells MECR.

Casos:
  1. titella  — receptari A1 + dislèxia + primària 1r (cas border, fallback esperat o ≤2 termes)
  2. fotosintesi — ciències A2 + ESO 1r (cas density-lexical, taula 8-10 termes esperada)
  3. democracia — història B1 + ESO 4t (cas noms propis + termes curriculars, taula 10-12)

Variants per cas:
  A · GPT-4o + prompt actual (descriptiu via prompt_adapter.md)  — baseline
  B · GPT-4o + JSON estructurat (rubrica_glossari.json)          — C amb GPT
  C · Gemma 4 + JSON estructurat                                 — C multi-model

Per defecte: 2 reps cada (variant × cas) → 18 crides totals.

Mètrica per cas:
  - PASS = (cap mot quotidià de la llista override) AND (cap castellanisme)
           AND (nombre termes en rang min-max del nivell o fallback canònic)
  - termes generats
  - secció ## Glossari extreta per a inspecció

Ús:
  python tests/pilot_glossari_2026_05_31/pilot.py
  python tests/pilot_glossari_2026_05_31/pilot.py --reps 3
  python tests/pilot_glossari_2026_05_31/pilot.py --only B,C --cases fotosintesi
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


# ── Configuració ──────────────────────────────────────────────────────────

PILOT_DIR = Path(__file__).resolve().parent
RUBRICA_JSON_PATH = PILOT_DIR / "rubrica_glossari.json"

# Llistes de detecció de fallades (compartides entre tots els casos)
# NOTA: només mots ESPECÍFICAMENT castellans, no els que coincideixen amb català.
# "planta" està compartit (CA=ES) — fora.
GENERIC_CASTELLANISMES = {
    # Cas titella (manualitats)
    "muñeco", "muñeca", "calcetín", "calcetin", "calcetines",
    "agujas", "aguja", "hilo", "boton", "botones",
    "rotulador", "trapo", "juguete", "jugar con él",
    # Cas fotosíntesi (ciències)
    "fotosíntesis", "fotosintesis",  # castellà ≠ català "fotosíntesi"
    "raíz", "raices", "raiz",        # castellà ≠ català "arrel/arrels"
    "hojas",                          # castellà ≠ català "fulles"
    "luz solar",                      # castellà ≠ català "llum del sol"
    # Cas democracia (història)
    "democracia ateniense",           # castellà ≠ català "democràcia atenenca"
    "voto", "votación", "votaciones", # castellà ≠ català "vot/votació"
    "pueblo",                         # castellà ≠ català "poble"
    "asamblea",                       # castellà ≠ català "assemblea"
}

# Termes "soroll" que poden colar-se del format taula (capçaleres) — el test
# els ha de descartar abans de comptar termes reals
HEADER_TERMS_NOISE = {"termes", "terme", "term", "explicació", "explicacio",
                      "traducció", "traduccio", "definició", "definicio",
                      "l1", "l1 (español)", "l1 (català)"}

# ── CASOS ─────────────────────────────────────────────────────────────────

CASES = {
    "titella": {
        "label": "Receptari titella · A1 · dislèxia · 1r primària (cas border)",
        "profile": {
            "caracteristiques": {
                "dislexia": {"actiu": True, "grau": "moderat"},
            },
        },
        "context": {"etapa": "Primària", "materia": "manualitats", "curs": "1r"},
        "params": {
            "mecr_sortida": "A1",
            "dua": "Core",
            "genere_discursiu": "receptari",
            "lang": "ca",
            "complements": {"glossari": True},
        },
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
Pots fer-li veu i jugar amb ell.
""",
        # Mots quotidians ESPECÍFICS d'aquest cas (text manualitats domèstiques).
        "quotidianes_local": {
            "mitja", "botó", "botons", "agulla", "agulles", "fil",
            "retolador", "vella", "ulls", "boca", "cap", "veu", "farciment",
        },
        "expectativa": "fallback OR ≤2 termes (titella, farciment-borderline)",
    },

    "fotosintesi": {
        "label": "Ciències fotosíntesi · A2 · ESO 1r (densitat lèxica alta)",
        "profile": {
            "caracteristiques": {
                "nouvingut": {"actiu": True, "L1": "àrab"},
            },
        },
        "context": {"etapa": "ESO", "materia": "ciències naturals", "curs": "1r"},
        "params": {
            "mecr_sortida": "A2",
            "dua": "Core",
            "genere_discursiu": "divulgatiu",
            "lang": "ca",
            "complements": {"glossari": True},
        },
        "adapted": """# La fotosíntesi de les plantes

Les plantes fan el seu propi menjar. Aquest procés es diu fotosíntesi.

Per fer la fotosíntesi, les plantes necessiten tres coses:
- Llum del sol
- Aigua
- Diòxid de carboni de l'aire

Les fulles són on passa la fotosíntesi. Tenen una substància verda anomenada clorofil·la. La clorofil·la captura la llum del sol.

L'aigua entra per les arrels. El diòxid de carboni entra per uns forats petits a les fulles, anomenats estomes.

Amb aquests tres ingredients, la planta fa glucosa. La glucosa és com el sucre que dona energia a la planta. Com a residu, la planta allibera oxigen a l'aire.

Per això les plantes són tan importants: ens donen l'oxigen que respirem.
""",
        # Per a ESO 1r A2 amb nouvingut, ningun objecte domèstic ni part del cos
        # apareix com a terme rellevant. Aquí cap mot quotidià hauria d'aparèixer.
        "quotidianes_local": set(),
        # Termes que SÍ esperem (tècnics del text):
        "termes_esperats_minim_3": {"fotosíntesi", "clorofil·la", "estomes", "glucosa", "diòxid de carboni"},
        "expectativa": "taula 8-10 termes amb fotosíntesi/clorofil·la/estomes/glucosa, columna L1 àrab",
    },

    "democracia": {
        "label": "Història democràcia atenenca · B1 · ESO 4t (noms propis + termes curriculars)",
        "profile": {
            "caracteristiques": {
                "tdah": {"actiu": True, "grau": "lleu"},
            },
        },
        "context": {"etapa": "ESO", "materia": "història", "curs": "4t"},
        "params": {
            "mecr_sortida": "B1",
            "dua": "Core",
            "genere_discursiu": "divulgatiu",
            "lang": "ca",
            "complements": {"glossari": True},
        },
        "adapted": """# La democràcia atenenca

Atenes va ser la primera ciutat on hi va haver democràcia. Va passar al segle V abans de Crist.

La paraula democràcia ve del grec: "demos" vol dir poble i "kratos" vol dir poder. És a dir, "el poder del poble".

A la democràcia atenenca, els ciutadans es reunien a l'àgora, la plaça pública. Allà debatien les lleis i feien votacions. Cada ciutadà podia donar la seva opinió.

Però atenció: no tothom era ciutadà. Només els homes adults nascuts a Atenes podien votar. Les dones, els esclaus i els estrangers (anomenats metecs) no tenien drets polítics.

La màxima institució era l'eclèsia, una assemblea on tots els ciutadans podien participar. També hi havia un consell anomenat bulé, format per 500 ciutadans escollits per sorteig cada any.

Polítics famosos com Pèricles van impulsar reformes per fer més justa la democràcia. Per exemple, va introduir el misthos: pagar als ciutadans pobres perquè poguessin assistir a l'assemblea sense perdre el sou.
""",
        # Per a B1 ESO 4t, no esperem que cap mot quotidià surti com a terme.
        # Atenció: els noms propis (Atenes, Pèricles) NO han de sortir com a terme
        # de glossari segons la regla, però són CLAUS per a la matèria — pot ser un
        # cas border. La regla diu "excepte si és clau per a la matèria".
        "quotidianes_local": set(),
        "termes_esperats_minim_4": {"democràcia", "àgora", "eclèsia", "bulé", "metecs", "misthos"},
        "expectativa": "taula 10-12 termes amb conceptes polítics grecs",
    },
}


# ── Construcció dels system prompts ───────────────────────────────────────

def build_prompt_A_descriptiu(case_key: str) -> str:
    """Variant A — system prompt actual (re-usa build_complements_prompt)."""
    import os
    os.environ["ATNE_USE_SKILLS"] = "true"
    os.environ["ATNE_USE_PROMPT_ADAPTER"] = "true"
    c = CASES[case_key]
    return build_complements_prompt(c["profile"], c["context"], c["params"])


def build_prompt_B_C_json(case_key: str) -> str:
    """Variants B i C — system prompt JSON-driven, minimal i imperatiu."""
    c = CASES[case_key]
    rubrica = json.loads(RUBRICA_JSON_PATH.read_text(encoding="utf-8"))

    mecr = c["params"]["mecr_sortida"]
    lang = c["params"].get("lang", "ca")
    etapa = c["context"].get("etapa", "")
    curs = c["context"].get("curs", "")
    L1 = c["profile"].get("caracteristiques", {}).get("nouvingut", {}).get("L1", "")
    nivell_data = rubrica["levels"].get(mecr, {})
    override = rubrica["case_overrides"]["A1_primaria_inicial_vocabulari_quotidia"]

    override_actiu = (
        mecr in override["trigger"]["mecr_in"]
        and etapa in override["trigger"]["etapa_in"]
        and curs in override["trigger"]["curs_in_inicial"]
    )

    L1_hint = (
        f"\nL1 de l'alumne: {L1}. Inclou columna `Traducció (L1)` a la taula amb la traducció en alfabet original."
        if L1 else ""
    )

    max_per_nivell = nivell_data.get("seleccio", {}).get("max_terms", 8)
    min_per_nivell = nivell_data.get("seleccio", {}).get("min_terms", 5)
    max_terms_efectiu = override["max_terms_si_aplica"] if override_actiu else max_per_nivell
    max_paraules_def = nivell_data.get("definicio", {}).get("max_paraules", 8)

    prompt = f"""Ets un generador de glossari per a textos educatius adaptats.

REPS un text ja adaptat. GENERA NOMÉS la secció `## Glossari` (cap altra secció,
cap pròleg, cap epíleg). Llengua de sortida: català.{L1_hint}

REGLES (rúbrica estructurada — segueix-les literalment, no parafrasegis):

```json
{json.dumps({
    "nivell_actiu": mecr,
    "etapa": etapa,
    "curs": curs,
    "lang": lang,
    "L1": L1 or None,
    "constraints_nivell": nivell_data,
    "override_aplicable": override_actiu,
    "override_definicio": override if override_actiu else None,
    "transversals": rubrica["transversals"],
}, ensure_ascii=False, indent=2)}
```

PROCEDIMENT OBLIGATORI (no t'ho saltis):

1. Identifica candidats: paraules del text que un alumne de {mecr} probablement NO coneix.
2. Filtra: descarta tot terme que aparegui a `override_definicio.exclude_categories.*`
   (objectes_domestics, parts_cos, verbs_accio_basics) si `override_aplicable=true`.
3. Filtra: descarta connectors i noms propis no curriculars (Pèricles SÍ — clau matèria; Maria NO).
4. Si després del filtre queden ZERO termes nous, escriu NOMÉS:
   `## Glossari\\n\\n{override["fallback_si_zero_termes_nous"]}`
   i atura't.
5. Si queden termes vàlids, selecciona entre {min_per_nivell} i {max_terms_efectiu} segons rellevància.
6. Construeix la taula segons `constraints_nivell.format`.
7. Per cada definició: max {max_paraules_def} paraules, en català, SENSE cap mot d'altra llengua
   (mai "muñeco", "calcetín", "rotulador", "raíz", etc.).
8. El terme MAI apareix dins la seva pròpia definició.

OUTPUT: només la secció markdown `## Glossari` (taula o nota fallback). Res més."""
    return prompt


# ── Extractors i scorer ────────────────────────────────────────────────────

def extract_glossari_section(text: str) -> str | None:
    m = re.search(r"^## Glossari\b[^\n]*$", text, re.MULTILINE | re.IGNORECASE)
    if not m:
        return None
    nxt = re.search(r"^## ", text[m.end():], re.MULTILINE)
    end = m.end() + nxt.start() if nxt else len(text)
    return text[m.start():end]


def extract_glossary_terms(section: str) -> list[str]:
    """Extrau els termes de la 1a columna del glossari.

    Detecta 3 formats possibles:
      1) Taula markdown amb pipes (A1+)
      2) Llista emoji+negreta (pre-A1)
      3) Format vertical jerarquitzat amb capçaleres H3 (algunes generacions A2)
    """
    terms = []

    # Format 1: taula markdown
    in_table_data = False
    for line in section.splitlines():
        line = line.strip()
        if not line.startswith("|") or "|" not in line[1:]:
            in_table_data = False
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        t = cells[0].strip()
        # Separador ----
        if re.match(r"^[-:\s]+$", t):
            in_table_data = True
            continue
        # Capçalera o noise
        if t.lower() in HEADER_TERMS_NOISE:
            continue
        t = re.sub(r"[*_`]", "", t).strip().lower()
        t = re.sub(r"^[^\w\s]+\s*", "", t).strip()
        if t and t not in HEADER_TERMS_NOISE:
            terms.append(t)

    # Format 3: H3 com a termes (alguns generadors A2 sense taula)
    if not terms:
        for line in section.splitlines():
            m = re.match(r"^###\s+(.+)$", line.strip())
            if m:
                t = m.group(1).strip().lower()
                t = re.sub(r"[*_`]", "", t).strip()
                t = re.sub(r"^[^\w\s]+\s*", "", t).strip()
                if t and t not in HEADER_TERMS_NOISE and t != "glossari":
                    terms.append(t)

    # Format 2: llista emoji+negreta (pre-A1)
    if not terms:
        for line in section.splitlines():
            m = re.search(r"\*\*([^\*]+)\*\*", line)
            if m:
                t = m.group(1).strip().lower()
                t = re.sub(r"^[^\w\s]+\s*", "", t).strip()
                if t and t not in HEADER_TERMS_NOISE and t != "glossari":
                    terms.append(t)

    return terms


def detect_castellanismes(section: str, case_key: str) -> list[str]:
    sl = section.lower()
    found = []
    # Genèrics aplicables a tots els casos
    for cw in GENERIC_CASTELLANISMES:
        if re.search(rf"\b{re.escape(cw)}\b", sl):
            found.append(cw)
    return found


def score_run(raw_output: str, case_key: str) -> dict:
    c = CASES[case_key]
    clean = _post_process_llm_output(clean_gemini_output(raw_output), lang=c["params"].get("lang", "ca"))
    section = extract_glossari_section(clean)
    if section is None:
        return {"ok": False, "reason": "secció ## Glossari ABSENT", "terms": [], "n_terms": 0}
    if "no necessita glossari nou" in section.lower():
        # Fallback canònic — vàlid SOLS si el cas l'espera (titella)
        ok = case_key == "titella"
        reason = "FALLBACK (nota sense taula)" if ok else "FALLBACK incorrecte (el cas espera taula)"
        return {"ok": ok, "reason": reason, "terms": [], "n_terms": 0,
                "section": section, "fallback": True}
    terms = extract_glossary_terms(section)
    quotidianes = sorted(t for t in terms if t in c.get("quotidianes_local", set()))
    castellanismes = detect_castellanismes(section, case_key)

    # Validació de rang segons nivell
    rubrica = json.loads(RUBRICA_JSON_PATH.read_text(encoding="utf-8"))
    mecr = c["params"]["mecr_sortida"]
    nivell_data = rubrica["levels"].get(mecr, {})
    sel = nivell_data.get("seleccio", {})
    min_t = sel.get("min_terms", 0)
    # Override pot reduir el max a 2; si actiu, deixem 1-2 termes vàlids
    override = rubrica["case_overrides"]["A1_primaria_inicial_vocabulari_quotidia"]
    override_actiu = (
        mecr in override["trigger"]["mecr_in"]
        and c["context"].get("etapa", "") in override["trigger"]["etapa_in"]
        and c["context"].get("curs", "") in override["trigger"]["curs_in_inicial"]
    )
    max_t = override["max_terms_si_aplica"] if override_actiu else sel.get("max_terms", 999)
    if override_actiu:
        min_t = 1  # admetem 1-2 si override
    rang_ok = min_t <= len(terms) <= max_t

    ok = (not quotidianes) and (not castellanismes) and rang_ok
    reasons = []
    if quotidianes:
        reasons.append(f"quotidianes={quotidianes}")
    if castellanismes:
        reasons.append(f"castellanismes={castellanismes}")
    if not rang_ok:
        reasons.append(f"rang_fora={len(terms)} (esperat {min_t}-{max_t})")
    return {
        "ok": ok,
        "reason": "OK" if ok else "; ".join(reasons),
        "n_terms": len(terms),
        "terms": terms,
        "quotidianes": quotidianes,
        "castellanismes": castellanismes,
        "rang_esperat": [min_t, max_t],
        "section": section,
    }


# ── Variants ──────────────────────────────────────────────────────────────

VARIANTS = {
    "A": {"label": "GPT-4o + descriptiu (baseline)", "model": "gpt-4o",
          "system_builder": build_prompt_A_descriptiu},
    "B": {"label": "GPT-4o + JSON",                  "model": "gpt-4o",
          "system_builder": build_prompt_B_C_json},
    "C": {"label": "Gemma 4 + JSON",                 "model": "gemma4",
          "system_builder": build_prompt_B_C_json},
}


def run_case_variant(case_key: str, variant_key: str, reps: int) -> list[dict]:
    v = VARIANTS[variant_key]
    c = CASES[case_key]
    system = v["system_builder"](case_key)
    user = f"TEXT ADAPTAT:\n{c['adapted']}\n\nGenera la secció ## Glossari segons la rúbrica."
    print(f"   [{variant_key}] sys={len(system)}ch  ", end="", flush=True)
    rs = []
    for k in range(reps):
        t0 = time.time()
        try:
            raw = _call_llm(v["model"], system, user)
            r = score_run(raw, case_key)
            r["raw"] = raw
        except Exception as e:
            r = {"ok": False, "reason": f"EXCEPCIÓ: {type(e).__name__}: {e}",
                 "terms": [], "n_terms": 0}
        r["elapsed_s"] = round(time.time() - t0, 1)
        rs.append(r)
        icon = "OK" if r.get("ok") else "FAIL"
        print(f"r{k+1}={icon}({r['elapsed_s']}s)", end=" ", flush=True)
    n_ok = sum(1 for r in rs if r.get("ok"))
    print(f"→ {n_ok}/{reps}")
    return rs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=2, help="reps per (cas × variant) (default 2)")
    ap.add_argument("--only", type=str, default="A,B,C", help="variants (default A,B,C)")
    ap.add_argument("--cases", type=str, default="titella,fotosintesi,democracia",
                    help="casos (default tots)")
    ap.add_argument("--dump", action="store_true", help="dumpa resultats a fitxer")
    args = ap.parse_args()

    variant_keys = [k.strip().upper() for k in args.only.split(",") if k.strip()]
    case_keys = [k.strip().lower() for k in args.cases.split(",") if k.strip()]
    for k in variant_keys:
        if k not in VARIANTS:
            print(f"ERROR: variant '{k}' desconeguda", file=sys.stderr); sys.exit(2)
    for k in case_keys:
        if k not in CASES:
            print(f"ERROR: cas '{k}' desconegut", file=sys.stderr); sys.exit(2)

    print(f"\nPILOT 2026-05-31 ampliat — JSON vs descriptiu, multi-cas multi-model")
    print(f"  Casos:    {case_keys}")
    print(f"  Variants: {variant_keys}")
    print(f"  Reps:     {args.reps}")
    print(f"  Total crides: {len(case_keys) * len(variant_keys) * args.reps}")

    all_results: dict = {}
    for case_key in case_keys:
        c = CASES[case_key]
        print(f"\n{'='*72}\n  CAS: {case_key} — {c['label']}\n  Esperat: {c['expectativa']}\n{'='*72}")
        all_results[case_key] = {}
        for vk in variant_keys:
            all_results[case_key][vk] = run_case_variant(case_key, vk, args.reps)

    # ── Resum agregat ─────────────────────────────────────────────────────
    print(f"\n{'='*72}\n  RESUM AGREGAT (PASS / TOTAL)\n{'='*72}")
    header = f"  {'CAS':<14}" + " ".join(f"{v:>14}" for v in variant_keys) + "  | termes (mitja)"
    print(header)
    print("  " + "-" * (len(header) - 2))
    totals_per_variant = {v: [0, 0] for v in variant_keys}
    for case_key in case_keys:
        cells = []
        terms_per_v = []
        for vk in variant_keys:
            rs = all_results[case_key][vk]
            n_ok = sum(1 for r in rs if r.get("ok"))
            avg_t = sum(r.get("n_terms", 0) for r in rs) / max(1, len(rs))
            cells.append(f"{n_ok}/{len(rs)}")
            terms_per_v.append(f"{vk}={avg_t:.1f}")
            totals_per_variant[vk][0] += n_ok
            totals_per_variant[vk][1] += len(rs)
        print(f"  {case_key:<14}" + " ".join(f"{c:>14}" for c in cells) + "  | " + " ".join(terms_per_v))
    print("  " + "-" * (len(header) - 2))
    cells_total = []
    for vk in variant_keys:
        n, t = totals_per_variant[vk]
        cells_total.append(f"{n}/{t}")
    print(f"  {'TOTAL':<14}" + " ".join(f"{c:>14}" for c in cells_total))

    # ── Detall fallades ───────────────────────────────────────────────────
    print(f"\n{'='*72}\n  DETALL FALLADES\n{'='*72}")
    any_fail = False
    for case_key in case_keys:
        for vk in variant_keys:
            for i, r in enumerate(all_results[case_key][vk]):
                if not r.get("ok"):
                    any_fail = True
                    print(f"  ✗ {case_key}/{vk}/rep{i+1}: {r['reason']}")
                    if r.get("terms"):
                        print(f"      termes: {r['terms']}")
    if not any_fail:
        print("  (cap fallada)")

    if args.dump:
        out_path = PILOT_DIR / f"resultats_multicas_{int(time.time())}.json"
        dump = {}
        for ck, vd in all_results.items():
            dump[ck] = {vk: [{k: v for k, v in r.items() if k != "raw"} for r in rs]
                        for vk, rs in vd.items()}
        out_path.write_text(json.dumps(dump, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n[dump] resultats desats a {out_path}")

    n_ok_total = sum(t[0] for t in totals_per_variant.values())
    n_total = sum(t[1] for t in totals_per_variant.values())
    sys.exit(0 if n_ok_total > n_total / 2 else 1)


if __name__ == "__main__":
    main()
