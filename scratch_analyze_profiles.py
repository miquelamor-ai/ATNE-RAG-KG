import os
import re
import json
from collections import defaultdict

base_dir = r"C:\Users\miquel.amor\Documents\GitHub\ATNE\mpv\resultats"

directories = [
    os.path.join(base_dir, "complet_20260423_232822"),
    os.path.join(base_dir, "nous_20260424_061819"),
    os.path.join(base_dir, "perfils_A_20260424_062851")
]

stats = []

def get_sentences(text):
    # Very basic sentence splitting
    return [s for s in re.split(r'[.!?]+', text) if len(s.strip()) > 5]

def process_file(filepath, filename):
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
        
    pipeline = "MVP" if "MVP" in filename else "CREAM"
    
    # Extract profile from filename. It's usually after the model name.
    # Actually, we can just look at the filename parts or the first line of the file.
    # Let's extract from the first line like "# gpt-4o · aacc · CREAM"
    lines = content.strip().split('\n')
    header = lines[0] if lines else ""
    profile = "Unknown"
    
    if "·" in header:
        parts = [p.strip() for p in header.split("·")]
        if len(parts) >= 2:
            profile = parts[1]
            
    # Extract level from the second line "**Nivell:** A1 | ..."
    level = "Unknown"
    for line in lines[:5]:
        if "**Nivell:**" in line:
            m = re.search(r'\*\*Nivell:\*\*\s*([A-C][1-2])', line)
            if m:
                level = m.group(1)
                break
                
    parts = re.split(r'##\s*(?:Argumentació|Notes\s*d\'auditoria)', content, maxsplit=1, flags=re.IGNORECASE)
    pure_text = parts[0].replace(header, "") # Remove header
    pure_text = re.sub(r'\*\*Nivell:\*\*.*?\n', '', pure_text) # Remove metadata line
    pure_text = pure_text.strip()
    
    word_count = len(pure_text.split())
    sentences = get_sentences(pure_text)
    avg_sentence_len = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
    
    stats.append({
        "pipeline": pipeline,
        "profile": profile,
        "level": level,
        "words": word_count,
        "avg_sentence_len": avg_sentence_len
    })

for f in os.listdir(base_dir):
    if f.startswith("20260423_232045_") and f.endswith(".md") and "INDEX" not in f:
        process_file(os.path.join(base_dir, f), f)

for d in directories:
    if not os.path.exists(d):
        continue
    for f in os.listdir(d):
        if f.endswith('.md') and "INDEX" not in f:
            process_file(os.path.join(d, f), f)

# Aggregate by profile
profile_agg = defaultdict(lambda: {"MVP_words": [], "CREAM_words": [], "MVP_slen": [], "CREAM_slen": []})
level_agg = defaultdict(lambda: {"MVP_words": [], "CREAM_words": [], "MVP_slen": [], "CREAM_slen": []})

for s in stats:
    p = s['profile']
    l = s['level']
    pipe = s['pipeline']
    
    profile_agg[p][f"{pipe}_words"].append(s['words'])
    profile_agg[p][f"{pipe}_slen"].append(s['avg_sentence_len'])
    
    level_agg[l][f"{pipe}_words"].append(s['words'])
    level_agg[l][f"{pipe}_slen"].append(s['avg_sentence_len'])

def summarize(agg_dict):
    res = {}
    for k, v in agg_dict.items():
        res[k] = {
            "MVP_words": round(sum(v["MVP_words"])/len(v["MVP_words"])) if v["MVP_words"] else 0,
            "CREAM_words": round(sum(v["CREAM_words"])/len(v["CREAM_words"])) if v["CREAM_words"] else 0,
            "MVP_sentence_len": round(sum(v["MVP_slen"])/len(v["MVP_slen"]), 1) if v["MVP_slen"] else 0,
            "CREAM_sentence_len": round(sum(v["CREAM_slen"])/len(v["CREAM_slen"]), 1) if v["CREAM_slen"] else 0,
        }
    return res

print("--- BY PROFILE ---")
print(json.dumps(summarize(profile_agg), indent=2))
print("--- BY LEVEL ---")
print(json.dumps(summarize(level_agg), indent=2))
