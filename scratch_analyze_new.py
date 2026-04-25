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
    return [s for s in re.split(r'[.!?]+', text) if len(s.strip()) > 5]

def process_file(filepath, filename):
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
        
    pipeline = "MVP" if "MVP" in filename else "CREAM"
    
    model = "Unknown"
    if "gpt_4o" in filename:
        model = "gpt-4o"
    elif "gpt_4.1_mini" in filename or "gpt-4.1-mini" in filename or "gpt_4_1_mini" in filename:
        model = "gpt-4.1-mini"
    elif "gemma_3" in filename:
        model = "gemma-3-27b"
    elif "gemma_4" in filename:
        model = "gemma-4-31b"
    elif "llama" in filename.lower():
        model = "llama"
    elif "mistral" in filename.lower():
        model = "mistral"
    elif "qwen" in filename.lower():
        model = "qwen"
        
    parts = re.split(r'##\s*(?:Argumentació|Notes\s*d\'auditoria)', content, maxsplit=1, flags=re.IGNORECASE)
    pure_text = parts[0]
    
    # Strip headers if present
    pure_text = re.sub(r'^#\s+.*?\n', '', pure_text)
    pure_text = re.sub(r'\*\*Nivell:\*\*.*?\n', '', pure_text)
    pure_text = pure_text.strip()
    
    word_count = len(pure_text.split())
    sentences = get_sentences(pure_text)
    avg_sentence_len = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
    
    h2_count = len(re.findall(r'^##\s+', pure_text, re.MULTILINE))
    bold_count = len(re.findall(r'\*\*.*?\*\*', pure_text))
    bullet_count = len(re.findall(r'^[-*]\s+', pure_text, re.MULTILINE))
    
    has_pedagogy = "Argumentació pedagògica" in content
    has_audit = "Notes d'auditoria" in content
    
    stats.append({
        "pipeline": pipeline,
        "model": model,
        "words": word_count,
        "avg_sentence_len": avg_sentence_len,
        "h2": h2_count,
        "bold": bold_count,
        "bullet": bullet_count,
        "pedagogy": 1 if has_pedagogy else 0,
        "audit": 1 if has_audit else 0
    })

for d in new_directories:
    if not os.path.exists(d):
        continue
    for f in os.listdir(d):
        if f.endswith('.md') and "INDEX" not in f:
            process_file(os.path.join(d, f), f)

# Aggregate by model + pipeline
agg = defaultdict(lambda: {"count": 0, "words": [], "slen": [], "h2": [], "bold": [], "bullet": [], "pedagogy": 0, "audit": 0})

for s in stats:
    key = f"{s['model']}_{s['pipeline']}"
    agg[key]["count"] += 1
    agg[key]["words"].append(s["words"])
    agg[key]["slen"].append(s["avg_sentence_len"])
    agg[key]["h2"].append(s["h2"])
    agg[key]["bold"].append(s["bold"])
    agg[key]["bullet"].append(s["bullet"])
    agg[key]["pedagogy"] += s["pedagogy"]
    agg[key]["audit"] += s["audit"]

result = {}
for k, v in agg.items():
    c = v["count"]
    result[k] = {
        "tests_count": c,
        "avg_words": round(sum(v["words"])/c, 1) if c else 0,
        "avg_sentence_len": round(sum(v["slen"])/c, 1) if c else 0,
        "avg_h2": round(sum(v["h2"])/c, 1) if c else 0,
        "avg_bold": round(sum(v["bold"])/c, 1) if c else 0,
        "avg_bullet": round(sum(v["bullet"])/c, 1) if c else 0,
        "pedagogy_compliance": f"{round((v['pedagogy']/c)*100)}%" if c else "0%",
        "audit_compliance": f"{round((v['audit']/c)*100)}%" if c else "0%"
    }

print(json.dumps(result, indent=2))
