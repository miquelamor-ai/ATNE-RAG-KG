# Taxonomia A1 de variables, paràmetres i indicacions per a l'adaptació de textos i materials didàctics

## Propòsit

Aquest document recull un llistat ampli i estructurat de variables que es poden considerar en adaptar textos i materials didàctics, amb especial atenció a la lectura fàcil, la complexitat textual, l'accessibilitat cognitiva i el Disseny Universal per a l'Aprenentatge (DUA).

La taxonomia està pensada per servir com a base exportable per a corpus, metadades, esquemes JSON, etiquetes de prompt i polítiques d'adaptació.

## Principis de disseny

Les guies de lectura fàcil recomanen llenguatge clar, frases curtes, estructura visible, coherència terminològica i eliminació d'ambigüitats innecessàries.

Les orientacions DUA indiquen que els materials s'han de dissenyar amb múltiples formes de representació, suport a la comprensió i opcions de personalització segons la variabilitat de l'alumnat.

La guia de W3C sobre usabilitat per a persones amb dificultats cognitives i d'aprenentatge reforça la necessitat de claredat, consistència, reducció de distraccions i suport visual funcional.

## Domini 1. Variables lingüístiques del text

| Codi | Variable | Definició funcional | Valors/exemples | Indicacions associades |
|---|---|---|---|---|
| TXT_SENT_LEN | Longitud de frase | Nombre de paraules per frase | curta, mitjana, llarga; max15, max20, max25 | fes frases curtes; una idea per frase |
| TXT_SENT_COMPLEX | Complexitat sintàctica | Presència de subordinació, incisos, passives, impersonals | baixa, mitjana, alta | redueix subordinades; evita passiva |
| TXT_SEGMENT | Segmentació interna | Separació clara entre frases i unitats de sentit | alta o baixa | separa idees; usa puntuació simple |
| TXT_LEX_FREQ | Freqüència lèxica | Proporció de paraules d'ús freqüent | alta, mixta, baixa | usa vocabulari freqüent |
| TXT_TERM_DENS | Densitat terminològica | Quantitat de termes especialitzats per tram de text | baixa, mitjana, alta | redueix tecnicismes; defineix termes |
| TXT_ABSTRACT | Grau d'abstracció lèxica | Percentatge de paraules abstractes vs concretes | concret, mixt, abstracte | concreta; dona exemples |
| TXT_POLYSEMY | Polisèmia | Presència de mots amb múltiples significats | baixa, mitjana, alta | evita mots ambigus; especifica |
| TXT_IDIOM | Idiomatismes i frases fetes | Expressions figurades o culturals | absent, moderat, alt | elimina metàfores i frases fetes |
| TXT_ACRONYM | Acrònyms i sigles | Quantitat d'abreviacions no explicades | baixa, mitjana, alta | desplega sigles la primera vegada |
| TXT_CONNECT | Connectors | Ús de connectors lògics i temporals | explícit, parcial, implícit | afegeix connectors clars |
| TXT_REF_CLEAR | Claredat referencial | Facilitat per identificar referents de pronoms i demostratius | alta, mitjana, baixa | substitueix pronoms per noms quan calgui |
| TXT_TOPIC_STAB | Estabilitat temàtica | Grau en què el tema principal es manté clar al paràgraf | alta, baixa | una idea central per paràgraf |
| TXT_TERM_CONS | Consistència terminològica | Manteniment del mateix terme per al mateix concepte | alta, baixa | no canviïs el terme si el concepte és el mateix |
| TXT_REGISTER | Registre | Distància entre llenguatge acadèmic i llengua quotidiana | quotidià, escolar, acadèmic | baixa el registre si cal |
| TXT_FORMALITY | Formalitat | Grau de formalitat discursiva | baixa, mitjana, alta | fes-lo proper però correcte |
| TXT_DIRECT | Directivitat | Grau d'explicitud en instruccions i missatges | baix, mitjà, alt | dona instruccions directes i clares |

## Domini 2. Variables macrotextuals i d'estructura

| Codi | Variable | Definició funcional | Valors/exemples | Indicacions associades |
|---|---|---|---|---|
| MACRO_GENRE | Gènere discursiu | Tipus de text/discurs | narratiu, expositiu, instructiu, argumentatiu, oral, multimodal | adapta segons gènere discursiu |
| MACRO_LENGTH | Extensió total | Volum total de text | micro, curt, mitjà, llarg | escurça o fragmenta |
| MACRO_HEAD | Jerarquia de títols | Existència i claredat de títols i subtítols | clara, parcial, absent | afegeix títols descriptius |
| MACRO_PARA | Longitud de paràgraf | Densitat i mida del paràgraf | curt, mitjà, dens | un paràgraf per idea |
| MACRO_SUM_PRE | Resum previ | Presència d'orientació inicial | sí/no | afegeix de què va el text |
| MACRO_SUM_POST | Resum final | Presència de síntesi final | sí/no | tanca amb idees clau |
| MACRO_LIST | Llistes i enumeracions | Transformació de blocs densos en llistes | alta, moderada, baixa | converteix enumeracions en vinyetes |
| MACRO_STEP | Seqüenciació | Presentació dels passos en ordre clar | explícita, parcial, implícita | numera passos |
| MACRO_SIGNAL | Senyalització | Ús de destacats i marques per idees clau | alta, mitjana, baixa | destaca què és important |

## Domini 3. Variables semàntiques i de contingut

| Codi | Variable | Definició funcional | Valors/exemples | Indicacions associades |
|---|---|---|---|---|
| SEM_CONCEPT_LOAD | Càrrega conceptual | Nombre de conceptes nous rellevants per unitat | baixa, mitjana, alta | redueix conceptes nous per bloc |
| SEM_BACKGROUND | Coneixement previ requerit | Dependència de sabers previs disciplinaris o culturals | baix, mitjà, alt | activa coneixement previ; afegeix context |
| SEM_CULT | Càrrega cultural | Referències culturals, institucionals o locals | baixa, mitjana, alta | explica referents culturals |
| SEM_INFER | Exigència inferencial | Quant depèn d'inferències no dites | baixa, mitjana, alta | fes explícit allò implícit |
| SEM_CAUSE | Estructura causal | Presència de relacions causa-efecte complexes | simple, moderada, complexa | separa causes i efectes |
| SEM_COMPARE | Comparació i contrast | Complexitat de comparacions entre elements | baixa, mitjana, alta | presenta comparacions en taula o llista |
| SEM_EMO | Càrrega emocional | Intensitat emocional o sensibilitat del contingut | baixa, moderada, alta | usa to prudent i segur |

## Domini 4. Variables de presentació i layout

| Codi | Variable | Definició funcional | Valors/exemples | Indicacions associades |
|---|---|---|---|---|
| LAY_LINE_LEN | Longitud de línia | Nombre aproximat de caràcters per línia | curta, òptima, llarga | manté línies llegibles; evita línies massa llargues |
| LAY_SPACING | Espaiat | Interlineat i espai entre blocs | estret, adequat, ampli | augmenta espaiat entre paràgrafs |
| LAY_FONT_SIZE | Mida de lletra | Cos tipogràfic del text principal | petit, mitjà, gran | usa mida suficient |
| LAY_FONT_STYLE | Estil tipogràfic | Tipus de lletra, cursiva, negreta, majúscules | simple, carregat | evita cursiva i majúscules sostingudes |
| LAY_CONTRAST | Contrast visual | Diferència entre text i fons | baix, adequat, alt | assegura contrast suficient |
| LAY_VISUAL_DENS | Densitat visual | Quantitat d'elements simultanis en pantalla o pàgina | baixa, mitjana, alta | redueix soroll visual |
| LAY_TABLE_DENS | Densitat de taules | Complexitat de taules i matrius | baixa, mitjana, alta | simplifica o fragmenta taules |
| LAY_HIGHLIGHT | Sistema de destacats | Ús coherent de negreta, colors o caixes | coherent, irregular, absent | destaca només el que és important |

## Domini 5. Variables de suport multimodal

| Codi | Variable | Definició funcional | Valors/exemples | Indicacions associades |
|---|---|---|---|---|
| MOD_IMG_REL | Rellevància de la imatge | Grau en què la imatge ajuda a entendre el text | baixa, mitjana, alta | afegeix imatge funcional, no decorativa |
| MOD_IMG_POS | Integració text-imatge | Distància i relació entre text i suport visual | integrada, propera, separada | col·loca la imatge al costat del contingut |
| MOD_AUDIO | Suport d'àudio | Disponibilitat d'audiolectura o locució | sí/no/opcional | ofereix lectura en veu alta |
| MOD_VIDEO | Suport de vídeo | Existència de vídeo explicatiu | sí/no | afegeix vídeo curt si aporta comprensió |
| MOD_SUBS | Subtítols/transcripció | Disponibilitat de text equivalent per àudio/vídeo | sí/no | incorpora subtítols i transcripció |
| MOD_GLOSS_VIS | Glossari visual | Definicions amb suport d'icona o imatge | sí/no | crea glossari visual |

## Domini 6. Variables de relació text-tasca

| Codi | Variable | Definició funcional | Valors/exemples | Indicacions associades |
|---|---|---|---|---|
| TASK_TYPE | Tipus de tasca | Finalitat d'ús del text | lectura, resolució, estudi, producció, examen | adapta segons tasca |
| TASK_COG_LOAD | Càrrega cognitiva de la tasca | Quantitat d'operacions mentals simultànies exigides | baixa, mitjana, alta | separa llegir de respondre |
| TASK_MEM | Càrrega de memòria de treball | Quant cal retenir mentre es processa | baixa, mitjana, alta | redueix informació simultània |
| TASK_STEPS | Nombre de passos | Seqüència operativa requerida | pocs, moderats, molts | divideix en passos |
| TASK_MODEL | Presència de modelatge | Existència d'exemple resolt o resposta model | sí/no | afegeix exemple abans de l'activitat |
| TASK_SUPPORT | Escaffolding | Suports de comprensió o execució | baix, mitjà, alt | afegeix preguntes guia o pistes |
| TASK_TIME | Pressió temporal | Temps disponible i ritme de lectura o resposta | baixa, moderada, alta | preveu temps extra si cal |

## Domini 7. Variables d'accessibilitat i personalització

| Codi | Variable | Definició funcional | Valors/exemples | Indicacions associades |
|---|---|---|---|---|
| ACC_SCREEN | Compatibilitat amb lector de pantalla | Si el material es pot navegar i entendre amb tecnologies de suport | sí/no/parcial | usa estructura semàntica clara |
| ACC_KEYB | Navegació per teclat | Possibilitat d'ús sense ratolí | sí/no/parcial | garanteix focus i ordre lògic |
| ACC_RESIZE | Reescalat i zoom | Possibilitat d'augmentar text sense pèrdua funcional | sí/no/parcial | permet personalitzar mida |
| ACC_PERSONAL | Personalització | Opcions per canviar contrast, espaiat, vista o modalitat | baixa, mitjana, alta | incorpora controls personals |
| ACC_GOAL_CLEAR | Claredat d'objectius | Explicitació del que s'ha d'aprendre o fer | baixa, mitjana, alta | indica objectiu i criteri d'èxit |
| ACC_RESPONSE_MODE | Modes de resposta | Vies per mostrar l'aprenentatge | text, oral, visual, multimodal | ofereix opcions d'expressió |

## Domini 8. Variables del lector o perfil d'adaptació

| Codi | Variable | Definició funcional | Valors/exemples | Indicacions associades |
|---|---|---|---|---|
| LR_AGE | Edat/etapa | Tram evolutiu i escolar | infantil, primària, ESO, adults | ajusta exemples i registre |
| LR_READ | Nivell lector | Capacitat general de lectura | inicial, bàsic, funcional, avançat | gradua complexitat |
| LR_LANG | Nivell de llengua | Domini de la llengua vehicular | pre-A1 a C2 | adapta lèxic i sintaxi |
| LR_L1_DIST | Distància lingüística L1-L2 | Proximitat entre llengua primera i llengua del material | baixa, mitjana, alta | preveu suport addicional si hi ha distància alta |
| LR_BACKGROUND | Familiaritat amb el tema | Coneixement previ del camp o contingut | baixa, mitjana, alta | activa coneixement previ |
| LR_ATT | Perfil atencional | Facilitat per mantenir atenció sostinguda | baixa, mitjana, alta | redueix distractors i blocs llargs |
| LR_EXEC | Funcions executives | Planificació, seqüenciació i seguiment d'instruccions | baixa, mitjana, alta | explicita passos i checkpoints |
| LR_SENSORY | Preferències i necessitats sensorials | Necessitats visuals, auditives o multimodals | visual, auditiva, multimodal | ofereix modalitats diverses |
| LR_SUPPORT | Grau de suport disponible | Ajuda docent, familiar o tecnològica disponible | baix, mitjà, alt | adapta autonomia requerida |

## Famílies d'indicacions derivables

A partir d'aquesta taxonomia, les indicacions d'adaptació es poden agrupar en set famílies operatives:

- Simplificació lingüística: reduir llargada de frase, disminuir subordinació, usar lèxic freqüent, evitar ambigüitats i idiomatismes.
- Reestructuració macrotextual: afegir títols, fragmentar paràgrafs, convertir blocs en llistes, incorporar resum inicial i final.
- Clarificació semàntica: fer explícit allò implícit, explicar referents culturals, donar context i exemples.
- Adaptació de presentació: millorar line length, espaiat, contrast, tipografia i densitat visual.
- Suport multimodal: incorporar imatges funcionals, àudio, subtítols, glossaris visuals i vies alternatives de representació.
- Escaffolding de tasca: separar lectura i activitat, seqüenciar passos, afegir modelatge i preguntes guia.
- Personalització i accessibilitat: ajustar segons perfil lector, objectius, tecnologies de suport i opcions d'expressió.

## Variables prioritàries per a una primera versió de sistema

Si cal fer una primera implementació pràctica, les variables més rendibles solen ser longitud de frase, complexitat sintàctica, freqüència lèxica, densitat terminològica, estructura de títols, longitud de paràgraf, exigència inferencial, càrrega cultural, densitat visual, suport multimodal i nivell lector/lingüístic.

Aquestes variables acostumen a produir millores visibles en comprensió i usabilitat sense requerir encara una modelització molt fina de tots els perfils.

## Esquema mínim recomanat de metadades

Per a ús en corpus o agents, una fitxa mínima per material podria incloure: `tipus_text`, `nivell_lingüístic`, `nivell_lector`, `llargada_frase`, `densitat_termes`, `càrrega_cultural`, `estructura_títols`, `suport_visual`, `tipus_tasca`, `càrrega_cognitiva`, `opcions_accessibilitat` i `regles_adaptació_aplicables`.

## Notes d'ús

Aquesta taxonomia no és una rúbrica diagnòstica ni una classificació clínica, sinó un mapa de decisions de disseny i adaptació de materials.

Moltes variables no s'han d'entendre com a valors absoluts, sinó com a dimensions que es poden graduar i combinar segons context, objectiu i perfil lector.
