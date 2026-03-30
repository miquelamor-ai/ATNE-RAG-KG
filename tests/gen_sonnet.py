"""Genera 400 adaptacions amb Sonnet via Anthropic SDK (usa credencials Claude Code)."""
import sqlite3, json, sys, time, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

from instruction_filter import get_instructions, format_instructions_for_prompt
from evaluator_metrics import evaluate_forma, retrieval_recall, extract_instruction_ids
import corpus_reader
corpus_reader.load_corpus()

# Load prompt_blocks from git
import subprocess, importlib.util
tmp = Path("tests/.tmp/prompt_blocks.py")
if not tmp.exists():
    r = subprocess.run(["git","show","prompt-v2-hardcoded:prompt_blocks.py"], capture_output=True, text=True)
    if r.returncode == 0: tmp.write_text(r.stdout, encoding="utf-8")
spec = importlib.util.spec_from_file_location("prompt_blocks", str(tmp))
pb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pb)

import anthropic
client = anthropic.Anthropic()

DB = Path("tests/results/evaluations.db")
with open("tests/test_data.json", encoding="utf-8") as f:
    data = json.load(f)

conn = sqlite3.connect(str(DB))
conn.row_factory = sqlite3.Row
conn.execute("PRAGMA journal_mode=WAL")

def flatten(p):
    flat = {"caracteristiques": {}}
    for k, v in p["profile"].get("caracteristiques", {}).items():
        fv = {"actiu": v.get("actiu", True)}
        if "detalls" in v: fv.update(v["detalls"])
        flat["caracteristiques"][k] = fv
    return flat

def detect_comps(text):
    return {
        "te_glossari": 1 if re.search(r"##\s*(Glossari|Paraules clau)", text, re.I) else 0,
        "te_glossari_bilingue": 1 if any(0x0600<=ord(c)<=0x06FF or 0x4E00<=ord(c)<=0x9FFF for c in text) else 0,
        "te_negretes": 1 if len(re.findall(r"\*\*[^*]+\*\*", text)) >= 2 else 0,
        "te_prellico": 1 if re.search(r"##\s*(Paraules|Abans|Objectius)", text, re.I) else 0,
        "te_esquema": 1 if re.search(r"##\s*(Esquema|Mapa)", text, re.I) else 0,
        "te_preguntes": 1 if re.search(r"##\s*Preguntes", text, re.I) else 0,
        "te_argumentacio_pedagogica": 1 if re.search(r"##\s*Argumentaci", text, re.I) else 0,
        "te_auditoria": 1 if re.search(r"##\s*(Notes.*auditoria|Auditoria)", text, re.I) else 0,
    }

run_id = "multi_v1"
generator = "sonnet"
total = len(data["textos"]) * len(data["perfils"]) * 2
i = 0

for t in data["textos"]:
    for p in data["perfils"]:
        for mode in ["hardcoded", "rag"]:
            i += 1
            cas_id = f"{t['id']}__{p['id']}"
            existing = conn.execute(
                "SELECT id FROM multi_llm_generations WHERE run_id=? AND cas_id=? AND generator=? AND prompt_mode=?",
                (run_id, cas_id, generator, mode)
            ).fetchone()
            if existing: continue

            print(f"[{i:4d}/{total}] {cas_id} [{generator}/{mode}]", end=" ", flush=True)
            try:
                params = p["params"]
                mecr = params.get("mecr_sortida", "B2")
                flat = flatten(p)
                active = [k for k,v in flat["caracteristiques"].items() if v.get("actiu")]

                if mode == "hardcoded":
                    parts = [pb.IDENTITY_BLOCK, pb.UNIVERSAL_RULES_BLOCK]
                    if mecr in pb.MECR_BLOCKS: parts.append(pb.MECR_BLOCKS[mecr])
                    dua = params.get("dua","Core")
                    if dua in pb.DUA_BLOCKS: parts.append(pb.DUA_BLOCKS[dua])
                    genre = params.get("genere_discursiu","")
                    if genre and genre in pb.GENRE_BLOCKS: parts.append(pb.GENRE_BLOCKS[genre])
                    for ap in active:
                        if ap in pb.PROFILE_BLOCKS: parts.append(pb.PROFILE_BLOCKS[ap])
                    if mecr in pb.FEWSHOT_EXAMPLES: parts.append(pb.FEWSHOT_EXAMPLES[mecr])
                    system_prompt = "\n\n".join(parts)
                    ids, fstats = [], {}
                else:
                    filtered = get_instructions(flat, params)
                    instr_text = format_instructions_for_prompt(filtered)
                    parts = [corpus_reader.get_identity(), instr_text]
                    dua_block = corpus_reader.get_dua_block(params.get("dua","Core"))
                    if dua_block: parts.append(dua_block)
                    fewshot = corpus_reader.get_fewshot_example(mecr)
                    if fewshot: parts.append(f"EXEMPLE ({mecr}):\n{fewshot}")
                    system_prompt = "\n\n".join(parts)
                    ids = extract_instruction_ids(filtered)
                    fstats = filtered.get("stats", {})

                t0 = time.time()
                resp = client.messages.create(
                    model="claude-sonnet-4-6-20250514",
                    max_tokens=8192,
                    system=system_prompt,
                    messages=[{"role":"user","content":f"Adapta el seguent text educatiu:\n\n{t['text']}"}],
                )
                text_adaptat = resp.content[0].text if resp.content else ""
                elapsed = time.time() - t0

                forma = evaluate_forma(text_adaptat, mecr)
                comps = detect_comps(text_adaptat)
                paraules = len(text_adaptat.split())
                recall, absents = None, None
                if mode == "rag":
                    ret = retrieval_recall(active, ids)
                    recall = ret["recall"]
                    absents = json.dumps(ret.get("absents",[]), ensure_ascii=False)

                conn.execute("""INSERT INTO multi_llm_generations
                    (run_id,cas_id,text_id,perfil_id,generator,prompt_mode,
                     text_original,text_original_tema,text_original_font,
                     text_original_etapa,text_original_genere,text_original_paraules,
                     perfil_nom,perfil_json,perfils_actius,mecr,dua,
                     system_prompt,system_prompt_length,instruction_ids,filter_stats,
                     text_adaptat,text_adaptat_length,text_adaptat_paraules,
                     te_glossari,te_glossari_bilingue,te_negretes,te_prellico,
                     te_esquema,te_preguntes,te_argumentacio_pedagogica,te_auditoria,
                     f1_longitud_frase,f2_titols,f3_negretes,f4_llistes,f5_prellico,
                     puntuacio_forma,recall,instruccions_absents,temps_generacio)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (run_id, cas_id, t["id"], p["id"], generator, mode,
                     t["text"], t.get("tema",""), t.get("font",""),
                     t.get("etapa",""), t.get("genere",""), t.get("paraules",0),
                     p.get("nom",""), json.dumps(p, ensure_ascii=False),
                     json.dumps(active), mecr, params.get("dua","Core"),
                     system_prompt, len(system_prompt),
                     json.dumps(ids, ensure_ascii=False),
                     json.dumps(fstats, ensure_ascii=False),
                     text_adaptat, len(text_adaptat), paraules,
                     comps["te_glossari"], comps["te_glossari_bilingue"],
                     comps["te_negretes"], comps["te_prellico"],
                     comps["te_esquema"], comps["te_preguntes"],
                     comps["te_argumentacio_pedagogica"], comps["te_auditoria"],
                     forma["F1_longitud_frase"], forma["F2_titols"],
                     forma["F3_negretes"], forma["F4_llistes"], forma["F5_prellico_present"],
                     forma["puntuacio_forma"], recall, absents, elapsed))
                conn.commit()
                print(f"{paraules}w {elapsed:.1f}s")
                time.sleep(1)
            except Exception as e:
                print(f"ERROR: {e}")
                conn.execute("INSERT INTO multi_llm_generations (run_id,cas_id,text_id,perfil_id,generator,prompt_mode,error) VALUES (?,?,?,?,?,?,?)",
                    (run_id, cas_id, t["id"], p["id"], generator, mode, str(e)))
                conn.commit()
                time.sleep(2)

n = conn.execute("SELECT COUNT(*) FROM multi_llm_generations WHERE run_id=? AND generator=?", (run_id, generator)).fetchone()[0]
print(f"\nSonnet completat: {n} generacions")
conn.close()
