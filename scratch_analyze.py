import os
import glob
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
        
    # Extract basic info
    if "MVP" in filename:
        pipeline = "MVP"
    elif "CREAM" in filename:
        pipeline = "CREAM"
    else:
        pipeline = "Unknown"
        
    model = "Unknown"
    if "gpt_4o" in filename:
        model = "gpt-4o"
    elif "gpt_4.1_mini" in filename or "gpt_4_1_mini" in filename or "gpt-4.1-mini" in filename:
        model = "gpt-4.1-mini"
    elif "gemma_3" in filename:
        model = "gemma-3-27b"
    elif "gemma_4" in filename:
        model = "gemma-4-31b"
        
    # Content metrics
    char_count = len(content)
    word_count = len(content.split())
    h1_count = len(re.findall(r'^#\s+', content, re.MULTILINE))
    h2_count = len(re.findall(r'^##\s+', content, re.MULTILINE))
    h3_count = len(re.findall(r'^###\s+', content, re.MULTILINE))
    bold_count = len(re.findall(r'\*\*.*?\*\*', content))
    bullet_count = len(re.findall(r'^[-*]\s+', content, re.MULTILINE))
    
    has_pedagogy = "Argumentació pedagògica" in content
    has_audit = "Notes d'auditoria" in content
    
    stats.append({
        "file": filename,
        "pipeline": pipeline,
        "model": model,
        "char_count": char_count,
        "word_count": word_count,
        "h1": h1_count,
        "h2": h2_count,
        "h3": h3_count,
        "bold": bold_count,
        "bullet": bullet_count,
        "pedagogy": has_pedagogy,
        "audit": has_audit
    })

# files in base_dir starting with 20260423_232045_
for f in os.listdir(base_dir):
    if f.startswith("20260423_232045_") and f.endswith(".md") and "INDEX" not in f:
        process_file(os.path.join(base_dir, f), f)

for d in directories:
    if not os.path.exists(d):
        continue
    for f in os.listdir(d):
        if f.endswith('.md') and "INDEX" not in f:
            process_file(os.path.join(d, f), f)

# Aggregate stats
aggregated = defaultdict(lambda: {"count": 0, "chars": 0, "words": 0, "h2": 0, "h3": 0, "bold": 0, "bullet": 0, "pedagogy": 0, "audit": 0})

for s in stats:
    key = f"{s['pipeline']}_{s['model']}"
    aggregated[key]["count"] += 1
    aggregated[key]["chars"] += s["char_count"]
    aggregated[key]["words"] += s["word_count"]
    aggregated[key]["h2"] += s["h2"]
    aggregated[key]["h3"] += s["h3"]
    aggregated[key]["bold"] += s["bold"]
    aggregated[key]["bullet"] += s["bullet"]
    if s["pedagogy"]: aggregated[key]["pedagogy"] += 1
    if s["audit"]: aggregated[key]["audit"] += 1

print(json.dumps(aggregated, indent=2))
