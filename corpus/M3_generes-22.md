---
modul: M3
titol: "Gèneres discursius — 22 sub-gèneres amb regles crítiques per adaptació"
tipus: estrategia
descripcio: "Regles d'adaptació específiques per gènere discursiu (22 sub-gèneres organitzats per tipologia SFL). Complementa M3_generes-discursius.md (4 macro-gèneres)."
review_status: esborrany
generat_at: 2026-04-19T22:00:00
---

# Gèneres discursius — 22 sub-gèneres amb regles crítiques

Aquest fitxer defineix **regles crítiques d'adaptació LF per als 22 sub-gèneres**
que apareixen al dropdown del generador d'ATNE (Pas 2). El codi `corpus_reader.py`
llegeix blocs amb encapçalament `## <key>` i extreu-ne el contingut fins al
següent `##` o final del fitxer.

**Font primària:** `docs/fitxes_generes_v1.md` (ATNE). Aquest fitxer n'extreu
només les seccions **Regles crítiques + Contraindicacions** per injectar al prompt.

**Claus:** minúscules, sense accents, tal com arriben del frontend.

---

## manual

TIPOLOGIA: Expositiva
ESTRUCTURA: títol + entradeta + apartats amb paràgrafs

REGLES CRÍTIQUES (fer):
- Progressió simple → complex: cada apartat es recolza en l'anterior.
- Desnominalitzar processos ("l'oxidació" → "quan s'oxida").
- Connectors causals explícits: "perquè", "per tant", "així doncs".
- Exemples concrets abans de l'abstracció.
- Termes tècnics sempre definits a la primera aparició, en negreta.

CONTRAINDICACIONS (NO fer):
- Apartats niats de més d'un nivell.
- Notes al peu que distreuen el flux.
- Referències a capítols posteriors ("ho veurem més endavant").
- Apel·lacions al lector adult.

---

## divulgatiu

TIPOLOGIA: Expositiva
ESTRUCTURA: títol + entradeta + desenvolupament narrativitzat

REGLES CRÍTIQUES (fer):
- Entradeta captadora però sense metàfores obscures.
- Narrativitzar el contingut (explicar com una història).
- Cites curtes amb atribució clara ("diu X, expert en Y").
- Arrodonir xifres ("més de 2 milions" enlloc de "2.347.812").

CONTRAINDICACIONS (NO fer):
- Tecnicismes sense explicar.
- Referències culturals implícites.
- Humor irònic (pot confondre).
- Frases incompletes o suspensives.

---

## informe

TIPOLOGIA: Expositiva
ESTRUCTURA: títol + resum executiu + objectiu + mètode + resultats + conclusions

REGLES CRÍTIQUES (fer):
- Resum executiu al principi (què s'ha fet i què s'ha trobat).
- Dades presentades visualment (taules, llistes) abans de la prosa.
- Conclusió destacada com a frase final prominent.
- Verbs en passat per a accions fetes; present per a conclusions.

CONTRAINDICACIONS (NO fer):
- Opinions personals barrejades amb fets.
- Conclusions que no derivin dels resultats.
- Tecnicismes sense glossari.
- Referències a lectura futura.

---

## enciclopedic

TIPOLOGIA: Expositiva
ESTRUCTURA: terme + definició nuclear + explicació ampliada + exemple

REGLES CRÍTIQUES (fer):
- Definició nuclear en una sola frase, sense subordinades.
- Evitar circularitat: no definir X usant X o paraules de la mateixa arrel.
- Exemple concret immediatament després de la definició.
- Categoria primer, especificitat després ("La balena és un mamífer gran que viu al mar").

CONTRAINDICACIONS (NO fer):
- Definicions per negació ("no és X") com a primera línia.
- Sinònims com a definició ("llibre: obra literària").
- Etimologia abans del significat.
- Referències a entrades anteriors/posteriors.

---

## descripcio

TIPOLOGIA: Expositiva / Descriptiva
ESTRUCTURA: títol + descripció general + característiques

REGLES CRÍTIQUES (fer):
- Ordre espacial explícit: de dalt a baix, de l'exterior a l'interior, etc.
- Comparacions concretes per a mides ("com una pilota de futbol").
- Evitar superlatius sintètics: "molt gran" > "grandíssim".
- Una característica per frase en nivells baixos.

CONTRAINDICACIONS (NO fer):
- Adjectius subjectius sense concretar ("molt bonic", "impressionant").
- Descripcions poètiques amb metàfores.
- Ordre aleatori de característiques.
- Barreja de descripció física i emocional.

---

## resum

TIPOLOGIA: Expositiva
ESTRUCTURA: títol + referència original + idea principal + idees secundàries

REGLES CRÍTIQUES (fer):
- Idea principal al primer paràgraf, sense preàmbul.
- Conservar la veu del text original (no interpretar).
- Connectors d'ordre lògic entre idees ("primer... després... finalment").
- No citar literalment: reformular amb vocabulari accessible.

CONTRAINDICACIONS (NO fer):
- Opinions del redactor.
- Cites textuals llargues.
- Repeticions del contingut original.
- Exemples no presents a l'original.

---

## conte

TIPOLOGIA: Narrativa
ESTRUCTURA: situació inicial → nus → resolució

REGLES CRÍTIQUES (fer):
- Cronologia lineal: no flashbacks, no salts temporals.
- Motivacions explícites: "Lluc tenia por perquè estava sol" (no inferibles).
- Emocions nomenades: "estava trist", "es va enfadar".
- Personatges principals persistents: usar els mateixos noms, no pronoms.
- Diàleg atribuït sempre: "va dir la Marta", "va preguntar en Pau".

CONTRAINDICACIONS (NO fer):
- Narrador no fiable o ambigu.
- Temps narratius barrejats (passat amb present històric).
- Referències culturals implícites.
- Finals oberts o ambigus.
- Ironia o sarcasme.

---

## fabula

TIPOLOGIA: Narrativa
ESTRUCTURA: situació + acció + desenllaç + moral explícita

REGLES CRÍTIQUES (fer):
- Moral explícita al final, no subentesa.
- Personatges arquetípics amb trets únics (la llebre ràpida, la tortuga lenta).
- Caràcters mantinguts: si un personatge és llest al principi, ho és fins al final.
- Llegendes: situar en temps i lloc reals tot i ser ficció.

CONTRAINDICACIONS (NO fer):
- Morals ambigües o debatables.
- Evolució psicològica dels personatges.
- Referències històriques no explicades (llegendes).
- Llenguatge arcaic.

---

## poema

TIPOLOGIA: Narrativa / Expressiva
ESTRUCTURA: títol + estrofes + versos

REGLES CRÍTIQUES (fer):
- Preservar estructura estròfica: no fusionar estrofes ni aplanar versos.
- No reescriure en prosa (seria un altre gènere).
- Simplificar vocabulari mantenint el ritme quan sigui possible.
- Metàfores concretes: "el sol és una taronja" > "l'astre flamíger".
- Rima: conservar-la si es pot; si no, prioritzar la claredat.

CONTRAINDICACIONS (NO fer):
- Convertir en narrativa.
- Eliminar la divisió en estrofes.
- Explicar la metàfora dins del poema (trencaria la forma).
- Afegir comentaris o notes entre versos.

---

## biografia

TIPOLOGIA: Narrativa
ESTRUCTURA: naixement → infància → fets principals → mort/llegat

REGLES CRÍTIQUES (fer):
- Ordre cronològic estricte: naixement → infància → fets → mort/llegat.
- 3-5 fets principals màxim; no llista exhaustiva.
- Dates completes: "el 15 de març de 1879", no "1879" ni "s. XIX".
- Contextualitzar lloc i època breument ("a Alemanya, fa 150 anys").
- Separar fets de llegat: primer què va fer, després per què importa.

CONTRAINDICACIONS (NO fer):
- Flashbacks ("però tornem als seus inicis...").
- Especulació ("potser pensava que...").
- Detalls íntims sense rellevància.
- Xifres romanes per a segles.

---

## noticia

TIPOLOGIA: Narrativa / Expositiva
ESTRUCTURA: titular + lead (5W) + cos (piràmide invertida)

REGLES CRÍTIQUES (fer):
- Piràmide invertida: el més important al principi.
- 5W al lead: qui, què, quan, on, per què — tots explicitats.
- Context explicat, no assumit (els lectors LF no segueixen sempre l'actualitat).
- Cites curtes amb atribució clara.
- Vocabulari no periodístic: "va morir" > "va perdre la vida".

CONTRAINDICACIONS (NO fer):
- Titulars metafòrics o amb jocs de paraules.
- Acrònims sense explicar (UE → Unió Europea).
- Referències a notícies anteriors sense context.
- Adjectius valoratius ("escandalós", "vergonyós").

---

## cronica

TIPOLOGIA: Narrativa / Testimonial
ESTRUCTURA: títol + moments ordenats cronològicament

REGLES CRÍTIQUES (fer):
- Cronologia explícita amb marcadors ("A les 9 del matí...").
- Perspectiva del cronista sempre visible: "vaig veure", "vam anar".
- Descripcions sensorials concretes (què es veu, què se sent).
- Separar fet de valoració: primer què va passar, després què va semblar.

CONTRAINDICACIONS (NO fer):
- Salts temporals (no flashback, no flash-forward).
- Opinions barrejades amb els fets.
- Especulació sobre el que altres pensaven.
- Jocs estilístics (metàfora estesa, ironia).

---

## diari

TIPOLOGIA: Narrativa / Reflexiva
ESTRUCTURA: data + entrada (què ha passat + com m'he sentit + què penso)

REGLES CRÍTIQUES (fer):
- Primera persona sempre: "he vist", "he pensat".
- Separar fets d'emocions en paràgrafs distints.
- Nomenar les emocions explícitament: "estava content", "em vaig avergonyir".
- Conclusió orientada a l'aprenentatge: "el que he après és...".

CONTRAINDICACIONS (NO fer):
- Reflexions filosòfiques abstractes.
- Dobles sentits o ironia.
- Crítiques a persones sense anonimitzar.
- Exageració dramàtica.

---

## opinio

TIPOLOGIA: Argumentativa
ESTRUCTURA: tesi + arguments amb evidència + conclusió

REGLES CRÍTIQUES (fer):
- Tesi al primer paràgraf, sense preàmbul.
- Arguments numerats o clarament separats (1 per paràgraf).
- Cada argument amb evidència concreta (dada, exemple, cita).
- Conclusió que reprèn la tesi, no n'introdueix cap d'altra.
- Connectors argumentatius explícits: "per tant", "en canvi", "a més".

CONTRAINDICACIONS (NO fer):
- Retòrica complexa (preguntes retòriques niades, paral·lelismes).
- Ironia (pot ser entesa literalment).
- Atacs personals.
- Tesis múltiples.

---

## ressenya

TIPOLOGIA: Argumentativa / Avaluativa
ESTRUCTURA: obra + descripció + valoració + recomanació

REGLES CRÍTIQUES (fer):
- Descripció abans de valoració: primer què és, després què en pensem.
- Separar fets de judicis: "la pel·lícula dura 2 hores" (fet) vs "és massa llarga" (judici).
- Recomanació concreta: "bona per a nens de 8 a 10 anys" (no "recomanable").
- Evitar spoilers: no revelar el final.

CONTRAINDICACIONS (NO fer):
- Sarcasme o ironia.
- Comparacions amb obres no conegudes pel lector.
- Llenguatge crític especialitzat sense explicar.
- Valoracions sense argument.

---

## assaig

TIPOLOGIA: Argumentativa / Reflexiva
ESTRUCTURA: introducció amb tesi + desenvolupament + conclusió

REGLES CRÍTIQUES (fer):
- Tesi clara a la introducció (no al final).
- Cada apartat desenvolupa una idea del paraigua tesi.
- Cites integrades, no decoratives: explicar per què importa la cita.
- Vocabulari acadèmic definit a la primera aparició.

CONTRAINDICACIONS (NO fer):
- Tesi implícita o ambigua.
- Digressions sense connexió amb la tesi.
- Llenguatge barroc o circumlocucions.
- Conclusions obertes ("cadascú que en pensi el que vulgui").

---

## carta

TIPOLOGIA: Argumentativa / Dialogada
ESTRUCTURA: capçalera + salutació + motiu + cos + petició + comiat + signatura

REGLES CRÍTIQUES (fer):
- Motiu al primer paràgraf: per què escrius.
- Petició concreta i única: què vols que faci el destinatari.
- Una acció per carta: no barrejar demandes.
- Registre ajustat al destinatari: formal (institució) o informal (amic).
- Frases 15-20 paraules màx, veu activa.

CONTRAINDICACIONS (NO fer):
- Fórmules arcaiques ("En prego acceptació de les més distingides salutacions").
- Introduccions llargues abans del motiu.
- Múltiples peticions barrejades.
- Abreviatures sense explicar.

---

## instructiu

TIPOLOGIA: Instructiva
ESTRUCTURA: materials + passos numerats + resultat esperat

REGLES CRÍTIQUES (fer):
- Materials en llista abans dels passos.
- Cada pas = 1 verb d'acció + 1 objecte concret.
- Ordre cronològic estricte: mai reordenar per legibilitat.
- Passos independents: cada pas s'ha de poder executar sense mirar el següent.
- Subjecte "tu" explícit quan calgui claredat.

CONTRAINDICACIONS (NO fer):
- Passos condicionals niats ("si X, fes Y; si no, fes Z").
- Passos implícits o omesos.
- Instruccions en passiva ("s'afegirà l'aigua").
- Observacions digressives al mig dels passos.

---

## receptari

TIPOLOGIA: Instructiva
ESTRUCTURA: ingredients + preparació (passos) + resultat

REGLES CRÍTIQUES (fer):
- Ingredients en ordre d'ús, no alfabètic.
- Cada pas = 1 verb d'acció + 1 objecte concret.
- No fusionar passos ("Barreja i deixa reposar" → 2 passos).
- Indicacions sensorials preferibles al temps ("fins que sigui daurat" > "5 minuts").
- Quantitats sempre explícites amb unitat (2 ous, 200 g farina).

CONTRAINDICACIONS (NO fer):
- Passatges narratius ("La meva àvia sempre deia...").
- Condicionals opcionals ("Si vols, pots afegir...").
- Valoracions subjectives ("Quedarà molt bo").
- Referències culturals implícites.

---

## reglament

TIPOLOGIA: Instructiva / Prescriptiva
ESTRUCTURA: títol + normes agrupades + conseqüències

REGLES CRÍTIQUES (fer):
- Una norma per ítem, sense conjuncions ni comes complexes.
- Veu imperativa directa: "Respecta el torn", no "S'ha de respectar el torn".
- Agrupar per tema, no per ordre d'importància.
- Conseqüències separades de les normes, en caixa específica.
- Positiu abans que negatiu: "Escolta els altres" > "No interrompis".

CONTRAINDICACIONS (NO fer):
- Normes condicionals complexes ("Si X, llavors Y, excepte quan Z").
- Justificacions dins de la norma.
- Excepcions niades.
- Llenguatge legal tècnic sense explicar.

---

## entrevista

TIPOLOGIA: Dialogada
ESTRUCTURA: presentació + parells pregunta/resposta

REGLES CRÍTIQUES (fer):
- Preguntes directes, sense subordinades: "Què fas quan estàs trist?".
- Respostes simplificades preservant la veu original (no en 3a persona).
- Marcar clarament qui parla amb etiquetes visibles.
- No linearitzar: mantenir el format P/R, no convertir en prosa.
- Explicar termes propis de l'entrevistat.

CONTRAINDICACIONS (NO fer):
- Preguntes múltiples en una ("Com et dius i què fas?").
- Preguntes retòriques.
- Intervencions intermèdies ("i llavors, vostè què va pensar...").
- Respostes sense pregunta anterior.

---

## dialeg

TIPOLOGIA: Dialogada
ESTRUCTURA: personatges + acotacions + torns de paraula

REGLES CRÍTIQUES (fer):
- Llistar personatges a l'inici amb descripció breu (1 línia).
- Atribuir cada torn amb el nom del personatge (no amb lletres/inicials).
- Acotacions al present i 3a persona: "En Joan entra a l'habitació".
- Subtext explícit: si un personatge està enfadat, nomenar-ho a l'acotació.
- Una acció per acotació, sense subordinades.

CONTRAINDICACIONS (NO fer):
- Acotacions amb ironia o judicis ("Diu amb un to evidentment fals").
- Canvis d'escena implícits (marcar-los amb apartat).
- Llenguatge teatral arcaic o elevat.
- Monòlegs interns llargs (el teatre és acció externa).
