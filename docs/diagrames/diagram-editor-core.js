/* ATNE editor-extension — NUCLI PUR de mutacions de markdown (testable a node)
   Tota operació d'edició estructural = transformació de l'string markdown.
   La font única es manté; el render es recalcula després. */
(function (root) {
  'use strict';

  function indentOf(line) { var m = line.match(/^(\s*)/); return m ? m[1].length : 0; }
  function isItem(line) { return /^\s*-\s+/.test(line); }

  // Última línia del subarbre que arrenca a lineIdx (descendents = sagnia més gran)
  function subtreeEnd(md, lineIdx) {
    var lines = md.split('\n'), base = indentOf(lines[lineIdx] || ''), i = lineIdx + 1;
    while (i < lines.length && (lines[i].trim() === '' ? false : indentOf(lines[i]) > base) && isItem(lines[i])) i++;
    return i - 1;
  }

  function classify(md, lineIdx) {
    var lines = md.split('\n'), line = lines[lineIdx] || '';
    if (!isItem(line)) return null;
    var bold = /^\s*-\s+\*\*.+\*\*\s*$/.test(line);
    if (indentOf(line) === 0) return 'root';
    return bold ? 'prop' : 'concept';
  }

  function insertAt(md, afterIdx, indent, label, bold) {
    var lines = md.split('\n');
    var text = ' '.repeat(indent) + '- ' + (bold ? '**' + label + '**' : label);
    lines.splice(afterIdx + 1, 0, text);
    return { md: lines.join('\n'), newLineIdx: afterIdx + 1 };
  }

  // Fill: després del subarbre del node, sagnia+2
  function addChild(md, lineIdx, label, bold) {
    var lines = md.split('\n');
    return insertAt(md, subtreeEnd(md, lineIdx), indentOf(lines[lineIdx]) + 2, label, !!bold);
  }
  // Germà: després del subarbre, mateixa sagnia (conserva la negreta si el node és prop)
  function addSibling(md, lineIdx, label) {
    var lines = md.split('\n');
    var bold = classify(md, lineIdx) === 'prop';
    return insertAt(md, subtreeEnd(md, lineIdx), indentOf(lines[lineIdx]), label, bold);
  }
  function deleteSubtree(md, lineIdx) {
    var lines = md.split('\n'), end = subtreeEnd(md, lineIdx);
    lines.splice(lineIdx, end - lineIdx + 1);
    return { md: lines.join('\n'), removed: end - lineIdx + 1 };
  }
  function descendantCount(md, lineIdx) { return subtreeEnd(md, lineIdx) - lineIdx; }
  function nodeCount(md) { return md.split('\n').filter(isItem).length; }

  // ── Operacions de textarea (toolbar) ──
  function shiftLines(text, selStart, selEnd, dir) {
    var lines = text.split('\n'), pos = 0, out = [], a = -1, b = -1;
    for (var i = 0; i < lines.length; i++) {
      var lineStart = pos, lineEnd = pos + lines[i].length;
      if (a === -1 && selStart <= lineEnd) a = i;
      if (selEnd >= lineStart) b = i;
      pos = lineEnd + 1;
    }
    for (i = 0; i < lines.length; i++) {
      if (i >= a && i <= b && lines[i].trim() !== '') {
        out.push(dir > 0 ? '  ' + lines[i] : lines[i].replace(/^ {1,2}/, ''));
      } else out.push(lines[i]);
    }
    return out.join('\n');
  }
  function wrapSelection(text, selStart, selEnd, marker) {
    var sel = text.slice(selStart, selEnd) || 'text';
    var m = marker.length;
    // Cas 1: la selecció INCLOU els marcadors (**hola** seleccionat sencer) -> treure'ls
    if (sel.length >= m * 2 && sel.slice(0, m) === marker && sel.slice(-m) === marker) {
      var rep = sel.slice(m, sel.length - m);
      return { text: text.slice(0, selStart) + rep + text.slice(selEnd),
               selStart: selStart, selEnd: selStart + rep.length };
    }
    // Cas 2: la selecció està ENVOLTADA pels marcadors (l'usuari selecciona només la paraula) -> treure'ls
    var before = text.slice(Math.max(0, selStart - m), selStart);
    var after  = text.slice(selEnd, selEnd + m);
    var surrounded = before === marker && after === marker;
    // Guard cursiva: comptem la tirada d'asteriscs a cada banda. Exactament 2
    // = negreta pura (no hi ha cursiva a treure); 1 o 3+ = la cursiva hi és.
    if (surrounded && marker === '*') {
      var rb = 0, ra = 0, i;
      for (i = selStart - 1; i >= 0 && text[i] === '*'; i--) rb++;
      for (i = selEnd; i < text.length && text[i] === '*'; i++) ra++;
      if (rb === 2 || ra === 2) surrounded = false;
    }
    if (surrounded) {
      return { text: text.slice(0, selStart - m) + sel + text.slice(selEnd + m),
               selStart: selStart - m, selEnd: selStart - m + sel.length };
    }
    // Cas 3: embolcallar (la selecció queda sobre el text, sense els marcadors)
    return { text: text.slice(0, selStart) + marker + sel + marker + text.slice(selEnd),
             selStart: selStart + m, selEnd: selStart + m + sel.length };
  }

  root.ATNE_EDIT_CORE = { indentOf: indentOf, subtreeEnd: subtreeEnd, classify: classify,
    addChild: addChild, addSibling: addSibling, deleteSubtree: deleteSubtree,
    descendantCount: descendantCount, nodeCount: nodeCount,
    shiftLines: shiftLines, wrapSelection: wrapSelection };
})(typeof window !== 'undefined' ? window : globalThis);

/* ─── ENLLAÇOS CREUATS (graf Novak) — nucli pur, testable ─── */
(function (root) {
  'use strict';
  var C = root.ATNE_EDIT_CORE;
  var HEADER = /^-\s*Enlla[çc]os creuats\s*:?\s*$/i;

  // Separa el markdown en {tree: string, cross: [{from,to,link,raw}]}
  function splitCross(md) {
    var lines = md.split('\n'), h = -1;
    for (var i = 0; i < lines.length; i++) if (HEADER.test(lines[i].trim())) { h = i; break; }
    if (h === -1) return { tree: md, cross: [], headerIdx: -1 };
    var tree = lines.slice(0, h).join('\n').replace(/\s+$/, '');
    var cross = [];
    for (var j = h + 1; j < lines.length; j++) {
      var t = lines[j].trim();
      if (!t) continue;
      // format:  - Origen -> Destí : paraula d'enllaç
      var m = t.match(/^-\s*(.+?)\s*->\s*(.+?)\s*:\s*(.+)$/);
      if (m) cross.push({ from: m[1].trim(), to: m[2].trim(), link: m[3].trim(), raw: lines[j] });
    }
    return { tree: tree, cross: cross, headerIdx: h };
  }

  // Afegeix un enllaç creuat (per etiquetes de node). Retorna nou md.
  function addCross(md, fromLabel, toLabel, link) {
    var s = splitCross(md);
    var line = '  - ' + fromLabel + ' -> ' + toLabel + ' : ' + link;
    if (s.headerIdx === -1) {
      return md.replace(/\s+$/, '') + '\n\n- Enllaços creuats:\n' + line;
    }
    return md.replace(/\s+$/, '') + '\n' + line;
  }

  function removeCross(md, idx) {
    var s = splitCross(md);
    if (idx < 0 || idx >= s.cross.length) return md;
    var lines = md.split('\n');
    var target = s.cross[idx].raw;
    var out = lines.filter(function (l) { return l !== target; });
    // si ja no queda cap enllaç, treu la capçalera
    var rest = splitCross(out.join('\n'));
    if (!rest.cross.length && rest.headerIdx !== -1) {
      out = out.filter(function (l, i) { return i !== rest.headerIdx; });
    }
    return out.join('\n').replace(/\n{3,}/g, '\n\n').replace(/\s+$/, '');
  }

  // Quan es reanomena un node, actualitza les referències als enllaços creuats
  function renameInCross(md, oldLabel, newLabel) {
    var s = splitCross(md);
    if (!s.cross.length) return md;
    var lines = md.split('\n');
    return lines.map(function (l) {
      if (!HEADER.test(l.trim()) && /->/.test(l) && /:/.test(l)) {
        var m = l.match(/^(\s*-\s*)(.+?)(\s*->\s*)(.+?)(\s*:\s*)(.+)$/);
        if (m) {
          var f = m[2].trim() === oldLabel ? newLabel : m[2];
          var t = m[4].trim() === oldLabel ? newLabel : m[4];
          return m[1] + f + m[3] + t + m[5] + m[6];
        }
      }
      return l;
    }).join('\n');
  }

  // Canvia la paraula d'enllaç d'un enllaç creuat (per índex dins splitCross.cross)
  function updateCrossLink(md, idx, newLink) {
    var s = splitCross(md);
    if (idx < 0 || idx >= s.cross.length) return md;
    var target = s.cross[idx].raw;
    var lines = md.split('\n');
    for (var i = 0; i < lines.length; i++) {
      if (lines[i] === target) {
        var m = lines[i].match(/^(\s*-\s*.+?\s*->\s*.+?\s*:\s*)(.+)$/);
        if (m) lines[i] = m[1] + newLink;
        break;
      }
    }
    return lines.join('\n');
  }

  C.splitCross = splitCross;
  C.addCross = addCross;
  C.removeCross = removeCross;
  C.updateCrossLink = updateCrossLink;
  C.renameInCross = renameInCross;
})(typeof window !== 'undefined' ? window : globalThis);
