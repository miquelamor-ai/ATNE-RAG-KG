/*
 * ATNE — help-mode.js
 * Cliques la icona ? → l'app entra en mode ajuda.
 * Cliques qualsevol element amb data-help="clau" → popover flotant.
 * Esc o 2n clic a ? → surt del mode.
 */
(function () {
  'use strict';

  var HELP = {

    /* ── Topbar compartit (totes les pàgines) ───────────── */
    'topbar-flash': {
      t: 'Mode Flash',
      d: 'El mode més ràpid: enganxa un text, tria el curs i prem Adaptar. Ideal per a adaptacions puntuals sense configurar un perfil complet.'
    },
    'topbar-taller': {
      t: 'Mode Taller',
      d: 'El mode complet: perfils guardats, complements avançats (esquema, preguntes, bastides), editor ric i comparació amb l\'original.'
    },
    'topbar-saber-ne': {
      t: 'Saber-ne+',
      d: 'Base de coneixement pedagògic d\'ATNE: marcs DUA i MECR, guies per condicions (TDAH, dislèxia, nouvinguts, AACC), gèneres discursius i bones pràctiques d\'adaptació.'
    },
    'topbar-suggerir': {
      t: 'Envia un suggeriment',
      d: 'Reporta un problema, proposa una millora o dóna feedback sobre l\'adaptació que has obtingut. El teu feedback s\'enregistra i ajuda a millorar ATNE.'
    },
    'topbar-compte': {
      t: 'El teu compte',
      d: 'Mostra el teu email de connexió (@fje.edu) i l\'opció per tancar la sessió o canviar d\'usuari.'
    },
    'topbar-steps': {
      t: 'Passos del Taller',
      d: 'Navegació entre els 3 passos del Taller: (1) Per a qui, (2) El text, (3) Adaptació. El pas actual és ressaltat; els completats permeten tornar-hi. Clica el Pas 3 des del Pas 2 per llançar l\'adaptació.'
    },

    /* ── Home ────────────────────────────────────────────── */
    'home-flash': {
      t: 'Mode Flash',
      d: 'Adaptació ràpida: enganxa el text, tria el curs i la condició i prem Adaptar. Tot en una sola pantalla. Recomanat per a les primeres proves i per a textos puntuals.'
    },
    'home-taller': {
      t: 'Mode Taller',
      d: 'Adaptació completa: perfils d\'alumne guardats, historial, editor de text ric, complements pedagògics avançats i comparació visual original vs. adaptat. Per a un ús regular i sistemàtic.'
    },
    'home-llms': {
      t: 'Entendre els LLM',
      d: 'Guia sobre els models d\'IA que ATNE utilitza: com funcionen, quines limitacions tenen, per què el text pot variar entre generacions i com interpretar els resultats.'
    },

    /* ── Pas 1: Perfils ──────────────────────────────────── */
    'cerca': {
      t: 'Cercar perfil',
      d: 'Escriu el nom, curs o condició de l\'alumne. La cerca és instantània i no distingeix majúscules ni accents.'
    },
    'filtres': {
      t: 'Filtres ràpids',
      d: 'Mostra només un subconjunt de perfils: Persones (individuals), Grups (classes), o alumnes amb una condició específica (TDAH, Dislèxia, Català L2, Altes capacitats).'
    },
    'ordenar': {
      t: 'Ordenar la llista',
      d: 'Canvia l\'ordre: "Últim ús" posa primer el perfil que has fet servir més recentment. També pots ordenar per nom alfabètic o per curs.'
    },
    'fab-persona': {
      t: 'Nou perfil de persona',
      d: 'Crea un perfil individual per a un alumne concret. Pots afegir el nom (sobrenom), curs, conductes observades i condicions. Com més informació hi poses, millors seran les adaptacions.'
    },
    'fab-grup': {
      t: 'Nou perfil de grup',
      d: 'Crea un perfil per a tota una classe. ATNE detecta els subgrups de necessitats i genera automàticament una versió del text per a cadascun.'
    },
    'sel-perfil': {
      t: 'Seleccionar aquest perfil',
      d: 'Obre el Pas 2 amb aquest alumne o grup actiu. Tot el text que adaptes tindrà en compte les seves condicions i el seu nivell lector.'
    },
    'mecr': {
      t: 'Nivell MECR',
      d: 'El Marc Europeu Comú de Referència indica el domini lector. A1-A2: textos molt senzills amb suport visual. B1: adaptació estàndard (la majoria de l\'alumnat). B2-C1: text complex amb suport puntual. Per a nouvinguts el nivell pot baixar; per a AACC pot pujar.'
    },
    'observacions': {
      t: 'Conductes observades i ajuts',
      d: 'Marca el que veus a l\'aula: ATNE ho converteix automàticament en ajuts pedagògics (fragmentació, llistes numerades, glossari…). No cal diagnòstic formal: comença pel que observes.'
    },
    'condicions': {
      t: 'Condicions i situacions',
      d: 'Les condicions permanents (TDAH, dislèxia, TEA…) activen instruccions específiques. Les situacions contextuals (nouvingut, convalescència, ritme alt) també s\'incorporen. Diverses condicions poden coexistir en un mateix alumne.'
    },

    /* ── Pas 2: El text ──────────────────────────────────── */
    'p2-perfil': {
      t: 'Perfil seleccionat',
      d: 'Mostra el nom, curs i condicions de l\'alumne per qui s\'adaptarà el text. Els ajuts que apareixen aquí s\'activaran automàticament a les instruccions de l\'IA.'
    },
    'p2-canviar': {
      t: 'Canviar de perfil',
      d: 'Torna al Pas 1 per seleccionar un altre alumne o grup. El text que has escrit o pujat es conservarà.'
    },
    'p2-tabs': {
      t: '4 maneres d\'entrar el text',
      d: 'Escriure: text directe. Pujar: extreu text d\'un PDF, Word o Markdown. Generar: l\'IA crea un text de zero sobre un tema que descrius. Recuperar: torna a carregar una adaptació anterior.'
    },
    'p2-format': {
      t: 'Eines de format',
      d: 'Estructura el text original: negreta (termes clau), títols H1/H2 (seccions), llistes. L\'adaptació respectarà l\'estructura que marquis aquí.'
    },
    'p2-text': {
      t: 'Text original',
      d: 'Enganxa o escriu el text curricular que vols adaptar. No incloguis noms ni dades identificatives de l\'alumne. Pot ser un article, exercici, enunciat, fragment de llibre de text…'
    },
    'p2-materia': {
      t: 'Matèria',
      d: 'Indica l\'assignatura (Ciències, Llengua, Matemàtiques…). Ajuda l\'IA a usar el vocabulari tècnic correcte i a mantenir el registre acadèmic adequat per a cada disciplina.'
    },
    'p2-complements': {
      t: 'Complements',
      d: 'Materials extra que es generen junt amb el text adaptat: Glossari (definicions de termes clau), Esquema (resum visual), Preguntes de comprensió (avaluació graduada per nivells), Bastides (andamiatge per a nous conceptes).'
    },
    'p2-upload': {
      t: 'Pujar un fitxer',
      d: 'Arrossega o selecciona un PDF, Word (.docx), Markdown o TXT (màx. 5 MB). ATNE n\'extreu el text i l\'adapta. Nota: les imatges incrustades als PDFs no s\'inclouen.'
    },
    'p2-generar': {
      t: 'Generar text amb IA',
      d: 'Descriu el tema i l\'IA crea un text original adaptat al nivell del perfil. Tria el gènere discursiu (manual, notícia, conte, entrevista…), el to i l\'extensió que necessites.'
    },
    'p2-frail-refinar': {
      t: 'Presets de refinament',
      d: 'Ajusta ràpidament el to, la llargada i la complexitat del text adaptat amb presets d\'un clic (simplificar, ampliar, escurçar, normalitzar català). S\'apliquen a la generació següent.'
    },
    'p2-frail-compl': {
      t: 'Triar complements',
      d: 'Selecciona quins materials extra vols generar: Glossari, Esquema, Preguntes de comprensió, Bastides. Apareixeran al Pas 3 junt amb el text adaptat.'
    },
    'p2-frail-desar': {
      t: 'Desar esborrany al servidor',
      d: 'Desa el text actual al servidor perquè el puguis recuperar des de qualsevol dispositiu amb "Recuperar". Diferent de l\'esborrany local que es desa automàticament al navegador.'
    },
    'p2-adaptar': {
      t: 'Adaptar text → Pas 3',
      d: 'Envia el text a l\'IA per adaptar-lo al perfil seleccionat. El resultat apareix en streaming al Pas 3; no cal esperar que s\'acabi per llegir-lo. El text original es conserva.'
    },

    /* ── Pas 3: Adaptació ────────────────────────────────── */
    'p3-perfil': {
      t: 'Perfil i ajuts actius',
      d: 'Mostra les condicions de l\'alumne i quins ajuts pedagògics s\'han aplicat a l\'adaptació. Expandeix la targeta per veure el detall de les instruccions activades.'
    },
    'p3-tornar': {
      t: 'Tornar al text',
      d: 'Torna al Pas 2 per editar el text original o canviar els paràmetres. Pots tornar a generar una nova adaptació quan vulguis.'
    },
    'p3-seccions': {
      t: 'Seccions del resultat',
      d: 'Navega entre el Text adaptat i els complements generats. El puntet verd = contingut disponible; groc = en generació. Clica "Afegir" per demanar un complement addicional.'
    },
    'p3-font': {
      t: 'Tipografia del text',
      d: 'Canvia la font del text adaptat i dels exports: Lexend (dislèxia / TDAH), Atkinson Hyperlegible (visió / TEA), Fraunces (AACC, textos literaris), JetBrains Mono (FP tècnic). Cada font maximitza la llegibilitat per al seu perfil.'
    },
    'p3-comparar': {
      t: 'Comparar amb l\'original',
      d: 'Veu el text original i l\'adaptat en paral·lel. Les marques de color indiquen: verd = contingut afegit (no estava a l\'original), blau = reformulació (la mateixa idea en paraules més senzilles).'
    },
    'p3-desar': {
      t: 'Desar al núvol',
      d: 'Desa l\'adaptació a la teva biblioteca personal. Podràs recuperar-la des de qualsevol dispositiu. L\'esborrany local (al navegador) es desa automàticament sense haver de clicar.'
    },
    'p3-lt': {
      t: 'Revisar català (LanguageTool)',
      d: 'Comprova l\'ortografia i la gramàtica del text adaptat. Els errors es marquen; pots acceptar o ignorar cada suggeriment. Útil per detectar incorreccions introduïdes per la IA.'
    },
    'p3-refinar': {
      t: 'Refinar l\'adaptació',
      d: 'Dona instruccions addicionals per ajustar el text: simplificar més, augmentar o reduir la llargada, canviar el to, afegir exemples. Es torna a generar conservant el perfil i el text original.'
    },
    'p3-export': {
      t: 'Exportar',
      d: 'Descarrega el text adaptat com a PDF (per imprimir o compartir) o copia al porta-retalls. El PDF inclou tots els complements actius i usa la tipografia que has triat.'
    },
    'p3-text': {
      t: 'Text adaptat',
      d: 'El resultat de l\'adaptació al perfil de l\'alumne. Les marques de color mostren on l\'IA ha afegit contingut (verd) o on ha reformulat frases (blau). Pots editar el text directament clicant al contingut.'
    },
    'p3-glossari': {
      t: 'Glossari',
      d: 'Definicions dels termes tècnics o poc freqüents, adaptades al nivell lector del perfil. S\'inclou a l\'export PDF. Pots activar o desactivar la inclusió amb el commutador de dalt.'
    },
    'p3-esquema': {
      t: 'Esquema visual',
      d: 'Resum estructurat del text en forma de jerarquia. Útil com a suport de comprensió global abans de llegir el text complet, especialment per a alumnes amb dificultats de processament.'
    },
    'p3-preguntes': {
      t: 'Preguntes de comprensió',
      d: 'Preguntes graduades en 3 nivells (literal, inferencial, crític), seguint el model MALL/TILC. Útils per a avaluació diferenciada o com a bastida de lectura guiada.'
    },
    'p3-rubric': {
      t: 'Refer amb rúbrica',
      d: 'Torna a generar l\'adaptació tenint en compte una rúbrica d\'avaluació. Pots indicar criteris específics (participació, argumentació, vocabulari) perquè l\'IA els reforci al text.'
    },
    'p3-regen': {
      t: 'Nova adaptació',
      d: 'Genera una adaptació alternativa des de zero: mateixa text original i perfil, però l\'IA la reescriu de nou. Útil quan el resultat no és el que esperaves o vols una versió diferent.'
    },
    'p3-chip-text': {
      t: 'Text adaptat',
      d: 'Torna a la vista principal del text adaptat. Si estàs veient un complement (glossari, esquema, preguntes), clica aquí per tornar al text.'
    },
    'p3-chip-add': {
      t: 'Afegir complement',
      d: 'Demana a l\'IA un complement addicional que no s\'ha generat automàticament: glossari, esquema, preguntes o bastides. Es genera i s\'afegeix a la vista.'
    },
    'p3-sel-tb': {
      t: 'Eines IA sobre selecció',
      d: 'Selecciona text i usa aquestes eines per modificar-ne un fragment concret: Simplificar (reescriure més senzill), Explicar (definir el concepte), Sinònim (alternatives de vocabulari), Glossari (afegir la paraula al glossari).'
    },
    'p3-para-menu': {
      t: 'Accions sobre el paràgraf',
      d: 'Menú d\'accions per al paràgraf on has clicat: Reescriure més senzill, Dividir en frases curtes, Afegir un exemple, Ressaltar concepte clau. S\'apliquen sols a aquest fragment.'
    },

    /* ── Flash ───────────────────────────────────────────── */
    'fl-curs': {
      t: 'Curs',
      d: 'Selecciona el curs de l\'alumne o del grup. Determina el vocabulari, la complexitat sintàctica i les convencions curriculars del text adaptat.'
    },
    'fl-tipus': {
      t: 'Per a qui: Grup o Alumne',
      d: 'Grup: genera una versió estàndard del curs, simplificada o enriquida per a tota la classe. Alumne: genera una versió personalitzada per a un alumne concret amb una condició específica.'
    },
    'fl-carregar': {
      t: 'Carregar perfil desat',
      d: 'Recupera un perfil d\'alumne que has desat anteriorment. Evita repetir la configuració per als alumnes que adaptes sovint. Els perfils es desen localment al navegador.'
    },
    'fl-condicio': {
      t: 'Adaptació del text',
      d: 'Per a un grup: tria el nivell estàndard del curs, versió simplificada (més accessible) o enriquida (més profunditat). Per a un alumne: selecciona la condició (TDAH, dislèxia, nouvingut, AACC, etc.).'
    },
    'fl-l1': {
      t: 'Llengua materna de l\'alumne',
      d: 'Per a alumnes nouvinguts: indica la seva L1 (àrab, amazic, urdú…). Ajuda l\'IA a triar estructures sintàctiques i exemples que facin la transició al català més natural.'
    },
    'fl-complements': {
      t: 'Complements',
      d: 'Materials que es generaran junt amb el text adaptat: Glossari (definicions dels termes tècnics), Preguntes (comprensió graduada), Resum (síntesi en punts clau). Activats per defecte; clica per desactivar-ne.'
    },
    'fl-textarea': {
      t: 'Text a adaptar',
      d: 'Enganxa o escriu el text curricular que vols adaptar. No incloguis noms ni dades identificatives. Màxim 12.000 caràcters (~1.800 paraules). Pot ser en qualsevol format: article, exercici, enunciat, fragment de llibre…'
    },
    'fl-idioma': {
      t: 'Llengua de sortida',
      d: 'L\'idioma en el qual es generarà el text adaptat. Per defecte, català. Si el text original és en castellà i vols l\'adaptació en castellà, canvia-ho aquí.'
    },
    'fl-adaptar': {
      t: 'Adaptar text',
      d: 'Envia el text a l\'IA. L\'adaptació es genera en temps real (streaming): pots llegir el resultat mentre s\'escriu, sense esperar que acabi. L\'adaptació apareix al panell de la dreta.'
    },
    'fl-desar-perfil': {
      t: 'Desa com a perfil',
      d: 'Guarda la configuració actual (curs, condició, L1) com a perfil amb nom. La propera vegada el podràs carregar directament amb "Carrega un perfil desat".'
    },
    'fl-font': {
      t: 'Tipografia',
      d: 'Canvia la font del text adaptat: Lexend (dislèxia/TDAH), Atkinson (visió/TEA), Fraunces (textos literaris), Inter (general), OpenDyslexic (dislèxia severa). La font s\'aplica també als exports.'
    },
    'fl-original': {
      t: 'Mostrar text original',
      d: 'Expandeix o col·lapsa el text original per comparar-lo amb l\'adaptat sense sortir de la pantalla. Útil per verificar que no s\'ha perdut contingut essencial.'
    },
    'fl-sec-glossari': {
      t: 'Glossari',
      d: 'Definicions dels termes tècnics del text, adaptades al nivell de l\'alumne. Clica per expandir. S\'inclou a l\'export PDF.'
    },
    'fl-sec-preguntes': {
      t: 'Preguntes de comprensió',
      d: 'Preguntes de comprensió sobre el text adaptat, graduades per nivell. Clica per expandir. S\'inclouen a l\'export PDF.'
    },
    'fl-sec-resum': {
      t: 'Resum',
      d: 'Síntesi del text adaptat en punts clau. Útil com a suport de comprensió global. Clica per expandir. S\'inclou a l\'export PDF.'
    },
    'fl-copiar': {
      t: 'Copiar al porta-retalls',
      d: 'Copia el text adaptat (i els complements visibles) al porta-retalls. Pots enganxar-lo directament a Word, Google Docs, Classroom o qualsevol altra eina.'
    },
    'fl-pdf': {
      t: 'Descarregar com a PDF',
      d: 'Descarrega el text adaptat i els complements actius com un PDF amb la tipografia triada, llest per imprimir o compartir digitalment.'
    },
    'fl-refer': {
      t: 'Tornar a generar',
      d: 'Genera una nova adaptació des de zero amb el mateix text i configuració. Útil si el resultat no és el que esperaves o vols una alternativa diferent.'
    },
    'fl-desar': {
      t: 'Desar a la biblioteca',
      d: 'Desa l\'adaptació actual a la biblioteca del núvol. Podràs recuperar-la des de qualsevol dispositiu amb el botó Historial.'
    },
    'fl-editar': {
      t: 'Editar el text',
      d: 'Activa l\'edició manual del text adaptat: pots corregir incorreccions, afegir exemples o ajustar el contingut abans d\'imprimir o compartir.'
    },
    'fl-historial': {
      t: 'Biblioteca d\'adaptacions',
      d: 'Consulta i recupera les adaptacions que has desat anteriorment. Pots buscar per data, perfil o contingut.'
    }
  };

  var active = false;
  var popEl = null;
  var bannerEl = null;
  var POP_W = 320;
  var POP_GAP = 10; // separació entre l'element i el popover (fa lloc a la fletxa)

  function getOrCreatePop() {
    if (popEl) return popEl;
    var el = document.createElement('div');
    el.id = 'help-pop';
    el.className = 'help-pop';
    el.setAttribute('role', 'tooltip');
    el.innerHTML =
      '<button class="help-pop-x" aria-label="Tancar ajuda">' +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" width="11" height="11">' +
          '<path d="M18 6 6 18M6 6l12 12"/>' +
        '</svg>' +
      '</button>' +
      '<div class="help-pop-t"></div>' +
      '<div class="help-pop-d"></div>';
    el.querySelector('.help-pop-x').addEventListener('click', function (e) {
      e.stopPropagation();
      hidePop();
    });
    document.body.appendChild(el);
    popEl = el;
    return el;
  }

  function showPop(key, anchor) {
    var data = HELP[key];
    if (!data) return;
    var pop = getOrCreatePop();
    pop.querySelector('.help-pop-t').textContent = data.t;
    pop.querySelector('.help-pop-d').textContent = data.d;

    // Reset abans de mesurar (per recalcular l'animació en cada show)
    pop.classList.remove('pop-below', 'pop-above');
    pop.style.animation = 'none';
    pop.style.display = 'block';
    /* eslint-disable no-unused-expressions */ pop.offsetHeight; /* reflow */
    pop.style.animation = '';

    var rect = anchor.getBoundingClientRect();
    var margin = 12;
    var anchorCx = rect.left + rect.width / 2;

    // Horitzontal: centrat sobre l'ancoratge, retallat al viewport
    var left = anchorCx - POP_W / 2;
    left = Math.max(margin, Math.min(left, window.innerWidth - POP_W - margin));

    var estH = pop.offsetHeight || 140;
    var spaceBelow = window.innerHeight - rect.bottom;
    var spaceAbove = rect.top;

    // Decideix sota/sobre segons quin costat té més espai
    var below = spaceBelow >= estH + POP_GAP + margin || spaceBelow > spaceAbove;
    var top = below ? (rect.bottom + POP_GAP) : (rect.top - estH - POP_GAP);
    top = Math.max(margin, Math.min(top, window.innerHeight - estH - margin));

    // Posició relativa de la fletxa dins el popover (respecte el centre de l'ancoratge)
    var arrowX = anchorCx - left;
    arrowX = Math.max(18, Math.min(arrowX, POP_W - 18));

    pop.style.setProperty('--pop-arrow-x', arrowX + 'px');
    pop.style.setProperty('--pop-origin', arrowX + 'px ' + (below ? '0' : '100%'));
    pop.classList.add(below ? 'pop-below' : 'pop-above');
    pop.style.left = left + 'px';
    pop.style.top = top + 'px';
  }

  function hidePop() {
    if (popEl) popEl.style.display = 'none';
  }

  function showBanner() {
    if (bannerEl) return;
    var el = document.createElement('div');
    el.className = 'help-banner';
    el.setAttribute('role', 'status');
    el.innerHTML =
      '<span class="help-banner-dot" aria-hidden="true"></span>' +
      '<span>Mode ajuda · clica un element per saber-ne més</span>' +
      '<kbd>Esc</kbd>' +
      '<button class="help-banner-x" aria-label="Sortir del mode ajuda">' +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M18 6 6 18M6 6l12 12"/></svg>' +
      '</button>';
    el.querySelector('.help-banner-x').addEventListener('click', function (e) {
      e.stopPropagation();
      toggle();
    });
    document.body.appendChild(el);
    bannerEl = el;
  }

  function hideBanner() {
    if (bannerEl) {
      bannerEl.remove();
      bannerEl = null;
    }
  }

  function findHelp(el) {
    var node = el;
    var limit = 8;
    while (node && node !== document.body && limit-- > 0) {
      if (node.dataset && node.dataset.help) return { key: node.dataset.help, el: node };
      node = node.parentElement;
    }
    return null;
  }

  function toggle() {
    active = !active;
    document.body.classList.toggle('help-mode', active);
    var btn = document.getElementById('help-mode-btn');
    if (btn) {
      btn.classList.toggle('active', active);
      btn.title = active
        ? 'Sortir del mode ajuda (Esc)'
        : 'Ajuda contextual: clica qualsevol element';
    }
    if (active) {
      showBanner();
    } else {
      hidePop();
      hideBanner();
    }
    if (window.ATNE_TRACK) ATNE_TRACK.event('help_mode_toggle', { active: active });
  }

  document.addEventListener('click', function (e) {
    if (!active) return;
    if (e.target.closest('#help-mode-btn')) return;
    if (e.target.closest('#help-pop')) return;       // clic dins popover: ignorar
    if (e.target.closest('.help-banner')) return;    // clic a la pill: ignorar

    var found = findHelp(e.target);
    if (found) {
      e.preventDefault();
      e.stopPropagation();
      showPop(found.key, found.el);
    } else {
      hidePop();
    }
  }, true);

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && active) toggle();
  });

  window.helpMode = { toggle: toggle };
})();
