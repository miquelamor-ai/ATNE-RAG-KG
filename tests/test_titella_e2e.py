"""
tests/test_titella_e2e.py — Re-adapt the user's titella case end-to-end
with the current code and dump everything (text, glossari, esquema, bastides,
pictogrames). Used to compare with the 2026-05-30 PDF that triggered this week's
fixes.

NOT a test (no assertions). Just an inspection harness.
"""
from __future__ import annotations
import sys, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
from dotenv import load_dotenv
load_dotenv(ROOT / ".env")

from adaptation.orchestrator import run_adaptation

ORIGINAL = """Com fer un titella de mitja

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
"""

PROFILE = {
    "name": "L'Aprenent",
    "course": "1r Primària",
    "type": "individual",
    "cat": "disl",
    "chips": [{"cat": "disl", "label": "Dislèxia"}],
    "conditions": [{"key": "dislexia", "actiu": True, "grau": "moderat"}],
    "caracteristiques": {
        "dislexia": {"actiu": True, "grau": "moderat"},
    },
}

PARAMS = {
    "mecr_sortida": "A1",
    "dua": "Core",
    "genere_discursiu": "receptari",
    "complements": {
        "glossari": True,
        "esquema_visual": True,
        "bastides": True,
        "pictogrames": True,
    },
    "lang": "ca",
    "verify_retry": True,
}

CONTEXT = {
    "etapa": "Primària",
    "materia": "manualitats",
    "curs": "1r Primària",
}


def main():
    events = []
    def cb(ev):
        events.append(ev)
        t = ev.get("type")
        if t == "step":
            print(f"[step:{ev.get('step')}] {ev.get('msg','')[:120]}")
    print("=" * 70)
    print("ADAPTANT EL TITELLA — perfil dislèxia A1, 1r primària, receptari")
    print("=" * 70)
    run_adaptation(
        text=ORIGINAL,
        profile=PROFILE,
        context=CONTEXT,
        params=PARAMS,
        progress_callback=cb,
    )
    adapted = ""
    for ev in events:
        if ev.get("type") == "result" and ev.get("adapted"):
            adapted = ev["adapted"]
            break
    if not adapted:
        # fallback: concat deltes
        deltes = [ev.get("text", "") for ev in events if ev.get("type") == "delta"]
        adapted = "".join(deltes)
    print("\n" + "=" * 70)
    print(f"OUTPUT FINAL ({len(adapted)} chars)")
    print("=" * 70)
    print(adapted)

    print("\n" + "=" * 70)
    print("MÈTRIQUES OBJECTIVES")
    print("=" * 70)
    # Text adaptat: longitud + similitud amb l'original (proxy)
    m_text = re.search(r"^## Text adaptat\b[^\n]*\n(.+?)(?=^## |\Z)", adapted, re.M | re.S)
    text_adap = m_text.group(1).strip() if m_text else ""
    orig_words = set(ORIGINAL.lower().split())
    adap_words = set(text_adap.lower().split())
    overlap = len(orig_words & adap_words) / max(len(orig_words), 1)
    print(f"  Text adaptat: {len(text_adap)} chars (original: {len(ORIGINAL)} chars)")
    print(f"  Overlap de tokens únics amb l'original: {overlap*100:.0f}%")
    # Picto markers (text adaptat només)
    pictos = len(re.findall(r"\[PICTO:", text_adap))
    arasaac = len(re.findall(r"arasaac", text_adap))
    print(f"  [PICTO:] markers o URLs ARASAAC: {pictos+arasaac}")
    # Glossari terms
    m_g = re.search(r"^## Glossari\b[^\n]*\n(.+?)(?=^## |\Z)", adapted, re.M | re.S)
    g_terms = []
    if m_g:
        for ln in m_g.group(1).splitlines():
            if ln.strip().startswith("|") and "|" in ln[1:]:
                cells = [c.strip() for c in ln.strip("|").split("|")]
                if len(cells) >= 2 and not re.match(r"^[-:\s]+$", cells[0]) and cells[0].lower() != "terme":
                    g_terms.append(cells[0])
    print(f"  Glossari: {len(g_terms)} termes — {g_terms}")
    # Bastides: 3 moments?
    m_b = re.search(r"^## Bastides\b[^\n]*\n(.+?)(?=^## |\Z)", adapted, re.M | re.S)
    moments = 0
    if m_b:
        for kw in ("abans de llegir", "durant la lectura", "després de llegir"):
            if re.search(rf"^###.*{kw}", m_b.group(1), re.M | re.I):
                moments += 1
    print(f"  Bastides: {moments}/3 moments presents")
    # Esquema visual: arrel
    m_e = re.search(r"^## Esquema visual\b[^\n]*\n(.+?)(?=^## |\Z)", adapted, re.M | re.S)
    esq_root = "?"
    if m_e:
        for ln in m_e.group(1).splitlines():
            rm = re.match(r"^[-*]\s+(.+)", ln)
            if rm:
                esq_root = rm.group(1)[:60]
                break
    print(f"  Esquema arrel: {esq_root!r}")


if __name__ == "__main__":
    main()
