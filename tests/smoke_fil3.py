"""
smoke_fil3.py — Smoke test del Fil 3 (currículum LOMLOE → generador de textos).

Testa els dos endpoints públics de Fil 3 a producció (sense auth):
  - GET /api/genres       → catàleg de gèneres derivat del corpusFJE
  - GET /api/curriculum   → dades curriculars (matèries + sabers / ODA + continguts)

Execució:
  cd ATNE
  python tests/smoke_fil3.py [--url https://atne-nixj2vso2a-ew.a.run.app]

Si --url és omès, usa la URL de producció per defecte.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

# UTF-8 a la consola de Windows (evita UnicodeEncodeError amb el cp1252 per defecte)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ── URL per defecte ───────────────────────────────────────────────────────────
DEFAULT_URL = "https://atne-nixj2vso2a-ew.a.run.app"

# ── Colors terminal ───────────────────────────────────────────────────────────
OK   = "\033[92m✓\033[0m"
FAIL = "\033[91m✗\033[0m"
WARN = "\033[93m⚠\033[0m"
INFO = "\033[94m·\033[0m"


class SmokeResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warns  = 0
        self._failures: list[str] = []

    def ok(self, msg: str):
        print(f"  {OK} {msg}")
        self.passed += 1

    def fail(self, msg: str):
        print(f"  {FAIL} {msg}")
        self.failed += 1
        self._failures.append(msg)

    def warn(self, msg: str):
        print(f"  {WARN} {msg}")
        self.warns += 1

    def info(self, msg: str):
        print(f"  {INFO} {msg}")

    def section(self, title: str):
        print(f"\n{'─'*60}")
        print(f"  {title}")
        print(f"{'─'*60}")

    def summary(self):
        print(f"\n{'═'*60}")
        total = self.passed + self.failed
        if self.failed == 0:
            print(f"  {OK} TOTS ELS TESTS HAN PASSAT ({self.passed}/{total})")
        else:
            print(f"  {FAIL} FALLADES: {self.failed}/{total}")
            for f in self._failures:
                print(f"      • {f}")
        if self.warns:
            print(f"  {WARN} Advertències: {self.warns}")
        print(f"{'═'*60}")
        return self.failed == 0


# ── Helpers HTTP ──────────────────────────────────────────────────────────────

def _get(base: str, path: str, params: dict | None = None, timeout: int = 15) -> tuple[int, dict]:
    """GET simple. Retorna (status_code, body_dict)."""
    url = base.rstrip("/") + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    try:
        t0 = time.time()
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            ms = int((time.time() - t0) * 1000)
            try:
                data = json.loads(raw)
            except Exception:
                data = {"_raw": raw[:200]}
            return resp.status, data, ms
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            data = json.loads(raw)
        except Exception:
            data = {"_raw": raw[:200]}
        return e.code, data, 0
    except Exception as ex:
        return 0, {"_error": str(ex)}, 0


# ── Blocs de tests ─────────────────────────────────────────────────────────────

def test_health(base: str, r: SmokeResult):
    r.section("1. /api/health")
    status, body, ms = _get(base, "/api/health")
    if status == 200:
        r.ok(f"Servidor actiu ({ms}ms)")
    else:
        r.fail(f"Health check ha fallat: HTTP {status}")
        return False
    return True


def test_genres(base: str, r: SmokeResult):
    r.section("2. /api/genres — catàleg de gèneres")

    # 2a. Format grouped (per defecte)
    status, body, ms = _get(base, "/api/genres")
    if status != 200:
        r.fail(f"HTTP {status} (esperat 200)"); return
    if not body.get("ok"):
        r.fail(f"ok=false al body"); return
    r.ok(f"Resposta 200 ({ms}ms)")

    # No degradat
    if body.get("degraded"):
        r.fail("catàleg DEGRADAT (submòdul no carregat)")
    else:
        r.ok("catàleg no degradat (submòdul OK)")

    # Total >= 22
    total = body.get("total", 0)
    if total >= 22:
        r.ok(f"total = {total} gèneres (≥22 ✓)")
    else:
        r.fail(f"total = {total} gèneres (esperat ≥22)")

    # Versió present
    version = body.get("version")
    if version:
        r.info(f"versió submòdul: {version}")
    else:
        r.warn("versió no disponible")

    # Famílies presents
    families = body.get("families", [])
    family_names = {f["macro_tipologia"] for f in families}
    EXPECTED_FAMILIES = {"narrativa", "explicativa", "argumentativa", "instructiva",
                         "conversacional", "descriptiva", "poetica"}
    missing_fam = EXPECTED_FAMILIES - family_names
    if not missing_fam:
        r.ok(f"7 famílies canòniques presents")
    else:
        r.fail(f"famílies que falten: {missing_fam}")

    # Gèneres STEAM (3/3)
    status2, flat, ms2 = _get(base, "/api/genres", {"format": "flat"})
    all_keys = {g["genre_key"] for g in flat.get("generes", [])}

    STEAM_GENRES = {"poster_cientific", "diari_camp", "practica_laboratori"}
    missing_steam = STEAM_GENRES - all_keys
    if not missing_steam:
        r.ok(f"STEAM 3/3 presents: {', '.join(sorted(STEAM_GENRES))}")
    else:
        r.fail(f"STEAM que falten: {missing_steam}")

    # Gèneres Fase 3 (5/5)
    FASE3_GENRES = {"enunciat", "mail_professional", "cv", "informe_tecnic", "instancia"}
    missing_f3 = FASE3_GENRES - all_keys
    if not missing_f3:
        r.ok(f"Fase 3 5/5 presents: {', '.join(sorted(FASE3_GENRES))}")
    else:
        r.fail(f"Fase 3 que falten: {missing_f3}")

    # Estructura interna: cada gènere té els camps mínims
    generes = flat.get("generes", [])
    required_fields = {"genre_key", "label_ca", "macro_tipologia"}
    malformed = [g.get("genre_key", "?") for g in generes if not required_fields.issubset(g)]
    if not malformed:
        r.ok(f"tots els gèneres tenen genre_key + label_ca + macro_tipologia")
    else:
        r.fail(f"gèneres mal formats (camps mínims absents): {malformed}")

    # Format keys_only
    status3, keys_body, _ = _get(base, "/api/genres", {"keys_only": "1"})
    if status3 == 200 and "genre_keys" in keys_body:
        r.ok(f"format keys_only OK ({len(keys_body['genre_keys'])} claus)")
    else:
        r.fail(f"format keys_only ha fallat (HTTP {status3})")

    # Sense etapa → 400
    status4, err_body, _ = _get(base, "/api/curriculum")
    if status4 == 400:
        r.ok("sense etapa retorna HTTP 400 (correcte)")
    else:
        r.warn(f"sense etapa retorna HTTP {status4} (esperat 400)")


def test_curriculum_eso(base: str, r: SmokeResult):
    r.section("3. /api/curriculum?etapa=eso — matèries ESO")

    status, body, ms = _get(base, "/api/curriculum", {"etapa": "eso"})
    if status != 200:
        r.fail(f"HTTP {status} (esperat 200)"); return
    r.ok(f"Resposta 200 ({ms}ms)")

    if body.get("ok") and body.get("etapa") == "eso":
        r.ok("ok=true, etapa=eso")
    else:
        r.fail(f"body incorrecte: ok={body.get('ok')}, etapa={body.get('etapa')}")

    items = body.get("items", [])
    # Esperat: 19 matèries ESO (manifest)
    if len(items) >= 10:
        r.ok(f"{len(items)} matèries ESO (esperat ≥10)")
    else:
        r.fail(f"Massa poques matèries ESO: {len(items)} (esperat ≥10)")

    # Estructura de cada matèria
    if items:
        sample = items[0]
        required = {"clau", "nom", "codi", "tipus"}
        if required.issubset(sample):
            r.ok(f"estructura OK: {sample['clau']} / {sample['nom']}")
        else:
            r.fail(f"camps absents: {required - set(sample)}")


def test_curriculum_eso_sabers(base: str, r: SmokeResult):
    r.section("4. /api/curriculum?etapa=eso&materia=matematiques&curs=3r — sabers")

    status, body, ms = _get(base, "/api/curriculum",
                             {"etapa": "eso", "materia": "matematiques", "curs": "3r"})
    if status != 200:
        r.fail(f"HTTP {status} (esperat 200)"); return
    r.ok(f"Resposta 200 ({ms}ms)")

    if body.get("tipus") != "sabers":
        r.fail(f"tipus esperat 'sabers', rebut '{body.get('tipus')}'"); return

    sabers = body.get("sabers", [])
    if sabers:
        r.ok(f"{len(sabers)} sabers per a 3r ESO Matemàtiques")
    else:
        r.fail("0 sabers retornats (esperat >0)")
        return

    # Estructura de cada saber
    s = sabers[0]
    required = {"bloc", "text", "nivell_norm"}
    if required.issubset(s):
        r.ok(f"estructura saber OK: nivell_norm={s.get('nivell_norm')}")
    else:
        r.fail(f"camps absents al saber: {required - set(s)}")

    # nivell_norm ha de ser ESO_C1 (3r ESO = primer cicle)
    nivells = {s.get("nivell_norm") for s in sabers}
    if "ESO_C1" in nivells:
        r.ok(f"nivell_norm ESO_C1 present (3r ESO → cicle 1 ✓)")
    else:
        r.warn(f"nivell_norm no inclou ESO_C1: trobats {nivells}")

    # Grups per bloc presents
    agrupats = body.get("agrupats", [])
    if agrupats:
        r.ok(f"{len(agrupats)} blocs/grups (ex: '{agrupats[0].get('bloc','?')}')")
    else:
        r.warn("agrupats buit")


def test_curriculum_primaria(base: str, r: SmokeResult):
    r.section("5. /api/curriculum?etapa=primaria — matèries primària")

    status, body, ms = _get(base, "/api/curriculum", {"etapa": "primaria"})
    if status != 200:
        r.fail(f"HTTP {status}"); return
    r.ok(f"Resposta 200 ({ms}ms)")

    items = body.get("items", [])
    if len(items) >= 8:
        r.ok(f"{len(items)} matèries primària (esperat ≥8)")
    else:
        r.fail(f"Poques matèries primària: {len(items)}")

    # Test amb curs de cicle 2
    status2, body2, ms2 = _get(base, "/api/curriculum",
                                {"etapa": "primaria", "materia": "catala", "curs": "4t"})
    if status2 == 200 and body2.get("tipus") == "sabers":
        sabers2 = body2.get("sabers", [])
        r.ok(f"sabers 4t primària català: {len(sabers2)} sabers")
        # nivell_norm ha de ser PRI_C2
        nivells2 = {s.get("nivell_norm") for s in sabers2}
        if "PRI_C2" in nivells2:
            r.ok(f"nivell_norm PRI_C2 (4t primària → cicle 2 ✓)")
        else:
            r.warn(f"PRI_C2 no trobat: {nivells2}")
    else:
        r.fail(f"sabers 4t primària català: HTTP {status2} / tipus={body2.get('tipus')}")


def test_curriculum_batxillerat(base: str, r: SmokeResult):
    r.section("6. /api/curriculum?etapa=batxillerat — matèries batxillerat")

    status, body, ms = _get(base, "/api/curriculum", {"etapa": "batxillerat"})
    if status != 200:
        r.fail(f"HTTP {status}"); return
    r.ok(f"Resposta 200 ({ms}ms)")

    items = body.get("items", [])
    if len(items) >= 20:
        r.ok(f"{len(items)} matèries batxillerat (esperat ≥20)")
    else:
        r.fail(f"Poques matèries batxillerat: {len(items)}")

    # Test sabers 1r batxillerat
    status2, body2, ms2 = _get(base, "/api/curriculum",
                                {"etapa": "batxillerat", "materia": "biologia", "curs": "1r"})
    if status2 == 200 and body2.get("tipus") == "sabers":
        sabers2 = body2.get("sabers", [])
        r.ok(f"sabers 1r batxillerat biologia: {len(sabers2)} sabers")
        nivells2 = {s.get("nivell_norm") for s in sabers2}
        if nivells2 & {"BAT_1R", "BAT_GEN"}:
            r.ok(f"nivell_norm {nivells2 & {'BAT_1R','BAT_GEN'}} (1r bat ✓)")
        else:
            r.warn(f"nivell_norm no inclou BAT_1R/BAT_GEN: {nivells2}")
    else:
        r.warn(f"sabers 1r bat biologia: HTTP {status2} (matèria pot no existir)")


def test_curriculum_infantil(base: str, r: SmokeResult):
    r.section("7. /api/curriculum?etapa=infantil — ODA infantil")

    status, body, ms = _get(base, "/api/curriculum", {"etapa": "infantil"})
    if status != 200:
        r.fail(f"HTTP {status}"); return
    r.ok(f"Resposta 200 ({ms}ms)")

    if body.get("tipus") != "objectius":
        r.fail(f"tipus esperat 'objectius', rebut '{body.get('tipus')}'"); return

    items = body.get("items", [])
    if items:
        r.ok(f"{len(items)} ODA d'infantil")
    else:
        r.fail("0 ODA retornats (esperat >0)")
        return

    # Estructura ODA
    oda = items[0]
    required_oda = {"clau", "nom", "codi", "tipus", "ambit", "area"}
    if required_oda.issubset(oda):
        r.ok(f"estructura ODA OK: {oda.get('codi')} ({oda.get('ambit','?')[:30]})")
    else:
        r.fail(f"camps absents a l'ODA: {required_oda - set(oda)}")

    if oda.get("tipus") == "oda":
        r.ok("tipus='oda' correcte")
    else:
        r.fail(f"tipus='oda' esperat, rebut '{oda.get('tipus')}'")

    # Agrupats per àmbit
    agrupats = body.get("agrupats", [])
    if agrupats:
        r.ok(f"{len(agrupats)} àmbits (ex: '{agrupats[0].get('ambit','?')[:40]}')")
    else:
        r.warn("agrupats per àmbit buit")

    # Test continguts d'un ODA
    oda_codi = oda.get("clau") or oda.get("codi")
    if oda_codi:
        status2, body2, ms2 = _get(base, "/api/curriculum",
                                   {"etapa": "infantil", "materia": oda_codi})
        if status2 == 200 and body2.get("tipus") == "continguts":
            blocs = body2.get("sabers", [])
            r.ok(f"continguts de l'ODA {oda_codi}: {len(blocs)} blocs de contingut")
        else:
            r.fail(f"continguts ODA: HTTP {status2} / tipus={body2.get('tipus')}")


def test_curriculum_fp(base: str, r: SmokeResult):
    r.section("8. /api/curriculum?etapa=fp — FP (fora abast Fase 1)")

    status, body, ms = _get(base, "/api/curriculum", {"etapa": "fp"})
    if status == 200:
        items = body.get("items", [])
        if items == []:
            r.ok("FP retorna llista buida (esperat — fora abast Fase 1)")
        else:
            r.warn(f"FP retorna {len(items)} matèries (inesperat — potser indexat?)")
    else:
        r.warn(f"FP retorna HTTP {status} (esperat 200 amb llista buida)")


def test_curriculum_error_cases(base: str, r: SmokeResult):
    r.section("9. Casos d'error i límit")

    # Sense etapa → 400
    status, body, _ = _get(base, "/api/curriculum")
    if status == 400 and body.get("ok") is False:
        r.ok("sense etapa → HTTP 400 + ok=false")
    else:
        r.fail(f"sense etapa → HTTP {status} (esperat 400)")

    # Etapa inexistent → 200 amb llista buida (tolerant)
    status2, body2, _ = _get(base, "/api/curriculum", {"etapa": "inexistent"})
    if status2 == 200 and body2.get("items") == []:
        r.ok("etapa inexistent → 200 + items=[] (tolerant ✓)")
    else:
        r.warn(f"etapa inexistent → HTTP {status2}")

    # Matèria inexistent per a una etapa real → sabers=[] (tolerant)
    status3, body3, _ = _get(base, "/api/curriculum",
                              {"etapa": "eso", "materia": "materia_inexistent", "curs": "1r"})
    if status3 == 200 and body3.get("sabers") == []:
        r.ok("matèria inexistent → 200 + sabers=[] (tolerant ✓)")
    else:
        r.warn(f"matèria inexistent → HTTP {status3} / sabers={body3.get('sabers')}")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Smoke test Fil 3")
    parser.add_argument("--url", default=DEFAULT_URL, help="URL base de l'ATNE")
    args = parser.parse_args()

    base = args.url.rstrip("/")
    print(f"\nSMOKE TEST FIL 3 — {base}")
    print(f"Data: 2026-06-27\n")

    r = SmokeResult()

    alive = test_health(base, r)
    if not alive:
        r.summary()
        sys.exit(1)

    test_genres(base, r)
    test_curriculum_eso(base, r)
    test_curriculum_eso_sabers(base, r)
    test_curriculum_primaria(base, r)
    test_curriculum_batxillerat(base, r)
    test_curriculum_infantil(base, r)
    test_curriculum_fp(base, r)
    test_curriculum_error_cases(base, r)

    ok = r.summary()
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
