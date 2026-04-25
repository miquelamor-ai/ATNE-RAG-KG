import os
import re
import json
from collections import defaultdict

base_dir = r"C:\Users\miquel.amor\Documents\GitHub\ATNE\mpv\resultats"
new_directories = [
    os.path.join(base_dir, "nous_20260424_071042"),
    os.path.join(base_dir, "perfils_A_20260424_081018"),
    os.path.join(base_dir, "perfils_A_20260424_092133")
]

stats = []

def get_sentences(text):
    return [s for s in re.split(r'[.!?]+', text) if len(s.strip()) > 3]

def process_file(filepath, filename):
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
        
    pipeline = "MVP" if "MVP" in filename else "CREAM"
    
    model = "Unknown"
    if "gpt_4o" in filename: model = "gpt-4o"
    elif "gpt_4.1_mini" in filename or "gpt-4.1-mini" in filename or "gpt_4_1_mini" in filename: model = "gpt-4.1-mini"
    elif "gemma_3" in filename: model = "gemma-3"
    elif "gemma_4" in filename: model = "gemma-4"
    elif "llama" in filename.lower(): model = "llama"
    elif "mistral" in filename.lower(): model = "mistral"
    elif "qwen" in filename.lower(): model = "qwen"
    elif "sonnet" in filename.lower(): model = "claude-3.5-sonnet"
        
    parts = re.split(r'##\s*(?:Argumentació|Notes\s*d\'auditoria)', content, maxsplit=1, flags=re.IGNORECASE)
    pure_text = parts[0]
    pure_text = re.sub(r'^#\s+.*?\n', '', pure_text)
    pure_text = re.sub(r'\*\*Nivell:\*\*.*?\n', '', pure_text)
    pure_text = pure_text.strip()
    
    sentences = get_sentences(pure_text)
    word_count = len(pure_text.split())
    
    is_tdah = "tdah" in filename.lower()
    is_di = "di_" in filename.lower() or "di." in filename.lower()
    is_aacc = "aacc" in filename.lower()
    is_a1 = "A1" in filename or "_a1_" in filename.lower()
    is_tea = "tea" in filename.lower()
    is_tdl = "tdl" in filename.lower()
    
    tdah_has_section = bool(re.search(r'\[Secció \d+ de \d+\]', pure_text, re.IGNORECASE))
    tea_has_numbers = bool(re.search(r'^\d+\.', pure_text, re.MULTILINE))
    
    di_compliance_pct = 0
    if sentences:
        short_sentences = sum(1 for s in sentences if len(s.split()) <= 8)
        di_compliance_pct = short_sentences / len(sentences)
        
    a1_compliance_pct = 0
    if sentences:
        short_sentences = sum(1 for s in sentences if len(s.split()) <= 10)
        a1_compliance_pct = short_sentences / len(sentences)
        
    bold_count = len(re.findall(r'\*\*.*?\*\*', pure_text))
    
    stats.append({
        "model": model,
        "pipeline": pipeline,
        "is_tdah": is_tdah,
        "is_di": is_di,
        "is_aacc": is_aacc,
        "is_a1": is_a1,
        "is_tea": is_tea,
        "is_tdl": is_tdl,
        "tdah_section": tdah_has_section,
        "tea_numbers": tea_has_numbers,
        "di_pct": di_compliance_pct,
        "a1_pct": a1_compliance_pct,
        "bold_count": bold_count,
        "words": word_count
    })

for d in new_directories:
    if not os.path.exists(d): continue
    for f in os.listdir(d):
        if f.endswith('.md') and "INDEX" not in f:
            process_file(os.path.join(d, f), f)

agg = defaultdict(lambda: {"count": 0, "tdah_sec": 0, "tdah_cnt": 0, "di_pct_sum": 0, "di_cnt": 0, 
                           "a1_pct_sum": 0, "a1_cnt": 0, "aacc_words": [], "tea_num": 0, "tea_cnt": 0})

for s in stats:
    k = f"{s['model']}_{s['pipeline']}"
    agg[k]["count"] += 1
    if s["is_tdah"]:
        agg[k]["tdah_cnt"] += 1
        if s["tdah_section"]: agg[k]["tdah_sec"] += 1
    if s["is_di"]:
        agg[k]["di_cnt"] += 1
        agg[k]["di_pct_sum"] += s["di_pct"]
    if s["is_a1"]:
        agg[k]["a1_cnt"] += 1
        agg[k]["a1_pct_sum"] += s["a1_pct"]
    if s["is_aacc"]:
        agg[k]["aacc_words"].append(s["words"])
    if s["is_tea"]:
        agg[k]["tea_cnt"] += 1
        if s["tea_numbers"]: agg[k]["tea_num"] += 1

result = {}
for k, v in agg.items():
    if v["count"] == 0: continue
    result[k] = {
        "tests": v["count"],
        "TDAH_Seccio_Format": f"{v['tdah_sec']}/{v['tdah_cnt']}",
        "DI_Frases_Curtes_Pct": round((v['di_pct_sum']/v['di_cnt'])*100, 1) if v["di_cnt"] else 0,
        "A1_Frases_Curtes_Pct": round((v['a1_pct_sum']/v['a1_cnt'])*100, 1) if v["a1_cnt"] else 0,
        "AACC_Avg_Words": round(sum(v["aacc_words"])/len(v["aacc_words"])) if v["aacc_words"] else 0,
        "TEA_Format": f"{v['tea_num']}/{v['tea_cnt']}"
    }

with open("scratch_evaluate_output.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2)
