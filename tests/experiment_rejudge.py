"""experiment_rejudge.py — 2a passada de jutge (creuat) + informe combinat.

Reusa les generacions ja fetes (experiment_models_*.json) i les RE-JUTJA amb un segon
jutge (per defecte gemini-2.5-flash, gratis), sense re-generar (estalvia el cost de la
generació de pagament). Produeix un informe combinat amb:
  - mitjana per candidat de CADA jutge (gpt-4.1-mini i gemini-2.5-flash)
  - concordança entre jutges (diferència de mitjanes) + marca de self-judging
    (jutge del mateix proveïdor que el candidat → puntuació potencialment inflada)

ÚS:
    python tests/experiment_rejudge.py                      # agafa el JSON més recent
    python tests/experiment_rejudge.py <fitxer.json> --judge2 gemini-2.5-flash --sleep 8
"""
from __future__ import annotations
import argparse, json, statistics, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from tests.experiment_models_2026 import CASES, judge, _provider_of  # noqa: E402

CASES_BY_ID = {c["id"]: c for c in CASES}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json", nargs="?", help="JSON de l'experiment (per defecte: el més recent)")
    ap.add_argument("--judge2", default="gemini-2.5-flash")
    ap.add_argument("--judge1-name", default="gpt-4.1-mini", help="nom del jutge de la 1a passada (per a l'informe)")
    ap.add_argument("--sleep", type=float, default=8.0)
    args = ap.parse_args()

    outdir = ROOT / "tests" / "results"
    path = Path(args.json) if args.json else max(outdir.glob("experiment_models_*.json"), key=lambda p: p.stat().st_mtime)
    data = json.loads(path.read_text(encoding="utf-8"))
    print(f"Re-jutjant {path.name} amb judge2={args.judge2}\n")

    # 2a passada: re-jutja cada generació amb èxit.
    for r in data:
        if "error" in r or not r.get("text_adaptat"):
            continue
        case = CASES_BY_ID.get(r["cas"])
        if not case:
            continue
        print(f"  [{r['cas']}] {r['model']} (judge2) …", end=" ", flush=True)
        try:
            j2 = judge(args.judge2, case, r["text_adaptat"])
            r["fons_judge2"] = j2
            print(f"fons2={j2.get('mitjana')}")
        except Exception as e:
            r["fons_judge2"] = {"error": str(e)}
            print(f"ERROR: {e}")
        time.sleep(args.sleep)

    ts = path.stem.replace("experiment_models_", "")
    (outdir / f"experiment_combinat_{ts}.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    # Agregació per candidat.
    models = []
    for r in data:
        if r["model"] not in models:
            models.append(r["model"])

    def _avg(xs):
        xs = [x for x in xs if x is not None]
        return round(statistics.mean(xs), 2) if xs else None

    lines = [f"# Experiment models — informe combinat (jutge creuat) · {ts}", "",
             f"Jutge 1: **{args.judge1_name}** · Jutge 2: **{args.judge2}** · Casos: {len({r['cas'] for r in data})}",
             "",
             "| Candidat | Fons J1 | Fons J2 | Δ (concordança) | C5 català (J1/J2) | F1 dins rang | Latència med. (ms) | Tokens out med. | Self-judge |",
             "|---|---|---|---|---|---|---|---|---|"]
    summary = {}
    for m in models:
        rs = [r for r in data if r["model"] == m and "error" not in r]
        if not rs:
            lines.append(f"| {m} | — (tots ERROR) | — | — | — | — | — | — | — |")
            continue
        j1 = _avg([r["fons"].get("mitjana") for r in rs if isinstance(r.get("fons"), dict)])
        j2 = _avg([r["fons_judge2"].get("mitjana") for r in rs if isinstance(r.get("fons_judge2"), dict)])
        c5_1 = _avg([r["fons"].get("C5_qualitat_catala", {}).get("p") for r in rs if isinstance(r.get("fons"), dict)])
        c5_2 = _avg([r["fons_judge2"].get("C5_qualitat_catala", {}).get("p") for r in rs if isinstance(r.get("fons_judge2"), dict)])
        delta = round(abs(j1 - j2), 2) if (j1 is not None and j2 is not None) else None
        f1 = sum(r["f1_longitud"]["dins_rang"] for r in rs if isinstance(r.get("f1_longitud"), dict))
        lat = round(statistics.median(r["latencia_ms"] for r in rs))
        tok = round(statistics.median(r["tokens_out"] for r in rs))
        # Self-judge: quin jutge és del mateix proveïdor que el candidat.
        sj = []
        if _provider_of(m) == _provider_of(args.judge1_name): sj.append("J1")
        if _provider_of(m) == _provider_of(args.judge2): sj.append("J2")
        summary[m] = {"j1": j1, "j2": j2, "delta": delta, "n": len(rs)}
        lines.append(f"| {m} | {j1} | {j2} | {delta} | {c5_1}/{c5_2} | {f1}/{len(rs)} | {lat} | {tok} | {'+'.join(sj) or '—'} |")

    lines += ["", "## Com llegir-ho",
              "- **Fons J1/J2** = mitjana C1-C5 (1-5) de cada jutge. **Δ** = concordança (com més petit, més acord).",
              "- **Self-judge**: J1 (gpt-4.1-mini) infla candidats OpenAI; J2 (gemini) infla candidats Gemini.",
              "  → per a un candidat, la puntuació CREUADA (jutge de l'altre proveïdor) és la menys esbiaixada.",
              "- **C5** = qualitat del català. **F1** = casos amb longitud de frase dins el rang MECR.",
              "- Si la diferència entre candidats és petita, **mana compliance (residència UE / Vertex)**, no el benchmark.",
              "", "## Veredicte per candidat (puntuació CREUADA, menys esbiaixada)"]
    for m in models:
        if m not in summary: continue
        cross = summary[m]["j2"] if _provider_of(m) != _provider_of(args.judge2) else summary[m]["j1"]
        lines.append(f"- **{m}**: creuat ≈ {cross} · J1={summary[m]['j1']} J2={summary[m]['j2']} (Δ {summary[m]['delta']}) · n={summary[m]['n']}")

    report = outdir / f"experiment_combinat_{ts}.md"
    report.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nInforme combinat: {report}")
    print(f"JSON combinat:   {outdir / f'experiment_combinat_{ts}.json'}")


if __name__ == "__main__":
    main()
