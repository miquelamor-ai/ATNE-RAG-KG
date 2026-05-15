"""
adaptation/params_resolver.py — Resolució canònica de paràmetres d'adaptació.

Font ÚNICA de veritat per al càlcul de MECR + DUA a partir d'un perfil.
Substitueix progressivament les 6 implementacions paral·leles repartides per:
  - ui/atne/pas1.html (_PCURS_TO_MECR, COURSE_TO_MECR del grup)
  - ui/atne/js/profile-canonical.js (deriveMECR)
  - ui/atne/pas3.html (computeMECRSortida)
  - ui/atne/flash.html + server.py _FLASH_CURS_MECR
  - server.py propose_adaptation (taula _MECR_PER_CURS interna)

Bug arrel que motiva aquest mòdul: cada implementació tenia regles
lleugerament diferents per a la mateixa entrada. Cas Petri I5 (Infantil 5
+ nouvingut + alfabet no llatí) sortia com a:
  - chip del perfil al Pas 1: pre-A1 (correcte, via deriveMECR)
  - MECR enviat al backend: A2 (incorrecte, via computeMECRSortida que
    forçava 'A2' per a tot nouvingut amb mesos no-numèrics)

Regla rectora pedagògica (Miquel Amor, 2026-05-15, refinada):
  ETAPA INFANTIL → MECR pre-A1 SEMPRE (Emergent), sigui quina sigui la
  resta de condicions: nouvingut, AACC, catalanoparlant pur, etc. Tota
  lectura a infantil és emergent i compartida amb un adult. La diferència
  entre perfils (nouvingut, AACC...) modifica QUÈ s'afegeix al voltant
  del text (glossari L1, suggeriments d'enriquiment per a la família,
  etc.) però NO el nivell del text mateix.

  Conseqüència: un I5 catalanoparlant amb AACC NO obté +1 nivell de MECR
  (A1). El seu suport AACC arribarà via les instruccions del catàleg
  filtrades per `altes_capacitats`, no per MECR més alt. Per a un I5
  nouvingut amb 24 mesos a Catalunya tampoc puja a A2 — el catàleg
  nouvingut activa G-01/G-03 (glossari + transliteració) per a la
  família lectora.
"""

# Ordre canònic dels nivells. min() pot calcular el "més baix" amb aquesta llista.
MECR_ORDER = ["pre-A1", "A1", "A2", "B1", "B2", "C1", "C2"]

# Taula canònica curs canònic -> MECR base (Decret 175/2022 + 171/2022 + 21/2023).
# Sincronitzada amb profile-canonical.js:COURSE_TO_MECR. Si canvies aquí,
# canvia allà (i a la inversa) — la Fase B.4 fa que el JS llegeixi d'aquí.
COURSE_TO_MECR = {
    "I3": "pre-A1", "I4": "pre-A1", "I5": "pre-A1",
    "1r Primària": "A1", "2n Primària": "A1",
    "3r Primària": "A1", "4t Primària": "A2",
    "5è Primària": "A2", "6è Primària": "B1",
    "Primer cicle Primària": "A1",
    "Segon cicle Primària": "A1",
    "Tercer cicle Primària": "A2",
    "1r ESO": "B1", "2n ESO": "B1", "3r ESO": "B2", "4t ESO": "B2",
    "Primer cicle ESO": "B1", "Segon cicle ESO": "B2",
    "1r Batxillerat": "B2", "2n Batxillerat": "C1",
    "Grau Bàsic": "A2", "Grau Mitjà": "B1", "Grau Superior": "B2",
    "1r FP Grau Bàsic": "A2", "2n FP Grau Bàsic": "A2",
    "1r FP Grau Mitjà": "B1", "2n FP Grau Mitjà": "B1",
    "1r FP Grau Superior": "B2", "2n FP Grau Superior": "B2",
}

# Fallback per etapa quan el curs concret no es coneix o no és canònic.
ETAPA_FALLBACK_MECR = {
    "infantil": "pre-A1",
    "primaria": "A1",
    "ESO": "B1",
    "batxillerat": "B2",
    "FP": "B1",
}


def _mesos_to_num(nouv_data: dict):
    """Tradueix mesos_catalunya (num) o mesos_catalunya_range (str) a número.

    Coherent amb profile-canonical.js mesosRangeToNum. Si no hi ha senyal,
    retorna None (i el resolver tracta el cas com a "desconegut" — NO inventa).
    """
    mesos = nouv_data.get("mesos_catalunya")
    if isinstance(mesos, (int, float)):
        return float(mesos)
    rng = (
        nouv_data.get("mesos_catalunya_range")
        or nouv_data.get("mesos_range")
        or ""
    )
    if isinstance(rng, str):
        mapping = {
            "Menys de 6 mesos": 3.0,
            "6-12 mesos": 9.0,
            "1-2 anys": 18.0,
            "Més de 2 anys": 30.0,
        }
        return mapping.get(rng.strip())
    return None


def _str_to_bool(v):
    if isinstance(v, bool):
        return v
    if isinstance(v, str):
        return v.lower() in ("true", "1", "sí", "si")
    return bool(v)


def resolve_params(caracteristiques: dict, etapa: str = "", curs: str = "",
                   override_mecr: str = None) -> dict:
    """
    Calcula {mecr, dua, motiu} canònic per a un perfil.

    Args:
        caracteristiques: dict {key: {actiu, ...subvars}} amb la mateixa
            estructura que arriba al backend (vegeu toBackendProfile).
        etapa: una de "infantil" | "primaria" | "ESO" | "batxillerat" | "FP".
            Cadena buida vol dir "no facilitada" — el resolver intenta
            inferir-la del curs i ho loggeja al motiu.
        curs: codi canònic del curs ("I5", "1r ESO", "1r Batxillerat"...).
            Cadena buida -> s'usa només l'etapa via fallback.
        override_mecr: si el docent ha triat un MECR manual al formulari,
            preval sobre tot el càlcul (és la voluntat explícita del docent).

    Returns:
        {
            "mecr": str (un de MECR_ORDER),
            "dua": "Acces" | "Core" | "Enriquiment",
            "motiu": "explicació pas a pas separada per ' · '",
            "trace": [pas_1, pas_2, ...]  # mateix contingut, en llista
        }
    """
    chars = caracteristiques or {}
    trace = []

    # ── 0) Override explícit del docent: sagrat ──
    if override_mecr and override_mecr in MECR_ORDER:
        mecr = override_mecr
        trace.append(f"override docent -> {mecr}")
        dua = _resolve_dua(chars, mecr)
        trace.append(f"DUA -> {dua}")
        return {"mecr": mecr, "dua": dua, "motiu": " · ".join(trace), "trace": trace}

    # ── 1) MECR base segons curs canònic, amb fallback per etapa ──
    mecr_base = COURSE_TO_MECR.get(curs)
    if mecr_base:
        trace.append(f"curs '{curs}' -> base {mecr_base}")
    elif etapa in ETAPA_FALLBACK_MECR:
        mecr_base = ETAPA_FALLBACK_MECR[etapa]
        trace.append(f"sense curs canònic, fallback etapa '{etapa}' -> {mecr_base}")
    else:
        mecr_base = "B1"
        trace.append("sense etapa ni curs -> fallback global B1")

    # ── 2) Condicions actives ──
    actives = {k for k, v in chars.items() if isinstance(v, dict) and v.get("actiu")}

    # Llista de candidats que poden modificar el MECR. Sempre comencem amb base.
    candidats = [mecr_base]

    # ── 3) Nouvingut ──
    if "nouvingut" in actives:
        nv = chars.get("nouvingut", {})
        mesos = _mesos_to_num(nv)
        alfabet_no_llati = nv.get("alfabet_llati") is False
        # El docent pot haver fixat MECR explícit al subform de nouvingut.
        nv_mecr_explicit = nv.get("mecr") if nv.get("mecr") in MECR_ORDER else None

        # REGLA RECTORA: a etapa infantil, nouvingut -> pre-A1 SEMPRE.
        # Lectura emergent compartida adult/infant. Independent dels mesos.
        # Aquest és el fix crític del cas Petri.
        if etapa == "infantil":
            candidats.append("pre-A1")
            trace.append("infantil + nouvingut -> pre-A1 (lectura emergent compartida)")
        elif nv_mecr_explicit:
            candidats.append(nv_mecr_explicit)
            trace.append(f"nouvingut.mecr explícit -> {nv_mecr_explicit}")
        elif mesos is not None:
            if mesos < 6:
                # <6 mesos: A1 amb alfabet llatí, pre-A1 amb alfabet no llatí
                cand = "pre-A1" if alfabet_no_llati else "A1"
                trace.append(
                    f"nouvingut <6 mesos, alfabet "
                    f"{'no-llatí' if alfabet_no_llati else 'llatí'} -> candidat {cand}"
                )
            elif mesos < 12:
                cand = "A1"
                trace.append("nouvingut 6-12 mesos -> candidat A1")
            elif mesos < 24:
                cand = "A2"
                trace.append("nouvingut 12-24 mesos -> candidat A2")
            else:
                cand = mecr_base
                trace.append(f"nouvingut >24 mesos -> manté base {mecr_base}")
            candidats.append(cand)
        else:
            # FIX cas Petri: ABANS el frontend forçava 'A2' aquí.
            # Ara, sense informació de mesos, NO inventem: el MECR base mana.
            trace.append("nouvingut sense mesos coneguts -> no modifica base")

    # ── 4) DI / TDL ──
    if "di" in actives:
        grau = chars.get("di", {}).get("grau", "lleu")
        cand = {"sever": "A1", "moderat": "A2", "lleu": "B1"}.get(grau, "B1")
        candidats.append(cand)
        trace.append(f"DI grau {grau} -> candidat {cand}")
    if "tdl" in actives:
        grau = chars.get("tdl", {}).get("grau", "lleu")
        cand = {"sever": "A1", "moderat": "A2", "lleu": "B1"}.get(grau, "B1")
        candidats.append(cand)
        trace.append(f"TDL grau {grau} -> candidat {cand}")

    # ── 5) Disc. auditiva LSC ──
    if "discapacitat_auditiva" in actives or "disc_auditiva" in actives:
        key = "discapacitat_auditiva" if "discapacitat_auditiva" in actives else "disc_auditiva"
        if chars.get(key, {}).get("comunicacio") == "LSC":
            candidats.append("A1")
            trace.append("disc. auditiva LSC -> candidat A1 (català escrit com a L2)")

    # ── 6) Vulnerabilitat: -1 nivell sobre la base (no sobre el mínim) ──
    if "vulnerabilitat" in actives:
        idx = MECR_ORDER.index(mecr_base)
        cand = MECR_ORDER[max(0, idx - 1)]
        candidats.append(cand)
        trace.append(f"vulnerabilitat -> -1 sobre base ({mecr_base} -> {cand})")

    # ── 7) Resolució: el MÉS BAIX guanya (regla del més restrictiu) ──
    mecr = min(candidats, key=lambda m: MECR_ORDER.index(m) if m in MECR_ORDER else 99)
    trace.append(f"més restrictiu de {candidats} -> {mecr}")

    # ── 8) AACC sense 2e: +1 nivell sobre el resultat ──
    ac = chars.get("altes_capacitats", {})
    if "altes_capacitats" in actives and not _str_to_bool(ac.get("doble_excepcionalitat")):
        idx = MECR_ORDER.index(mecr)
        prev = mecr
        mecr = MECR_ORDER[min(len(MECR_ORDER) - 1, idx + 1)]
        trace.append(f"AACC sense 2e -> +1 ({prev} -> {mecr})")

    # ── 8.5) CLAMP INFANTIL: regla rectora MALL ──
    # A etapa infantil, tota lectura és Emergent (compartida amb adult).
    # Cap condició pot pujar el MECR. L'AACC d'I5 expressa el seu repte via
    # les instruccions PERFIL del catàleg, no via MECR més alt.
    if etapa == "infantil" and mecr != "pre-A1":
        trace.append(f"clamp infantil -> pre-A1 (era {mecr}; tota lectura infantil és Emergent)")
        mecr = "pre-A1"

    # ── 9) DUA segons MECR final + condicions ──
    dua = _resolve_dua(chars, mecr)
    trace.append(f"DUA -> {dua}")

    return {"mecr": mecr, "dua": dua, "motiu": " · ".join(trace), "trace": trace}


def _resolve_dua(chars: dict, mecr_sortida: str) -> str:
    """Calcula el DUA: Acces / Core / Enriquiment."""
    actives = {k for k, v in chars.items() if isinstance(v, dict) and v.get("actiu")}

    di_grau = chars.get("di", {}).get("grau", "")
    tea_nivell = chars.get("tea", {}).get("nivell_suport", 0)
    try:
        tea_nivell = int(tea_nivell)
    except (TypeError, ValueError):
        tea_nivell = 0
    tdl_grau = chars.get("tdl", {}).get("grau", "")
    nv_alfabet = chars.get("nouvingut", {}).get("alfabet_llati", True)
    ac_doble = _str_to_bool(
        chars.get("altes_capacitats", {}).get("doble_excepcionalitat", False)
    )

    if (
        (di_grau == "sever" and "di" in actives)
        or (tea_nivell >= 3 and "tea" in actives)
        or (tdl_grau == "sever" and "tdl" in actives)
        or (mecr_sortida == "pre-A1" and not nv_alfabet and "nouvingut" in actives)
    ):
        return "Acces"

    if "altes_capacitats" in actives and not ac_doble:
        return "Enriquiment"

    return "Core"


# ─────────────────────────────────────────────────────────────────────────
# Smoke tests inline (executar amb `python -m adaptation.params_resolver`)
# ─────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    def _check(label, got, expected_mecr, expected_dua=None):
        ok_m = got["mecr"] == expected_mecr
        ok_d = (expected_dua is None) or got["dua"] == expected_dua
        status = "OK " if (ok_m and ok_d) else "FAIL"
        print(f"  [{status}] {label}: mecr={got['mecr']} dua={got['dua']}")
        if not ok_m:
            print(f"           -> esperava mecr={expected_mecr}")
        if expected_dua is not None and not ok_d:
            print(f"           -> esperava dua={expected_dua}")
        print(f"           motiu: {got['motiu']}")
        return ok_m and ok_d

    print("\n=== smoke tests adaptation/params_resolver.py ===\n")
    all_ok = True

    # Cas Petri I5 — el bug arrel
    all_ok &= _check(
        "Petri I5 + nouvingut Urdú (alfabet no-llatí, mesos desconeguts)",
        resolve_params(
            {
                "nouvingut": {"actiu": True, "l1": "urdú", "alfabet_llati": False,
                              "mesos_catalunya_range": "1-2 anys"},
                "tdah": {"actiu": True},
            },
            etapa="infantil", curs="I5",
        ),
        expected_mecr="pre-A1",
        expected_dua="Acces",  # alfabet no llatí + pre-A1 + nouvingut -> Acces
    )

    # El Viatger — 1r ESO nouvingut 2 mesos
    all_ok &= _check(
        "El Viatger 1r ESO + nouvingut 2 mesos (no infantil)",
        resolve_params(
            {"nouvingut": {"actiu": True, "mesos_catalunya": 2, "alfabet_llati": True}},
            etapa="ESO", curs="1r ESO",
        ),
        expected_mecr="A1",  # 2 mesos + alfabet llatí -> A1
        expected_dua="Core",
    )

    # Cas que abans donava A2 (bug)
    all_ok &= _check(
        "Nouvingut ESO sense mesos coneguts -> NO ha de caure a A2 hardcoded",
        resolve_params(
            {"nouvingut": {"actiu": True, "l1": "àrab", "alfabet_llati": False}},
            etapa="ESO", curs="1r ESO",
        ),
        expected_mecr="B1",  # base ESO; no podem afirmar A2 sense mesos
    )

    # I5 sense condicions
    all_ok &= _check(
        "I5 sense condicions",
        resolve_params({}, etapa="infantil", curs="I5"),
        expected_mecr="pre-A1", expected_dua="Core",
    )

    # 4t ESO AACC -> B2 -> C1
    all_ok &= _check(
        "4t ESO AACC pura",
        resolve_params(
            {"altes_capacitats": {"actiu": True}},
            etapa="ESO", curs="4t ESO",
        ),
        expected_mecr="C1", expected_dua="Enriquiment",
    )

    # 3r Primària DI moderat -> A2 (mecr base A1 + DI moderat A2 = mínim A1)
    all_ok &= _check(
        "3r Primària DI moderat",
        resolve_params(
            {"di": {"actiu": True, "grau": "moderat"}},
            etapa="primaria", curs="3r Primària",
        ),
        expected_mecr="A1",  # min(A1 base, A2 DI) = A1
    )

    # 2e: AACC + dislèxia -> no s'aplica el +1 d'AACC
    all_ok &= _check(
        "2e (AACC + dislèxia)",
        resolve_params(
            {"altes_capacitats": {"actiu": True, "doble_excepcionalitat": True},
             "dislexia": {"actiu": True}},
            etapa="ESO", curs="2n ESO",
        ),
        expected_mecr="B1",  # base sense +1 perquè 2e
    )

    # Override sagrat
    all_ok &= _check(
        "Override del docent guanya sobre tot",
        resolve_params(
            {"nouvingut": {"actiu": True, "mesos_catalunya": 1}},
            etapa="ESO", curs="1r ESO", override_mecr="B2",
        ),
        expected_mecr="B2",
    )

    # Curs no canònic + etapa coneguda
    all_ok &= _check(
        "Curs no canònic -> fallback etapa",
        resolve_params({}, etapa="ESO", curs="curs estrany"),
        expected_mecr="B1",
    )

    # Sense etapa ni curs
    all_ok &= _check(
        "Sense etapa ni curs -> fallback global",
        resolve_params({}, etapa="", curs=""),
        expected_mecr="B1",
    )

    # Vulnerabilitat 2n Primària
    all_ok &= _check(
        "Vulnerabilitat 2n Primària",
        resolve_params(
            {"vulnerabilitat": {"actiu": True}},
            etapa="primaria", curs="2n Primària",
        ),
        expected_mecr="pre-A1",  # A1 base - 1 = pre-A1
    )

    # Auditiva LSC
    all_ok &= _check(
        "3r ESO + sord LSC",
        resolve_params(
            {"discapacitat_auditiva": {"actiu": True, "comunicacio": "LSC"}},
            etapa="ESO", curs="3r ESO",
        ),
        expected_mecr="A1",
    )

    # ── Regla rectora MALL: infantil sempre pre-A1 (Miquel 2026-05-15) ──
    all_ok &= _check(
        "I5 catalanoparlant sense condicions -> pre-A1 (regla rectora)",
        resolve_params({}, etapa="infantil", curs="I5"),
        expected_mecr="pre-A1",
    )
    all_ok &= _check(
        "I5 catalanoparlant + AACC -> pre-A1 (NO puja a A1 per AACC)",
        resolve_params(
            {"altes_capacitats": {"actiu": True}},
            etapa="infantil", curs="I5",
        ),
        expected_mecr="pre-A1",  # AACC infantil expressa repte via catàleg PERFIL, no MECR
    )
    all_ok &= _check(
        "I5 nouvingut amb >24 mesos -> pre-A1 (NO puja a A2 per temps)",
        resolve_params(
            {"nouvingut": {"actiu": True, "mesos_catalunya": 36}},
            etapa="infantil", curs="I5",
        ),
        expected_mecr="pre-A1",
    )
    all_ok &= _check(
        "I3 amb DI sever -> pre-A1 + DUA Acces",
        resolve_params(
            {"di": {"actiu": True, "grau": "sever"}},
            etapa="infantil", curs="I3",
        ),
        expected_mecr="pre-A1",
        expected_dua="Acces",
    )

    print("\n", "TOTS OK" if all_ok else "HI HA FALLS", "\n")
