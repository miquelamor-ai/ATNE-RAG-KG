"""Avaluació individual i comparativa via OpenRouter (Llama + Qwen com a jutges)."""
import sqlite3, json, os, sys, time, random
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1")
DB = Path("tests/results/evaluations.db")

EVAL_SYSTEM = """Ets un avaluador pedagògic expert i escèptic. Avalua la qualitat d'una adaptació de text educatiu.

PROCEDIMENT (Chain-of-Thought):
1. Llegeix el text adaptat i identifica 3-5 evidències per criteri.
2. Per cada criteri, raona en 1-2 frases.
3. NOMÉS DESPRÉS, assigna la puntuació.

Criteris (1-5):
C1 COHERÈNCIA: text intern consistent, idees flueixen lògicament, connectors
C2 ADEQUACIÓ AL PERFIL: instruccions del perfil aplicades amb evidència
C3 PRESERVACIÓ CURRICULAR: contingut original mantingut sense omissions
C4 ADEQUACIÓ MECR: lèxic/sintaxi al nivell declarat
C5 PRELLIÇÓ: glossari previ o organitzador cognitiu

Retorna NOMÉS JSON:
{"C1":{"p":1-5,"j":"..."},"C2":{"p":1-5,"j":"..."},"C3":{"p":1-5,"j":"..."},"C4":{"p":1-5,"j":"..."},"C5":{"p":1-5,"j":"..."}}"""

COMP_SYSTEM = """Ets un avaluador pedagògic expert. Reps dos textos adaptats (A i B) del MATEIX original per al MATEIX perfil. Decideix quin és millor.
NO saps quina branca ha generat cada text. Tria A o B o empat. Justifica.
Retorna NOMÉS JSON:
{"global":{"winner":"A/B/empat","confidence":"alta/mitjana/baixa","justification":"..."},
"C1":{"winner":"A/B/empat","j":"..."},"C2":{"winner":"A/B/empat","j":"..."},
"C3":{"winner":"A/B/empat","j":"..."},"C4":{"winner":"A/B/empat","j":"..."},
"C5":{"winner":"A/B/empat","j":"..."}}"""

def call_or(model, system, user):
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role":"system","content":system},{"role":"user","content":user}],
        max_tokens=4096, temperature=0.2)
    raw = resp.choices[0].message.content or ""
    start = raw.find("{"); end = raw.rfind("}")
    if start != -1 and end != -1:
        return json.loads(raw[start:end+1])
    return {}

def run_individual(conn, judge_name, model, run_id):
    rows = conn.execute("""
        SELECT id, cas_id, generator, prompt_mode, text_adaptat, text_original,
               perfils_actius, mecr, dua, text_original_etapa, text_original_genere
        FROM multi_llm_generations
        WHERE run_id=? AND text_adaptat IS NOT NULL AND error IS NULL
        ORDER BY cas_id, generator, prompt_mode
    """, (run_id,)).fetchall()
    total = len(rows)
    for i, r in enumerate(rows, 1):
        existing = conn.execute(
            "SELECT id FROM multi_llm_evaluations WHERE run_id=? AND generation_id=? AND judge=? AND eval_type='individual'",
            (run_id, r["id"], judge_name)).fetchone()
        if existing: continue
        is_self = 1 if r["generator"] == judge_name else 0
        print(f"  [{i:4d}/{total}] {r['cas_id']} [{r['generator']}/{r['prompt_mode']}] jutge={judge_name} ...", end=" ", flush=True)
        user = f"Perfil: {r['perfils_actius']} | MECR: {r['mecr']} | DUA: {r['dua']}\n\nORIGINAL:\n{(r['text_original'] or '')[:1500]}\n\nADAPTAT:\n{(r['text_adaptat'] or '')[:3000]}"
        try:
            result = call_or(model, EVAL_SYSTEM, user)
            scores = {}
            for c in ["C1","C2","C3","C4","C5"]:
                v = result.get(c, {}); scores[c] = {"p": v.get("p",0), "j": v.get("j","")}
            avg = sum(scores[c]["p"] for c in scores if scores[c]["p"]) / max(1, sum(1 for c in scores if scores[c]["p"]))
            print(f"avg={avg:.1f}")
            conn.execute("""INSERT INTO multi_llm_evaluations
                (run_id,cas_id,generation_id,judge,eval_type,c1_coherencia,c1_justificacio,
                 c2_adequacio_perfil,c2_justificacio,c3_preservacio_curricular,c3_justificacio,
                 c4_adequacio_mecr,c4_justificacio,c5_prellico_funcional,c5_justificacio,
                 puntuacio_fons,is_self_eval)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (run_id, r["cas_id"], r["id"], judge_name, "individual",
                 scores["C1"]["p"],scores["C1"]["j"],scores["C2"]["p"],scores["C2"]["j"],
                 scores["C3"]["p"],scores["C3"]["j"],scores["C4"]["p"],scores["C4"]["j"],
                 scores["C5"]["p"],scores["C5"]["j"],round(avg,2),is_self))
            conn.commit()
        except Exception as e:
            print(f"ERR: {str(e)[:50]}")
        time.sleep(2)

def run_comparative(conn, judge_name, model, run_id):
    pairs = conn.execute("""
        SELECT g1.id as hc_id, g1.cas_id, g1.generator, g1.text_adaptat as text_hc,
               g2.id as rag_id, g2.text_adaptat as text_rag,
               g1.text_original, g1.perfils_actius, g1.mecr, g1.dua
        FROM multi_llm_generations g1
        JOIN multi_llm_generations g2 ON g1.cas_id=g2.cas_id AND g1.generator=g2.generator AND g1.run_id=g2.run_id
        WHERE g1.run_id=? AND g1.prompt_mode='hardcoded' AND g2.prompt_mode='rag'
            AND g1.text_adaptat IS NOT NULL AND g2.text_adaptat IS NOT NULL
            AND g1.error IS NULL AND g2.error IS NULL
        ORDER BY g1.cas_id, g1.generator
    """, (run_id,)).fetchall()
    total = len(pairs)
    for i, r in enumerate(pairs, 1):
        existing = conn.execute(
            "SELECT id FROM multi_llm_evaluations WHERE run_id=? AND generation_id=? AND other_generation_id=? AND judge=? AND eval_type='comparative'",
            (run_id, r["hc_id"], r["rag_id"], judge_name)).fetchone()
        if existing: continue
        is_self = 1 if r["generator"] == judge_name else 0
        if random.random() < 0.5:
            text_a, text_b, order = r["text_hc"], r["text_rag"], "hc_first"
        else:
            text_a, text_b, order = r["text_rag"], r["text_hc"], "rag_first"
        print(f"  [{i:4d}/{total}] {r['cas_id']} gen={r['generator']} jutge={judge_name} ...", end=" ", flush=True)
        user = f"Perfil: {r['perfils_actius']} | MECR: {r['mecr']}\n\nORIGINAL:\n{(r['text_original'] or '')[:1000]}\n\nTEXT A:\n{(text_a or '')[:2500]}\n\nTEXT B:\n{(text_b or '')[:2500]}"
        try:
            result = call_or(model, COMP_SYSTEM, user)
            g = result.get("global", {})
            w = g.get("winner", "empat")
            def resolve(winner):
                if not winner or winner == "empat": return "empat"
                if order == "hc_first": return "hardcoded" if winner == "A" else "rag"
                return "rag" if winner == "A" else "hardcoded"
            winner = resolve(w)
            print(f"-> {winner}")
            conn.execute("""INSERT INTO multi_llm_evaluations
                (run_id,cas_id,generation_id,other_generation_id,judge,eval_type,
                 winner,confidence,justification,
                 c1_coherencia,c1_justificacio,c2_adequacio_perfil,c2_justificacio,
                 c3_preservacio_curricular,c3_justificacio,c4_adequacio_mecr,c4_justificacio,
                 c5_prellico_funcional,c5_justificacio,is_self_eval,order_presented)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (run_id, r["cas_id"], r["hc_id"], r["rag_id"], judge_name, "comparative",
                 winner, g.get("confidence",""), g.get("justification",""),
                 resolve(result.get("C1",{}).get("winner","")), result.get("C1",{}).get("j",""),
                 resolve(result.get("C2",{}).get("winner","")), result.get("C2",{}).get("j",""),
                 resolve(result.get("C3",{}).get("winner","")), result.get("C3",{}).get("j",""),
                 resolve(result.get("C4",{}).get("winner","")), result.get("C4",{}).get("j",""),
                 resolve(result.get("C5",{}).get("winner","")), result.get("C5",{}).get("j",""),
                 is_self, order))
            conn.commit()
        except Exception as e:
            print(f"ERR: {str(e)[:50]}")
        time.sleep(2)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--judge", required=True, choices=["llama","qwen"])
    parser.add_argument("--eval-type", required=True, choices=["individual","comparative"])
    parser.add_argument("--run-id", default="multi_v1")
    args = parser.parse_args()

    models = {"llama": "meta-llama/llama-3.3-70b-instruct", "qwen": "qwen/qwen-2.5-72b-instruct"}
    model = models[args.judge]

    conn = sqlite3.connect(str(DB))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")

    print(f"=== {args.judge} ({model}) — {args.eval_type} via OpenRouter ===")
    if args.eval_type == "individual":
        run_individual(conn, args.judge, model, args.run_id)
    else:
        run_comparative(conn, args.judge, model, args.run_id)
    conn.close()
