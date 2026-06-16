/* ═══ ATNE editor-extension v0.2 (PROTOTIP) — +/× contextual, undo/redo, toolbar, xuleta, preview ═══ */
(function () {
  'use strict';
  var C = window.ATNE_EDIT_CORE;
  var MECR_RANGES = { 'A2': [4,6], 'B1': [6,8], 'B2': [8,12] };
  var state = { mecr: 'B1', undo: [], redo: [], lastLine: null, cont: null, type: 'mapa_conceptual' };

  function md() { return state.cont.dataset.md; }
  function refreshBtns() {
    document.getElementById('btn-undo').disabled = !state.undo.length;
    document.getElementById('btn-redo').disabled = !state.redo.length;
  }
  function setMd(newMd, opts) {
    state.undo.push(md());
    if (state.undo.length > 80) state.undo.shift();
    state.redo = [];                      // una acció nova invalida el refés
    state.cont.dataset.md = newMd;
    rerender(); updateBadge(); syncTextarea(); refreshBtns();
    if (opts && opts.openLine != null) setTimeout(function () { openPopupFor(opts.openLine); }, 80);
  }
  function undo() {
    if (!state.undo.length) return;
    state.redo.push(md());
    state.cont.dataset.md = state.undo.pop();
    rerender(); updateBadge(); syncTextarea(); refreshBtns();
  }
  function redo() {
    if (!state.redo.length) return;
    state.undo.push(md());
    state.cont.dataset.md = state.redo.pop();
    rerender(); updateBadge(); syncTextarea(); refreshBtns();
  }
  var _lastLabels = null;
  function rerender() {
    state.cont.classList.remove('mermaid-active');
    state.cont.innerHTML = '';
    window.ATNE_MERMAID.renderMermaidBlock(state.cont, md(), state.type);
  }
  function openPopupFor(lineIdx) {
    var g = state.cont.querySelector('g[data-line="' + lineIdx + '"]');
    if (g) g.dispatchEvent(new MouseEvent('click', { bubbles: true }));
  }

  function updateBadge() {
    var n = C.nodeCount(md()), r = MECR_RANGES[state.mecr] || [6,8];
    var b = document.getElementById('mecr-badge');
    b.textContent = n + ' nodes · recomanat ' + r[0] + '–' + r[1] + ' per a ' + state.mecr;
    b.className = 'badge' + (n > r[1] ? ' over' : (n < r[0] ? ' under' : ''));
  }

  // ── Botons contextuals injectats al popup d'edició existent ──
  document.addEventListener('click', function (e) {
    var t = e.target;
    while (t && t.nodeType === 1 && !(t.hasAttribute && t.hasAttribute('data-nid'))) t = t.parentElement;
    if (t && t.nodeType === 1 && t.hasAttribute('data-nid')) {
      state.lastLine = parseInt(t.getAttribute('data-line'), 10);
      state.lastLabel = t.getAttribute('data-lbl') || '';
      setTimeout(injectButtons, 70);
    }
  }, true);

  function mkBtn(label, title, cls, fn) {
    var b = document.createElement('button');
    b.type = 'button'; b.textContent = label; b.title = title;
    b.className = 'popup-ext-btn' + (cls ? ' ' + cls : '');
    b.addEventListener('click', function (ev) { ev.stopPropagation(); fn(); });
    return b;
  }
  function closePopup() { var p = document.getElementById('atne-node-popup'); if (p) p.remove(); }
  function addPropAndConcept(li) {
    var r1 = C.addChild(md(), li, 'enlla\u00e7', true);
    var r2 = C.addChild(r1.md, r1.newLineIdx, 'Nou concepte');
    closePopup(); state.lastLine = null;
    setMd(r2.md, { openLine: r1.newLineIdx });
  }

  function injectButtons() {
    var pop = document.getElementById('atne-node-popup');
    if (!pop || pop.querySelector('.popup-ext-btn') || state.lastLine == null) return;
    var li = state.lastLine, kind = C.classify(md(), li);
    var bar = document.createElement('div');
    bar.style.cssText = 'display:flex;gap:5px;margin-left:6px;padding-left:8px;border-left:1px solid #e9d5ff';

    if (kind === 'root') {
      bar.appendChild(mkBtn('+ proposició', 'Nova branca: paraula d\u2019enlla\u00e7 + concepte', '', function () { addPropAndConcept(li); }));
    } else if (kind === 'prop') {
      bar.appendChild(mkBtn('+ concepte', 'Afegir un concepte sota aquesta proposici\u00f3', '', function () {
        var r = C.addChild(md(), li, 'Nou concepte');
        closePopup(); state.lastLine = null;
        setMd(r.md, { openLine: r.newLineIdx });
      }));
      bar.appendChild(mkBtn('+ proposició', 'Proposici\u00f3 germana', '', function () {
        var r = C.addSibling(md(), li, 'enlla\u00e7');
        closePopup(); state.lastLine = null;
        setMd(r.md, { openLine: r.newLineIdx });
      }));
    } else if (kind === 'concept') {
      bar.appendChild(mkBtn('+ germà', 'Concepte germ\u00e0', '', function () {
        var r = C.addSibling(md(), li, 'Nou concepte');
        closePopup(); state.lastLine = null;
        setMd(r.md, { openLine: r.newLineIdx });
      }));
      // La cadena Novak continua en profunditat: concepte -> enlla\u00e7 -> concepte
      bar.appendChild(mkBtn('+ proposició', 'Aprofundir: paraula d\u2019enlla\u00e7 + concepte sota aquest', '', function () { addPropAndConcept(li); }));
    }
    if (kind !== 'root') {
      bar.appendChild(mkBtn('\u00d7', 'Eliminar', 'del', function () {
        var nd = C.descendantCount(md(), li);
        if (nd > 0 && !confirm('Aquest node t\u00e9 ' + nd + ' descendent(s). Eliminar tota la branca?')) return;
        var r = C.deleteSubtree(md(), li);
        closePopup(); state.lastLine = null;
        setMd(r.md);
      }));
    }
    // Connectar amb un altre concepte (enllaç creuat Novak).
    // Usem data-lbl (fiable) en lloc de re-derivar per índex de línia.
    var nodeLabel = state.lastLabel || '';
    bar.appendChild(mkBtn('\u219d connectar', 'Enlla\u00e7 creuat cap a un altre concepte', 'cross', function () {
      startConnect(nodeLabel);
      closePopup(); state.lastLine = null;
    }));
    pop.appendChild(bar);
  }


  // ── Mode connexió (enllaços creuats) ──
  function startConnect(fromLabel) {
    var banner = document.createElement('div');
    banner.id = 'connect-banner';
    banner.style.cssText = 'position:fixed;top:10px;left:50%;transform:translateX(-50%);z-index:10000;' +
      'background:#ea580c;color:#fff;padding:8px 16px;border-radius:99px;font-size:13px;' +
      'box-shadow:0 6px 24px rgba(234,88,12,.35);font-family:system-ui,sans-serif;cursor:default';
    banner.textContent = 'Connectant des de «' + fromLabel + '» — clica el concepte de destí (Esc o clic aquí per cancel\u00b7lar)';
    banner.style.cursor = 'pointer';
    banner.addEventListener('click', cancelConnect);
    document.body.appendChild(banner);
    state.connecting = fromLabel;
    state.cont.querySelectorAll('g[data-nid]').forEach(function (g) { g.style.outline = '2px dashed #fdba74'; g.style.outlineOffset = '2px'; });
    document.addEventListener('keydown', escConnect, true);
  }
  function escConnect(e) { if (e.key === 'Escape') cancelConnect(); }
  function cancelConnect() {
    state.connecting = null;
    var b = document.getElementById('connect-banner'); if (b) b.remove();
    state.cont.querySelectorAll('g[data-nid]').forEach(function (g) { g.style.outline = ''; });
    document.removeEventListener('keydown', escConnect, true);
  }
  // Captura el clic de destí en mode connexió (fase de captura, abans del popup d'edició)
  document.addEventListener('click', function (e) {
    if (!state.connecting) return;
    var t = e.target;
    while (t && t.nodeType === 1 && !(t.hasAttribute && t.hasAttribute('data-nid'))) t = t.parentElement;
    if (!t || t.nodeType !== 1 || !t.hasAttribute('data-nid')) return;
    e.stopPropagation(); e.preventDefault();
    var toLbl = t.getAttribute('data-lbl') || '';
    var from = state.connecting;
    cancelConnect();
    if (!toLbl) { return; }
    if (toLbl === from) { alert('No pots connectar un concepte amb ell mateix.'); return; }
    var link = window.prompt('Com es relacionen «' + from + '» \u2192 «' + toLbl + '»?\nEscriu la paraula d\u2019enlla\u00e7 (p. ex. «\u00e9s imprescindible per a», «provoca»):', '');
    if (link && link.trim()) {
      setMd(C.addCross(md(), from, toLbl, link.trim()));
    }
  }, true);

  // ── Clic sobre etiqueta d'enllaç creuat -> editar paraula o eliminar ──
  document.addEventListener('click', function (e) {
    if (state.connecting) return;   // en mode connexió, no interferim
    var t = e.target;
    while (t && t.nodeType === 1 && !(t.hasAttribute && t.hasAttribute('data-cross-idx'))) t = t.parentElement;
    if (!t || t.nodeType !== 1 || !t.hasAttribute('data-cross-idx')) return;
    e.stopPropagation();
    var idx = parseInt(t.getAttribute('data-cross-idx'), 10);
    var cross = C.splitCross(md()).cross[idx];
    if (!cross) return;
    showCrossPopup(t, cross, idx);
  }, true);

  function showCrossPopup(anchorEl, cross, idx) {
    var old = document.getElementById('atne-cross-popup'); if (old) old.remove();
    var bbox = anchorEl.getBoundingClientRect();
    var pop = document.createElement('div');
    pop.id = 'atne-cross-popup';
    pop.style.cssText =
      'position:fixed;z-index:9999;background:#fff;border:2px solid #ea580c;border-radius:10px;' +
      'padding:8px 10px;box-shadow:0 8px 32px rgba(234,88,12,.2);display:flex;gap:7px;align-items:center;' +
      'font-family:system-ui,sans-serif;font-size:12.5px';
    var ww = window.innerWidth, wh = window.innerHeight;
    var left = Math.max(4, Math.min(bbox.left + bbox.width / 2 - 150, ww - 304));
    var top = bbox.top - 52; if (top < 8) top = bbox.bottom + 6;
    pop.style.left = left + 'px'; pop.style.top = top + 'px';

    var lblTxt = document.createElement('span');
    lblTxt.textContent = cross.from + ' \u2192 ' + cross.to;
    lblTxt.style.cssText = 'color:#94a3b8;font-size:11px;max-width:120px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap';

    var inp = document.createElement('input');
    inp.type = 'text'; inp.value = cross.link;
    inp.style.cssText = 'border:1.5px solid #fed7aa;border-radius:6px;padding:5px 8px;font-size:12.5px;width:140px;outline:none;color:#1e293b';
    inp.addEventListener('keydown', function (ev) {
      if (ev.key === 'Enter') { save(); }
      if (ev.key === 'Escape') { pop.remove(); }
    });

    function save() {
      var v = inp.value.trim();
      pop.remove();
      if (v && v !== cross.link) setMd(C.updateCrossLink(md(), idx, v));
    }
    var btnSave = document.createElement('button');
    btnSave.textContent = 'Desa'; btnSave.type = 'button';
    btnSave.style.cssText = 'border:none;background:#ea580c;color:#fff;border-radius:6px;padding:5px 10px;font-size:12px;cursor:pointer';
    btnSave.onclick = save;

    var btnDel = document.createElement('button');
    btnDel.textContent = '\u00d7'; btnDel.type = 'button'; btnDel.title = 'Eliminar la connexió';
    btnDel.style.cssText = 'border:1px solid #fecaca;background:#fef2f2;color:#dc2626;border-radius:6px;padding:5px 9px;font-size:13px;cursor:pointer;font-weight:700';
    btnDel.onclick = function () { pop.remove(); setMd(C.removeCross(md(), idx)); };

    pop.appendChild(lblTxt); pop.appendChild(inp); pop.appendChild(btnSave); pop.appendChild(btnDel);
    document.body.appendChild(pop);
    inp.focus(); inp.select();

    setTimeout(function () {
      function close(ev) { if (!pop.contains(ev.target)) { pop.remove(); document.removeEventListener('mousedown', close, true); } }
      document.addEventListener('mousedown', close, true);
    }, 60);
  }

  // ── Editor de font millorat ──
  var ta, previewTimer = null;
  function syncTextarea() { if (ta && ta.value !== md()) ta.value = md(); }
  function applyTa(newText, selStart, selEnd) {
    state.undo.push(md());
    state.redo = [];
    state.cont.dataset.md = newText;
    ta.value = newText;
    if (selStart != null) ta.setSelectionRange(selStart, selEnd != null ? selEnd : selStart);
    ta.focus();
    rerender(); updateBadge(); refreshBtns();
  }
  function schedulePreview() {
    clearTimeout(previewTimer);
    previewTimer = setTimeout(function () {
      if (ta.value.trim() && ta.value !== md()) {
        state.undo.push(md()); state.redo = [];
        state.cont.dataset.md = ta.value;
        rerender(); updateBadge(); refreshBtns();
      }
    }, 350);
  }
  function doWrap(mk) {
    var r = C.wrapSelection(ta.value, ta.selectionStart, ta.selectionEnd, mk);
    applyTa(r.text, r.selStart, r.selEnd);
  }
  function initEditor() {
    ta = document.getElementById('src');
    ta.value = md();
    ta.addEventListener('input', schedulePreview);
    ta.addEventListener('keydown', function (e) {
      if (e.key === 'Tab') {
        e.preventDefault();
        applyTa(C.shiftLines(ta.value, ta.selectionStart, ta.selectionEnd, e.shiftKey ? -1 : 1),
                Math.max(0, ta.selectionStart + (e.shiftKey ? -2 : 2)),
                Math.max(0, ta.selectionEnd + (e.shiftKey ? -2 : 2)));
      }
      if ((e.ctrlKey || e.metaKey) && !e.shiftKey && e.key.toLowerCase() === 'b') { e.preventDefault(); doWrap('**'); }
      if ((e.ctrlKey || e.metaKey) && !e.shiftKey && e.key.toLowerCase() === 'i') { e.preventDefault(); doWrap('*'); }
    });
    document.getElementById('tb-in').onclick  = function () { applyTa(C.shiftLines(ta.value, ta.selectionStart, ta.selectionEnd, 1), ta.selectionStart + 2, ta.selectionEnd + 2); };
    document.getElementById('tb-out').onclick = function () { applyTa(C.shiftLines(ta.value, ta.selectionStart, ta.selectionEnd, -1), Math.max(0, ta.selectionStart - 2), Math.max(0, ta.selectionEnd - 2)); };
    document.getElementById('tb-b').onclick   = function () { doWrap('**'); };
    document.getElementById('tb-i').onclick   = function () { doWrap('*'); };
    document.getElementById('tb-br').onclick  = function () {
      var pos = ta.value.lastIndexOf('\n', ta.selectionStart - 1);
      var lineStart = pos + 1;
      var indent = (ta.value.slice(lineStart).match(/^\s*/) || [''])[0];
      var lineEnd = ta.value.indexOf('\n', ta.selectionStart);
      if (lineEnd === -1) lineEnd = ta.value.length;
      var ins = '\n' + indent + '- ';
      applyTa(ta.value.slice(0, lineEnd) + ins + ta.value.slice(lineEnd), lineEnd + ins.length);
    };
  }

  // ── Arrencada ──
  window.addEventListener('DOMContentLoaded', function () {
    state.cont = document.getElementById('diagram');
    state.cont.dataset.md = document.getElementById('seed').textContent.trim();
    rerender(); updateBadge(); initEditor(); refreshBtns();
    document.getElementById('btn-undo').onclick = undo;
    document.getElementById('btn-redo').onclick = redo;
    document.addEventListener('keydown', function (e) {
      var k = e.key.toLowerCase();
      if ((e.ctrlKey || e.metaKey) && k === 'z' && !e.shiftKey) { e.preventDefault(); undo(); }
      else if ((e.ctrlKey || e.metaKey) && (k === 'y' || (k === 'z' && e.shiftKey))) { e.preventDefault(); redo(); }
    });
  });
})();
