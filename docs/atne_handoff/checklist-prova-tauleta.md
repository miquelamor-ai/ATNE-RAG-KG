# Checklist de prova — ATNE Editorial Cream (tauleta)

Prova sencera del flux responsive a tauleta (~768–1024px). Marca cada item que vagi bé amb `[x]`.

**URL base**: `https://<cloud-run-url>/ui/atne/`

---

## 0. Preparació

- [ ] Obres la URL en un navegador amb la finestra a amplada **900–1024px** (tauleta apaïsada).
- [ ] Si pots, obre també en una segona finestra a **390–640px** (mòbil) per comparar.
- [ ] Si alguna cosa falla, marca amb `[ ]` i afegeix una nota breu al costat.

---

## 1. Pas 1 — Per a qui adaptem avui? (`pas1.html`)

### Layout
- [ ] Rail esquerre estret amb icones (Inici / Perfils actiu / Textos / Biblioteca / Preferències).
- [ ] Topbar: stepper centrat "1 Perfil (actiu fons fosc) · 2 Entrada · 3 Resultat", títol "Per a qui adaptem avui?", avatar docent "E" (lavanda AACC) a la dreta.
- [ ] Input de cerca amb placeholder "Cerca per nom, curs, condició…".
- [ ] Fila de xips filtre: Tots 32, Persones, Grups, TDAH, Dislèxia, Català L2, AACC. Cadascun amb dot de color semàntic.
- [ ] Botó "Ordre: Últim ús" a la dreta.
- [ ] Subcapçalera "Recents · 6" i llista de 6 files amb avatars i xips.
- [ ] Subcapçalera "Tots els altres · 26" amb més files.
- [ ] FABs a baix-dreta: "Cercar perfil" (actiu dark), "Nova persona" (to tan), "Nou grup" (to lavanda).

### Interaccions
- [ ] Clic al xip "TDAH" el ressalta i (visualment) deixaria filtrar la llista.
- [ ] Clic a la fila de **Marc Ribera** → navega a Pas 2.
- [ ] Clic al FAB "Nova persona" → canvia a mode formulari amb camps (Nom, Curs, Nivell MECR, Conductes, etc.).
- [ ] Clic al FAB "Nou grup" → canvia a mode formulari de grup.
- [ ] Clic al FAB "Cercar perfil" torna a la llista.
- [ ] Clic al step "2 Entrada" del stepper → navega a Pas 2.

---

## 2. Pas 2 — El text original (`pas2.html`)

### Layout
- [ ] Rail esquerre visible.
- [ ] Sidebar 200–220px amb label "PER A QUI" + card blanca de Marc Ribera:
  - [ ] Avatar circular "M" vermell TDAH.
  - [ ] Nom "Marc Ribera" serif, subtítol "14 anys · 3r ESO A" mono.
  - [ ] Xips "TDAH" + "B1 · Intermedi".
  - [ ] Secció "CONDUCTES OBSERVADES" amb 3 items.
  - [ ] Secció "AJUTS QUE ACTIVA EL PERFIL" amb 4 items.
  - [ ] Botó "Canviar perfil" a baix.
- [ ] Topbar: botó hamburguesa (invisible a tauleta), títol "ATNE", stepper "✓1 · 2 Text (actiu fosc) · 3", botó ajuda.
- [ ] Títol document editable "La Revolució Industrial" (serif) + meta "Desat · 52 paraules".
- [ ] Tab bar de modes (4 icones): llapis (Escriure actiu fosc), fletxa-amunt (Pujar), espurnes (Generar), rellotge (Recuperar).
- [ ] Card blanca amb textarea amb el text demo de la Revolució Industrial.
- [ ] Comptador "52 PARAULES" a la cantonada inferior-dreta del textarea.
- [ ] Pills d'opcions: MATÈRIA Història · NIVELL ESO 4 · COMPLEMENTS Cap.
- [ ] Frail dret (pill vertical blanca) amb 4 icones + separador + pill primari blau "Adaptar" (fletxa dreta).

### Interaccions
- [ ] Clic al tab **Pujar fitxer** → la card canvia a drop zone amb icona, "Arrossega un fitxer..." i formats admesos.
- [ ] Clic al tab **Generar** → la card canvia a formulari amb "Tema o tòpic" + 4 selects (Gènere/Tipologia/To/Extensió) + botó "Generar text".
- [ ] Clic al tab **Recuperar** → la card canvia a cerca + filter pills + llista de 4 documents recents.
- [ ] Tornes al tab **Escriure** i el text segueix allà.
- [ ] Si buides el textarea, els botons del frail (Edició, Refinar, Accions) i el botó Adaptar es desactiven visualment. "Complements" manté l'aparença normal.
- [ ] Si escrius al textarea, tots tornen a estat normal.
- [ ] Clic al frail "Adaptar" → navega a Pas 3.
- [ ] Clic al step "1 Per a qui" → torna a Pas 1.
- [ ] Clic al botó "Canviar perfil" → (funcionalitat no implementada, però no ha de petar).

---

## 3. Pas 3 — L'adaptació (`pas3.html`)

### Layout
- [ ] Rail esquerre visible.
- [ ] Sidebar esquerra amb label "PER A QUI" + card de Marc (igual que Pas 2) + botó "Tornar al text".
- [ ] Topbar: hamburguesa (amagat a tauleta), "ATNE", stepper "✓1 · ✓2 · 3 Adaptacions (actiu fosc)", botons ajuda/compartir.
- [ ] Center-head: input doc-title "La Revolució Industrial" + badge "Desat" verd + meta "adaptat fa 1m · 318 paraules" + botons undo/redo.
- [ ] Segona fila: xips complements (Glossari/Esquema/Preguntes amb dots d'estat + Afegir) + botó "Comparar amb l'original".
- [ ] Targeta blanca gran central amb el text adaptat en serif (H1 + H2 + paràgrafs amb marques groc/verd).
- [ ] Frail dret amb 4 icones (Refinar/Rúbrica/Nova adaptació/Exportar) + separador + botó primari Exportar.

### Interaccions bàsiques
- [ ] Clic al xip **Glossari** → la card central canvia a una llista de termes.
- [ ] Clic al xip **Esquema** → la card canvia a una graella de nodes.
- [ ] Clic al xip **Preguntes** → la card canvia a una llista de preguntes generades.
- [ ] Clic al botó "Comparar amb l'original" → la card es parteix en 2 columnes (original + adaptat).
- [ ] Clic al botó "Tornar al text" del sidebar → torna a Pas 2.
- [ ] Clic al step "1 Per a qui" → torna a Pas 1.
- [ ] Clic al step "2 Text" → torna a Pas 2.

### Eines d'edició del frail
- [ ] Clic al frail "Refinar" (icona sliders) → obre popover amb 3 steppers (Llargada/Simplificar/To) + checkbox "Revisar català" + àrea de text + botó "Aplicar i regenerar".
- [ ] Clic al frail "Refer amb rúbrica" → popover amb 5 checkboxes + textarea + botó "Regenerar".
- [ ] Clic al frail "Nova adaptació" → popover de confirmació amb botó "Nova adaptació".
- [ ] Clic al frail "Exportar" → popover amb 5 opcions (PDF / Word / Google Docs / Imatge / Imprimir).
- [ ] Clic fora d'un popover → es tanca.
- [ ] Tecla `Esc` → tanca el popover actiu.

### Eines sobre el text adaptat
- [ ] Selecciones un fragment de text dins de la targeta → apareix una **selection toolbar** flotant sobre la selecció amb botons (Simplificar/Explicar/Sinònim/Glossari + separador + B/I/U/H2/UL).
- [ ] Clic a "Simplificar" dins la selection toolbar → apareix overlay "Regenerant…" durant ~1.5s i la selecció es marca amb classe `.ins` (fons clar).
- [ ] Clic a "B" (bold) amb text seleccionat → el text es posa en negreta.
- [ ] Passes el cursor sobre un paràgraf → apareix un **handle de 3 punts** a l'esquerra.
- [ ] Clic al handle → menú contextual amb "Reescriure més senzill", "Dividir en frases curtes", "Afegir un exemple", "Marcar com a important", "Eliminar paràgraf".
- [ ] Clic a "Dividir en frases curtes" → overlay "Dividint…" i canvi al text.

### Undo/Redo
- [ ] `Cmd/Ctrl+Z` → desfà l'última acció (restaura text).
- [ ] `Cmd/Ctrl+Shift+Z` → refà.
- [ ] Botons undo/redo de la topbar reflecteixen l'estat (actius/desactivats segons pila).

### Regeneració (aplicació real, no només visual)
- [ ] Cap acció de regenerar envia una crida real al LLM. **Ara mateix tot és mock**: l'overlay apareix 1.5s i restaura/modifica text amb lògica de client. **Aquesta és la feina pendent crítica** (Fase 5).

---

## 4. Drawer mòbil (opcional, si proves finestra estreta)

Redimensiona la finestra per sota de 640px d'amplada:

- [ ] Rail esquerre desapareix.
- [ ] Apareix botó hamburguesa a l'esquerra de la topbar.
- [ ] Clic al hamburguesa → drawer lateral obert amb 5 entrades (Inici/Perfils/Textos/Biblioteca/Preferències).
- [ ] L'entrada corresponent al pas actual està ressaltada amb `.on` (fons lavanda clar).
- [ ] Clic al backdrop fosc → tanca drawer.
- [ ] Clic a la X (dreta de la capçalera del drawer) → tanca drawer.
- [ ] Tecla Esc → tanca drawer.
- [ ] Clic a una entrada del drawer → navega al pas i tanca el drawer.

---

## 5. Responsive — redimensionament de la finestra

- [ ] A **>1024px** (escriptori): rail, sidebars i frail tots visibles. El layout és el del prototip desktop original.
- [ ] A **768–1024px** (tauleta): rail, sidebar i frail encara visibles, però amb mides lleugerament reduïdes.
- [ ] A **<640px** (mòbil): rail i sidebar amagats, frail substituït per bottom tab bar (a Pas 2 i Pas 3), hamburguesa visible.
- [ ] Al transicionar entre mides, cap element "peta" visualment (res desbordant, res solapant-se).

---

## 6. Problemes coneguts

Aquests ja estan identificats — **no cal marcar-los**, només verificar si els observes:

- **Selection toolbar al Pas 3 mòbil**: dissenyada per a desktop, a mòbil el navegador natiu mostra la seva pròpia toolbar que tapa la nostra. Funciona bé al desktop/tauleta.
- **Bottom tab bar del Pas 3 mòbil** — els botons deleguen al frail via onclick, però el frail està amagat a mòbil. Possible que els clicks no disparin els popovers. **Cal testar.**
- **Paragraph handle a mòbil**: surt a `:hover`, que no existeix al mòbil. No és accessible sense long-press. **Cal implementar.**
- **Pas 2 — modes Pujar/Generar/Recuperar a tauleta**: només mostren els mocks visuals (drop zone, formulari, llista). Cap d'ells és funcional encara.
- **LLM**: totes les crides són mocks amb `setTimeout`. Cap petició real a `server.py`.
- **Persistència**: cap estat es guarda entre passos. El Marc del Pas 1 i el Marc del Pas 2 són hardcoded independentment.

---

## Observacions lliures

_Afegeix aquí qualsevol detall que hagis detectat, capturat, o vulguis recordar (colors que fallen, textos que desborden, atalls que no responen, etc.)_

-
-
-
