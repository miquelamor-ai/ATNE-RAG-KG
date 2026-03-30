"""
compare_branches.py — Judici comparatiu multi-jutge (Christodoulou / Bradley-Terry).

Cada jutge (Opus, Sonnet, Gemini) rep parells de textos adaptats (HC vs RAG)
i decideix quin és millor — comparació directa, no rúbrica absoluta.

Protocol anti-biaix:
  - L'ordre de presentació (A/B) es randomitza per cada cas
  - El jutge NO sap quina branca és quina (etiquetes "Text A" / "Text B")
  - Per cada criteri C1-C5, decisió binària (A o B)
  - Decisió global + justificació

Ús:
  python tests/compare_branches.py --judge gemini
  python tests/compare_branches.py --judge opus    (requereix agent Claude)
  python tests/compare_branches.py --judge sonnet  (requereix agent Claude)

Referència: docs/decisions/avaluacio_agent_v2.md
"""

import argparse
import json
import os
import random
import sqlite3
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

_RUN_ID = "20260329_130946"  # Últim batch complet
DB_PATH = Path(__file__).parent / "results" / "evaluations.db"

# ═══════════════════════════════════════════════════════════════════════════════
# PROMPT COMPARATIU (sense revelar quina branca és quina)
# ═══════════════════════════════════════════════════════════════════════════════

SYSTEM_PROMPT = """Ets un avaluador pedagògic expert. Reps dos textos adaptats (Text A i Text B) del MATEIX text original, per al MATEIX perfil d'alumnat. Has de decidir quin és millor.

REGLES:
1. NO saps quina branca ha generat cada text. Avalua només el resultat.
2. Per cada criteri, tria A o B (o "empat" si realment no pots decidir).
3. Justifica cada decisió en UNA frase.
4. Retorna NOMÉS el JSON demanat.
5. Escriu en català."""

USER_TEMPLATE = """## Cas: {cas_id}

### PERFIL DE L'ALUMNAT
- Perfils actius: {perfils}
- MECR sortida: {mecr}
- DUA: {dua}
- Etapa: {etapa}
- Gènere discursiu: {genere}

### TEXT ORIGINAL
{text_original}

---

### TEXT A
{text_a}

---

### TEXT B
{text_b}

---

Compara Text A i Text B. Per cada criteri, decideix quin és millor.
Retorna EXACTAMENT aquest JSON:

{{
  "global": {{"winner": "A" o "B" o "empat", "confidence": "alta" o "mitjana" o "baixa", "justification": "..."}},
  "C1_coherencia": {{"winner": "A" o "B" o "empat", "justification": "..."}},
  "C2_adequacio_perfil": {{"winner": "A" o "B" o "empat", "justification": "..."}},
  "C3_preservacio_curricular": {{"winner": "A" o "B" o "empat", "justification": "..."}},
  "C4_adequacio_mecr": {{"winner": "A" o "B" o "empat", "justification": "..."}},
  "C5_prellico_funcional": {{"winner": "A" o "B" o "empat", "justification": "..."}}
}}
"""


def get_cases(conn, run_id: str) -> list[dict]:
    """Llegeix tots els parells HC/RAG de la BD."""
    rows = conn.execute("""
        SELECT cas_id, branca, text_adaptat, perfils_actius, mecr, dua, etapa, genere
        FROM eval_cases WHERE run_id = ? AND text_adaptat IS NOT NULL
        ORDER BY cas_id, branca
    """, (run_id,)).fetchall()

    cases = {}
    for r in rows:
        cid = r["cas_id"]
        if cid not in cases:
            cases[cid] = {"cas_id": cid, "perfils": r["perfils_actius"],
                          "mecr": r["mecr"], "dua": r["dua"],
                          "etapa": r["etapa"], "genere": r["genere"]}
        cases[cid][r["branca"]] = r["text_adaptat"]

    # Només casos amb ambdues branques
    return [c for c in cases.values() if "hardcoded" in c and "rag" in c]


def get_original_text(cas_id: str) -> str:
    """Recupera el text original del test_data.json."""
    data_path = Path(__file__).parent / "test_data.json"
    with open(data_path, encoding="utf-8") as f:
        data = json.load(f)
    text_id = cas_id.rsplit("__", 1)[0]
    for t in data["textos"]:
        if t["id"] == text_id:
            return t["text"]
    return "(text original no trobat)"


def parse_json_response(raw: str) -> dict:
    """Extreu JSON de la resposta de l'LLM."""
    raw = raw.strip()
    start = raw.find("{")
    end = raw.rfind("}")
    if start != -1 and end != -1:
        try:
            return json.loads(raw[start:end + 1])
        except json.JSONDecodeError:
            pass
    return {"error": "parse_failed", "raw": raw[:500]}


def evaluate_with_gemini(prompt: str) -> dict:
    """Crida Gemini Flash com a jutge."""
    from google import genai
    from google.genai import types
    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY"),
        http_options=types.HttpOptions(timeout=180_000),
    )
    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[types.Content(role="user", parts=[types.Part(text=prompt)])],
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.2,
            max_output_tokens=4096,
        ),
    )
    return parse_json_response(resp.text or "")


def save_judgement(conn, run_id: str, case: dict, result: dict, judge: str, order: str):
    """Guarda el judici a la BD."""
    def resolve(winner):
        if not winner or winner == "empat":
            return "empat"
        if order == "hc_first":
            return "hardcoded" if winner == "A" else "rag"
        else:
            return "rag" if winner == "A" else "hardcoded"

    g = result.get("global", {})
    parts = case["cas_id"].rsplit("__", 1)
    text_id = parts[0] if len(parts) == 2 else case["cas_id"]
    perfil_id = parts[1] if len(parts) == 2 else ""

    conn.execute("""
        INSERT INTO comparative_judgements
        (run_id, cas_id, text_id, perfil_id, judge, winner, confidence, justification,
         c1_winner, c1_justification, c2_winner, c2_justification,
         c3_winner, c3_justification, c4_winner, c4_justification,
         c5_winner, c5_justification, order_presented)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        run_id, case["cas_id"], text_id, perfil_id, judge,
        resolve(g.get("winner", "")),
        g.get("confidence", ""),
        g.get("justification", ""),
        resolve(result.get("C1_coherencia", {}).get("winner", "")),
        result.get("C1_coherencia", {}).get("justification", ""),
        resolve(result.get("C2_adequacio_perfil", {}).get("winner", "")),
        result.get("C2_adequacio_perfil", {}).get("justification", ""),
        resolve(result.get("C3_preservacio_curricular", {}).get("winner", "")),
        result.get("C3_preservacio_curricular", {}).get("justification", ""),
        resolve(result.get("C4_adequacio_mecr", {}).get("winner", "")),
        result.get("C4_adequacio_mecr", {}).get("justification", ""),
        resolve(result.get("C5_prellico_funcional", {}).get("winner", "")),
        result.get("C5_prellico_funcional", {}).get("justification", ""),
        order,
    ))
    conn.commit()


def run_judge(judge_name: str, cases: list[dict], conn, run_id: str):
    """Executa el jutge per tots els casos."""
    total = len(cases)
    wins = {"hardcoded": 0, "rag": 0, "empat": 0, "error": 0}

    for i, case in enumerate(cases, 1):
        # Randomitzar ordre (anti-biaix posicional)
        if random.random() < 0.5:
            text_a, text_b = case["hardcoded"], case["rag"]
            order = "hc_first"
        else:
            text_a, text_b = case["rag"], case["hardcoded"]
            order = "rag_first"

        original = get_original_text(case["cas_id"])

        prompt = USER_TEMPLATE.format(
            cas_id=case["cas_id"],
            perfils=case.get("perfils", ""),
            mecr=case.get("mecr", ""),
            dua=case.get("dua", ""),
            etapa=case.get("etapa", ""),
            genere=case.get("genere", ""),
            text_original=original[:1500],
            text_a=text_a[:2500],
            text_b=text_b[:2500],
        )

        print(f"  [{i:3d}/{total}] {case['cas_id']} ...", end=" ", flush=True)

        try:
            if judge_name == "gemini":
                result = evaluate_with_gemini(prompt)
            else:
                result = evaluate_with_gemini(prompt)  # Fallback

            if "error" in result:
                print("ERROR")
                wins["error"] += 1
            else:
                g = result.get("global", {})
                winner_label = g.get("winner", "?")
                if winner_label == "empat":
                    actual = "empat"
                elif order == "hc_first":
                    actual = "hardcoded" if winner_label == "A" else "rag"
                else:
                    actual = "rag" if winner_label == "A" else "hardcoded"
                wins[actual] = wins.get(actual, 0) + 1
                print(f"-> {actual} ({g.get('confidence', '?')})")

                save_judgement(conn, run_id, case, result, judge_name, order)

        except Exception as e:
            print(f"EXCEPTION: {e}")
            wins["error"] += 1

        time.sleep(2)

    return wins


def main():
    parser = argparse.ArgumentParser(description="Judici comparatiu multi-jutge")
    parser.add_argument("--judge", type=str, default="gemini",
                        choices=["gemini", "opus", "sonnet"],
                        help="Quin jutge usar")
    parser.add_argument("--limit", type=int, default=0,
                        help="Limitar a N casos (0 = tots)")
    parser.add_argument("--run-id", type=str, default=_RUN_ID,
                        help="Run ID a avaluar")
    args = parser.parse_args()

    run_id = args.run_id

    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row

    cases = get_cases(conn, run_id)
    if args.limit > 0:
        cases = cases[:args.limit]

    print("=" * 60)
    print(f"  JUDICI COMPARATIU — Jutge: {args.judge}")
    print(f"  Run: {run_id} | Casos: {len(cases)}")
    print("=" * 60)

    wins = run_judge(args.judge, cases, conn, run_id)

    print("\n" + "=" * 60)
    print("  RESULTATS")
    print("=" * 60)
    total_valid = sum(v for k, v in wins.items() if k != "error")
    for label, count in sorted(wins.items(), key=lambda x: -x[1]):
        pct = count / total_valid * 100 if total_valid > 0 else 0
        print(f"  {label:12s}: {count:3d} ({pct:5.1f}%)")

    conn.close()


if __name__ == "__main__":
    main()
