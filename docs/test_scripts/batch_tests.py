"""Test batch: executa tests end-to-end de gèneres contra Cloud Run.

Ús intern per validar la integració dels 22 gèneres. No forma part del pilot."""
import json, urllib.request, concurrent.futures, time

URL = 'https://atne-1050342211642.europe-west1.run.app/api/adapt'

TESTS = [
    # (id, genere, mecr, perfil_key, text)
    ('noticia_retest', 'noticia', 'B1', 'tdah',
     """Descoberta una nova especie de granota al Montseny

18 d'abril de 2026 — Un equip de biolegs ha identificat una nova especie al Parc Natural del Montseny. L'animal, batejat Rana montsenyensis, mesura 3-5 cm i te pell verda amb taques marrons.

El descobriment arriba despres de tres anys d'investigacio. La doctora Elena Marti afirma que podria haver estat confosa amb la Rana temporaria durant decades.

"Es un recordatori de la riquesa biologica encara per descobrir", diu Marti. Demanen protegir l'habitat per l'escalfament global."""),

    ('cronica', 'cronica', 'B1', 'dislexia',
     """Cronica del viatge a Roma

Dilluns 14 d'abril. Vam arribar a Roma a les 10 del mati despres de 3 hores d'avio. Feia sol i els carrers eren plens de gent.

Dimarts 15. Vam visitar el Colosseu i el Forum Roma. El guia ens va explicar que el Colosseu tenia cabuda per a 50.000 persones. Va ser impressionant.

Dimecres 16. Anada al Vatica: Capella Sixtina i Basilica de Sant Pere. Els frescos de Miquel Angel em van deixar sense paraules.

Dijous 17. Vam tornar a casa amb les motxilles plenes de records. Roma ens ha canviat una mica."""),

    ('manual', 'manual', 'A2', 'nouvingut',
     """El sistema solar

El sistema solar es el conjunt format pel Sol i els cossos que l'orbiten. Hi ha 8 planetes principals: Mercuri, Venus, Terra, Mart, Jupiter, Saturn, Urans i Neptu.

Els planetes es divideixen en dos grups. Els planetes rocosos son els mes propers al Sol: Mercuri, Venus, Terra i Mart. Son petits i tenen la superficie solida.

Els planetes gasosos son els mes llunyans: Jupiter, Saturn, Urans i Neptu. Son molt grans i estan formats principalment de gas.

A mes dels planetes, el sistema solar conte asteroides, cometes i planetes nans com Pluto."""),

    ('divulgatiu', 'divulgatiu', 'B1', 'nouvingut',
     """Per que el cel es blau?

Quan la llum del sol entra a l'atmosfera, xoca amb les molecules d'aire. La llum blanca del sol en realitat esta feta de tots els colors de l'arc de Sant Marti.

El cientific Lord Rayleigh va descobrir al segle XIX que la llum blava es dispersa mes que els altres colors perque te una longitud d'ona mes curta. Per tant, quan mirem al cel, veiem aquesta llum blava dispersada en totes direccions.

Al cap vespre, la llum ha de travessar mes atmosfera per arribar-nos, i la llum blava ja ha estat dispersada abans. Per aixo veiem colors rojos i taronges.

"La fisica de la llum es una de les mes belles que hi ha", deia Einstein."""),

    ('informe', 'informe', 'B1', 'altes_capacitats',
     """Informe sobre la qualitat de l'aire a Barcelona (2025)

Objectiu: Mesurar la qualitat de l'aire en 10 punts de la ciutat durant 2025.

Metode: Hem installat sensors de NO2, PM2.5 i ozo. Hem pres mesures cada hora durant tot l'any.

Resultats:
- La concentracio mitjana de NO2 ha estat de 42 µg/m3 (limit legal 40).
- Les zones mes contaminades: Eixample i Poblenou.
- Les zones menys contaminades: Sarria-Sant Gervasi.
- El trafic es la principal font d'emissions.

Conclusions: Barcelona supera el limit de NO2 en 6 dels 10 punts. Cal reduir el trafic al centre urba."""),

    ('enciclopedic', 'enciclopedic', 'A2', 'nouvingut',
     """Fotosintesi

Proces biologic pel qual les plantes, algues i alguns bacteris transformen la llum solar en energia quimica. Es produeix principalment a les fulles, en uns organuls anomenats cloroplasts, gracies a un pigment verd anomenat clorofilla.

La fotosintesi converteix el dioxid de carboni (CO2) i l'aigua (H2O) en glucosa (C6H12O6) i allibera oxigen (O2). L'equacio simplificada es: 6CO2 + 6H2O + llum -> C6H12O6 + 6O2.

Es fonamental per a la vida a la Terra perque produeix l'oxigen que respirem i forma la base de gairebe totes les cadenes alimentaries."""),

    ('descripcio', 'descripcio', 'A2', 'tea',
     """La platja de Sant Sebastia

La platja de Sant Sebastia es a la Barceloneta, a Barcelona. Es una platja llarga de sorra fina i daurada.

A la dreta hi ha el port, ple de vaixells. A l'esquerra hi ha un passeig amb palmeres i terrasses. Al fons es veu el mar blau, amb vaixells petits al lluny.

L'aigua esta neta i no es molt freda a l'estiu. La sorra te grans petits i es calentona pel sol. Sovint hi ha gent fent esport: voleibol, correguda, ioga.

A sobre de la sorra hi ha gandules, para-sols i castells de sorra que fan els nens."""),

    ('resum', 'resum', 'B1', 'tdah',
     """Resum: article "L'impacte de les xarxes socials en els adolescents" (M. Pons, 2024)

L'autora analitza com l'us de xarxes socials com Instagram i TikTok afecta els adolescents entre 12 i 17 anys. Segons un estudi amb 2.000 joves catalans, el 78% les utilitza mes de 3 hores diaries.

Pons conclou que aquest us excessiu te tres efectes principals: disminucio de la concentracio academica, increment de l'ansietat i deteriorament de les relacions presencials.

L'autora recomana limitar l'us a 1-2 hores diaries, fomentar activitats offline i formar docents i families en l'educacio digital."""),

    ('diari', 'diari', 'A2', 'tea',
     """Dijous 18 d'abril

Avui a l'escola hem fet una sortida al Museu de Ciencies. Hem agafat l'autobus a les 9 del mati. Erem tota la classe, 23 alumnes, i dues mestres.

Al museu hi havia molts experiments per tocar. A mi m'ha agradat especialment el que feia llampecs de debo. Tambe he vist dinosaures de mida real.

Al principi tenia una mica de por pel soroll, pero despres m'he acostumat. He menjat amb els companys al pati del museu.

Quan he tornat a casa, estava cansat pero content. Tenia ganes d'explicar-ho tot a la mare."""),

    ('ressenya', 'ressenya', 'B1', 'altes_capacitats',
     """Ressenya de "El nom del vent", de Patrick Rothfuss (2007)

Aquesta novel·la fantastica explica la vida de Kvothe, un noi que esdeve una llegenda vivent. El llibre es el primer de la triologia "Cronica de l'Assassi de Reis".

La historia esta ben construida: Rothfuss alterna el present del Kvothe adult amb el seu passat turmentat, creant tensio des del principi. El sistema de magia basat en la "simpatia" es original i coherent.

Tanmateix, alguns passatges son excessivament llargs i la segona meitat del llibre perd ritme. A mes, el segon llibre no va arribar mai a l'alcada del primer.

Recomanable per a lectors que gaudeixin amb sagues extenses i no tinguin pressa."""),

    ('assaig', 'assaig', 'B2', 'altes_capacitats',
     """El dret a l'oblit digital

Vivim en una era en que tot queda gravat a internet per sempre. Un tuit escrit als 15 anys pot perseguir-nos als 40. Aquest fenomen planteja una pregunta etica fonamental: tenim dret a ser oblidats?

El Tribunal de Justicia de la UE va establir el 2014 el "dret a l'oblit": els ciutadans poden demanar a Google que elimini resultats sobre la seva persona que ja no siguin rellevants. Aquesta sentencia defensa que la memoria eterna de la xarxa viola la nostra dignitat.

Tanmateix, aquest dret topa amb la llibertat d'informacio. Si eliminem cada error del passat, com podem preservar la memoria historica?

Com deia Nietzsche, l'oblit es una forma de salut. Sense oblidar no podem avançar. Pero oblidar-ho tot tampoc no ens fa lliures."""),

    ('instructiu', 'instructiu', 'A2', 'nouvingut',
     """Com plantar una llavor de mongeta

Materials: un got de plastic, terra, una llavor de mongeta, aigua.

Passos:
1. Omple el got de plastic de terra fins a la meitat.
2. Fes un forat petit al mig amb el dit, de 2 cm de profunditat.
3. Posa la llavor de mongeta dins el forat.
4. Cobreix la llavor amb un poc de terra.
5. Afegeix aigua fins que la terra estigui humida.
6. Posa el got en un lloc on tingui llum solar directa.

Resultat: En 5-7 dies veuras una planta verda sortint de la terra. Rega-la cada dia amb una mica d'aigua."""),

    ('reglament', 'reglament', 'A2', 'dislexia',
     """Normes de la biblioteca escolar

La biblioteca es un espai d'estudi i lectura per a tots. Les seguents normes garanteixen que tothom pugui aprofitar-la.

Per treballar be:
- Manten el silenci a la sala de lectura.
- Apaga el mobil abans d'entrar.
- No menjis ni beguis al costat dels llibres.
- Tanca bé els llibres abans de tornar-los.

Per utilitzar els llibres:
- Registra't al taulell abans de treure un llibre.
- Torna el llibre abans de 15 dies.
- Si perds o fas malbe un llibre, parla amb la bibliotecaria.

Si no compleixes les normes, la bibliotecaria et recordara que has de fer. Si passa diverses vegades, es parlara amb la familia."""),
]

PROFILES = {
    'nouvingut': {'caracteristiques': {'nouvingut': {'actiu': True, 'mecr': 'A2'}}},
    'tdah': {'caracteristiques': {'tdah': {'actiu': True, 'mecr': 'B1'}}},
    'tea': {'caracteristiques': {'tea': {'actiu': True, 'mecr': 'A2'}}},
    'dislexia': {'caracteristiques': {'dislexia': {'actiu': True, 'mecr': 'B1'}}},
    'altes_capacitats': {'caracteristiques': {'altes_capacitats': {'actiu': True, 'mecr': 'B2'}}},
}

CONTEXTS = {
    'A2': {'etapa': 'Primaria', 'curs': '4t Primaria', 'materia': 'llengua'},
    'B1': {'etapa': 'ESO', 'curs': '2n ESO', 'materia': 'llengua'},
    'B2': {'etapa': 'Batxillerat', 'curs': '1r Batx', 'materia': 'llengua'},
}


def run_test(test_id, genere, mecr, perfil, text):
    payload = {
        'text': text,
        'profile': PROFILES[perfil],
        'context': CONTEXTS[mecr],
        'params': {'mecr_sortida': mecr, 'levels': ['single'], 'genere_discursiu': genere, 'complements': {}},
        'docent_id': f'test-batch-{test_id}'
    }
    req = urllib.request.Request(URL,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'})
    t0 = time.time()
    adapted = None
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            for line in resp:
                line = line.decode('utf-8').strip()
                if line.startswith('data: '):
                    try:
                        ev = json.loads(line[6:])
                        if ev.get('type') == 'result':
                            adapted = ev.get('adapted', '')
                        elif ev.get('type') == 'done':
                            break
                    except: pass
    except Exception as e:
        return test_id, None, str(e), time.time() - t0
    return test_id, adapted, None, time.time() - t0


def main():
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(run_test, *t): t[0] for t in TESTS}
        for fut in concurrent.futures.as_completed(futures):
            test_id = futures[fut]
            r = fut.result()
            results[test_id] = r
            status = 'OK' if r[1] else 'FAIL'
            print(f'[{status}] {test_id} ({r[3]:.1f}s)')

    # Escriure resultats a un fitxer
    out_path = 'docs/test_scripts/batch_results.md'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('# Resultats batch tests gèneres\n\n')
        for test_id, adapted, err, elapsed in results.values():
            f.write(f'## {test_id}\n\n')
            f.write(f'**Temps:** {elapsed:.1f}s\n\n')
            if err:
                f.write(f'**Error:** {err}\n\n')
                continue
            if adapted:
                # Extreure nomes el "## Text adaptat"
                parts = adapted.split('##')
                if len(parts) >= 2:
                    f.write('```\n##' + parts[1].strip() + '\n```\n\n')
    print(f'\nResultats a: {out_path}')


if __name__ == '__main__':
    main()
