"""Anàlisi puntual dels complements al pilot (v2 — adaptada al schema real).

Llegeix Supabase amb SERVICE_KEY (bypass RLS) i respon a les preguntes
que el schema actual permet contestar.

Realitat del schema (auditat 2026-05-21):
- atne_sessions NO té ni complements ni params (només instruction_ids, mecr, etapa, conditions)
- history.params_json només té {nivell, adaptacio} — NO complements
- adapt_started event té n_complements (count, no llista)
- complement_generated/deleted NO s'emeten al Pas 2 actual
- complement_toggled només al Flash mode
- complement_edited al Pas 3 (3 events totals)
- history.rating té 162 ratings (modal antic /home); pill nou només n=4

Preguntes que SÍ podem respondre amb dades reals:
  1. Rúbrica «Falten ajuts» — % i observacions concretes
  2. Comentaris lliures amb paraules clau de complements
  3. Distribució n_complements i correlació amb mecr_sortida
  4. Edicions manuals al Pas 3 (qualitat de generació)
  5. Toggles al Flash mode (què desactiva el docent)
  6. Errors al pipeline d'adaptació (adapt_error)

Ús: PYTHONIOENCODING=utf-8 python tests/analyze_complements.py
"""

from __future__ import annotations
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
if not SUPABASE_URL or not SERVICE_KEY:
    sys.exit("Falten SUPABASE_URL / SUPABASE_SERVICE_KEY al .env")

HEADERS = {"apikey": SERVICE_KEY, "Authorization": f"Bearer {SERVICE_KEY}"}
BASE = f"{SUPABASE_URL}/rest/v1"


def get(path: str, params: str = "") -> list:
    r = requests.get(f"{BASE}/{path}{('?' + params) if params else ''}", headers=HEADERS, timeout=20)
    if r.status_code != 200:
        print(f"  ! GET {path}: HTTP {r.status_code}")
        return []
    return r.json()


def section(title: str) -> None:
    print(f"\n{'=' * 78}\n {title}\n{'=' * 78}")


def table(rows: list[tuple], headers: tuple) -> None:
    if not rows:
        print("  (cap dada)")
        return
    widths = [max(len(str(h)), max((len(str(r[i])) for r in rows), default=0)) for i, h in enumerate(headers)]
    print("  " + "  ".join(str(h).ljust(w) for h, w in zip(headers, widths)))
    print("  " + "  ".join("-" * w for w in widths))
    for r in rows:
        print("  " + "  ".join(str(c).ljust(w) for c, w in zip(r, widths)))


# ──────────────────────────────────────────────────────────────────────
# Càrrega
# ──────────────────────────────────────────────────────────────────────
print("Carregant dades del pilot...")

events = get(
    "atne_pilot_events",
    "select=ts,event_type,session_id,docent_id,data&order=ts.desc&limit=10000",
)
events = [e for e in events if not (e.get("data") or {}).get("_health_probe")
                              and not (e.get("data") or {}).get("_boot_probe")]
print(f"  · {len(events)} events (sense probes)")

feedback = get(
    "history",
    "select=created_at,etapa,curs,rating,comment,review_items,edit_manual,exported,copied,"
    "refine_count,params_json,profile_json,context_json,perfil_kind&order=created_at.desc&limit=2000",
)
print(f"  · {len(feedback)} feedbacks")

# ──────────────────────────────────────────────────────────────────────
# 1. RÚBRICA — «Falten ajuts»
# ──────────────────────────────────────────────────────────────────────
section("1. RÚBRICA — Refinaments que marquen «Falten ajuts/complements»")

rubric_events = [e for e in events if e.get("event_type") == "redo_rubric"]
problems_counter: Counter = Counter()
observacions_per_problema: dict[str, list[str]] = defaultdict(list)

for e in rubric_events:
    data = e.get("data") or {}
    probs = data.get("problems") or []
    obs = (data.get("user_observation") or "").strip()
    ts = (e.get("ts") or "")[:16].replace("T", " ")
    for p in probs:
        problems_counter[p] += 1
        if obs:
            observacions_per_problema[p].append(f"[{ts}] {obs[:200]}")

print(f"  Total refinaments via rúbrica: {len(rubric_events)}")
print(f"  Total problemes marcats: {sum(problems_counter.values())}")
table([(p[:65], c) for p, c in problems_counter.most_common()], ("problema", "count"))

complement_problems = [p for p in problems_counter if "complement" in p.lower() or "ajut" in p.lower() or "glossari" in p.lower()]
total_complement = sum(problems_counter[p] for p in complement_problems)
if rubric_events:
    pct = total_complement / len(rubric_events) * 100
    print(f"\n  → % refinaments que toquen complements/ajuts: {pct:.0f}% ({total_complement}/{len(rubric_events)})")

print("\n  Observacions de docents sobre «Falten ajuts»:")
for p in complement_problems:
    for obs in observacions_per_problema[p][:5]:
        print(f"    · {obs}")

# ──────────────────────────────────────────────────────────────────────
# 2. COMENTARIS LLIURES — paraules clau
# ──────────────────────────────────────────────────────────────────────
section("2. COMENTARIS LLIURES amb paraules clau de complements")

KEYWORDS = {
    "glossari": ["glossari", "glosari", "vocabulari", "lèxic", "definici"],
    "preguntes": ["pregunta", "preg.", "qüesti", "comprensi"],
    "pictogrames": ["pictograma", "imatge", "il·lustra", "il.lustra", "dibuix"],
    "mapa": ["mapa conceptual", "mapa mental"],
    "bastides": ["bastida", "scaffold", "suport"],
    "esquema": ["esquema"],
    "resum": ["resum"],
    "ajut": ["ajut", "complement"],
}

def detect_categories(text: str) -> list[str]:
    t = text.lower()
    cats = []
    for cat, kws in KEYWORDS.items():
        if any(k in t for k in kws):
            cats.append(cat)
    return cats

samples: list[tuple[str, str, str, list[str]]] = []  # (font, ts, text, cats)

# history.comment
for h in feedback:
    cmt = (h.get("comment") or "").strip()
    if cmt:
        cats = detect_categories(cmt)
        if cats:
            ts = (h.get("created_at") or "")[:16].replace("T", " ")
            samples.append(("history.comment", ts, cmt[:300], cats))

# refine_submitted.user_instruction, redo_rubric.user_observation, suggestion_submitted.text
for e in events:
    et = e.get("event_type")
    data = e.get("data") or {}
    text = ""
    if et == "refine_submitted":
        text = (data.get("user_instruction") or data.get("instruction_full") or "").strip()
    elif et == "redo_rubric":
        text = (data.get("user_observation") or "").strip()
    elif et == "suggestion_submitted":
        text = (data.get("text") or "").strip()
    if text:
        cats = detect_categories(text)
        if cats:
            ts = (e.get("ts") or "")[:16].replace("T", " ")
            samples.append((et, ts, text[:300], cats))

cat_counter: Counter = Counter()
for _, _, _, cats in samples:
    for c in cats:
        cat_counter[c] += 1

print(f"  Total comentaris amb paraules clau: {len(samples)}")
print()
print("  Categories més mencionades:")
table([(c, n) for c, n in cat_counter.most_common()], ("categoria", "mencions"))

print("\n  Mostres més recents (top 20):")
for font, ts, txt, cats in samples[:20]:
    print(f"    [{font:22s}] [{ts}] {cats}")
    print(f"      {txt[:240]}")

# ──────────────────────────────────────────────────────────────────────
# 3. n_complements × MECR (via adapt_started)
# ──────────────────────────────────────────────────────────────────────
section("3. n_COMPLEMENTS × MECR — Distribució i correlació")

adapt_started = [e for e in events if e.get("event_type") == "adapt_started"]
n_dist: Counter = Counter()
mecr_n: dict[str, list[int]] = defaultdict(list)
for e in adapt_started:
    data = e.get("data") or {}
    n = data.get("n_complements")
    mecr = data.get("mecr_sortida") or "?"
    if n is not None:
        n_dist[n] += 1
        mecr_n[mecr].append(n)

print(f"  Total adaptacions iniciades: {len(adapt_started)}")
print()
print("  Distribució nombre complements per adaptació:")
table([(n, c) for n, c in sorted(n_dist.items())], ("n_complements", "adaptacions"))

print("\n  Mitjana de complements actius per MECR:")
rows = []
for mecr in ["pre-A1", "A1", "A2", "B1", "B2", "C1", "C2"]:
    if mecr in mecr_n:
        vals = mecr_n[mecr]
        rows.append((mecr, len(vals), f"{sum(vals)/len(vals):.1f}", min(vals), max(vals)))
table(rows, ("MECR", "n_sessions", "mitjana_comp", "min", "max"))

# ──────────────────────────────────────────────────────────────────────
# 4. EDICIONS al Pas 3
# ──────────────────────────────────────────────────────────────────────
section("4. COMPLEMENTS — Edicions manuals al Pas 3 (senyal qualitat)")

edits = [e for e in events if e.get("event_type") == "complement_edited"]
edit_counter: Counter = Counter()
for e in edits:
    data = e.get("data") or {}
    comp = data.get("comp") or "?"
    edit_counter[comp] += 1

print(f"  Total edicions: {len(edits)}")
table([(c, n) for c, n in edit_counter.most_common()], ("complement", "edicions"))

# edit_manual de history
manual_edit_count = sum(1 for h in feedback if h.get("edit_manual"))
print(f"\n  Sessions amb edit_manual=true a history: {manual_edit_count} de {len(feedback)}")

# ──────────────────────────────────────────────────────────────────────
# 5. FLASH MODE — Toggles
# ──────────────────────────────────────────────────────────────────────
section("5. FLASH MODE — Toggles ON/OFF de complements")

toggled = [e for e in events if e.get("event_type") == "complement_toggled"]
on_counter: Counter = Counter()
off_counter: Counter = Counter()
for e in toggled:
    data = e.get("data") or {}
    comp = data.get("comp") or "?"
    action = data.get("action")
    if action == "off":
        off_counter[comp] += 1
    elif action == "on":
        on_counter[comp] += 1

print(f"  Total toggles: ON={sum(on_counter.values())}, OFF={sum(off_counter.values())}")
all_comps = sorted(set(on_counter) | set(off_counter))
rows = [(c, on_counter.get(c, 0), off_counter.get(c, 0)) for c in all_comps]
table(rows, ("complement", "ON", "OFF"))

# ──────────────────────────────────────────────────────────────────────
# 6. ERRORS al pipeline
# ──────────────────────────────────────────────────────────────────────
section("6. PIPELINE — Errors i abandonaments")

adapt_errors = [e for e in events if e.get("event_type") == "adapt_error"]
form_abandoned = [e for e in events if e.get("event_type") == "form_abandoned"]
client_errors = [e for e in events if e.get("event_type") == "client_error"]
adapt_done = [e for e in events if e.get("event_type") == "adapt_done"]

print(f"  adapt_started: {len(adapt_started)}")
print(f"  adapt_done:    {len(adapt_done)}")
print(f"  adapt_error:   {len(adapt_errors)}")
if adapt_started:
    print(f"  → ratio èxit: {len(adapt_done)/len(adapt_started)*100:.0f}%")
print(f"  form_abandoned: {len(form_abandoned)}")
print(f"  client_error:   {len(client_errors)}")

err_msgs: Counter = Counter()
for e in adapt_errors:
    data = e.get("data") or {}
    msg = data.get("error") or data.get("message") or "?"
    err_msgs[msg[:80]] += 1
if err_msgs:
    print("\n  Top errors d'adaptació:")
    table([(m, c) for m, c in err_msgs.most_common(10)], ("error", "count"))

# ──────────────────────────────────────────────────────────────────────
# 7. PUNTUACIÓ
# ──────────────────────────────────────────────────────────────────────
section("7. PUNTUACIÓ — Distribució rating global (history)")

ratings = [h["rating"] for h in feedback if h.get("rating") is not None]
if ratings:
    rd = Counter(ratings)
    print(f"  Total ratings: {len(ratings)}, mitjana: {sum(ratings)/len(ratings):.2f}/3")
    for r in sorted(rd):
        print(f"    {r}: {rd[r]}")
else:
    print("  (cap rating)")

# Review items checkboxes
review_counter: Counter = Counter()
altres_texts = []
for h in feedback:
    ri = h.get("review_items") or {}
    if isinstance(ri, dict):
        for k, v in ri.items():
            if k == "altres_text":
                if v:
                    altres_texts.append(str(v)[:200])
            elif v:
                review_counter[k] += 1
print("\n  Intent d'ús (checkboxes pill «Valora»):")
table([(k, v) for k, v in review_counter.most_common()], ("intent", "count"))

# ──────────────────────────────────────────────────────────────────────
# RESUM EXECUTIU
# ──────────────────────────────────────────────────────────────────────
section("RESUM EXECUTIU")

print(f"  · Adaptacions: {len(adapt_started)} iniciades, {len(adapt_done)} completades")
print(f"  · Feedbacks rating: {len(ratings)}, mitjana: {sum(ratings)/len(ratings):.2f}/3" if ratings else "  · Feedbacks: 0")
print(f"  · Refinaments rúbrica: {len(rubric_events)}")
if rubric_events:
    print(f"  · % rúbriques amb 'Falten ajuts': {total_complement/len(rubric_events)*100:.0f}%")
print(f"  · Comentaris parlant de complements: {len(samples)}")
print(f"  · Edicions manuals: {len(edits)} a events + {manual_edit_count} a history")
if cat_counter:
    print(f"  · Top categories als comentaris: {', '.join(f'{c}({n})' for c,n in cat_counter.most_common(3))}")
print()
