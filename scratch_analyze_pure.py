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

def process_file(filepath, filename):
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
        
    if "MVP" in filename:
        pipeline = "MVP"
    elif "CREAM" in filename:
        pipeline = "CREAM"
    else:
        pipeline = "Unknown"
        
    model = "Unknown"
    if "gpt_4o" in filename:
        model = "gpt-4o"
    elif "gpt_4.1_mini" in filename or "gpt-4.1-mini" in filename:
        model = "gpt-4.1-mini"
    elif "gemma_3" in filename:
        model = "gemma-3-27b"
    elif "gemma_4" in filename:
        model = "gemma-4-31b"
        
    # Extract only the pure adapted text (ignore pedagogy/audit)
    # Split by the heading for pedagogical argument or audit notes
    parts = re.split(r'##\s*(?:Argumentació|Notes\s*d\'auditoria)', content, maxsplit=1, flags=re.IGNORECASE)
    pure_text = parts[0]
    
    char_count = len(pure_text)
    word_count = len(pure_text.split())
    
    # H2 and H3 only inside pure_text (and we ignore the header of the document like # gpt-4o · tea)
    # Actually, wait, CREAM often has "## Text adaptat"
    h2_count = len(re.findall(r'^##\s+', pure_text, re.MULTILINE))
    h3_count = len(re.findall(r'^###\s+', pure_text, re.MULTILINE))
    bold_count = len(re.findall(r'\*\*.*?\*\*', pure_text))
    bullet_count = len(re.findall(r'^[-*]\s+', pure_text, re.MULTILINE))
    
    stats.append({
        "file": filename,
        "pipeline": pipeline,
        "model": model,
        "pure_chars": char_count,
        "pure_words": word_count,
        "h2": h2_count,
        "h3": h3_count,
        "bold": bold_count,
        "bullet": bullet_count
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

aggregated = defaultdict(lambda: {"count": 0, "pure_chars": 0, "pure_words": 0, "h2": 0, "h3": 0, "bold": 0, "bullet": 0})

for s in stats:
    key = f"{s['pipeline']}"
    aggregated[key]["count"] += 1
    aggregated[key]["pure_chars"] += s["pure_chars"]
    aggregated[key]["pure_words"] += s["pure_words"]
    aggregated[key]["h2"] += s["h2"]
    aggregated[key]["h3"] += s["h3"]
    aggregated[key]["bold"] += s["bold"]
    aggregated[key]["bullet"] += s["bullet"]

# Calculate averages
result = {}
for k, v in aggregated.items():
    c = v["count"]
    result[k] = {
        "count": c,
        "avg_words": round(v["pure_words"] / c, 1),
        "avg_h2": round(v["h2"] / c, 1),
        "avg_h3": round(v["h3"] / c, 1),
        "avg_bold": round(v["bold"] / c, 1),
        "avg_bullet": round(v["bullet"] / c, 1)
    }

print(json.dumps(result, indent=2))
