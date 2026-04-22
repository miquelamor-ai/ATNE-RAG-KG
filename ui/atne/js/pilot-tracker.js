/*
 * ATNE — Pilot UX events tracker (Sprint 1C, 2026-04-22)
 *
 * Exposa window.ATNE_TRACK amb dues APIs:
 *
 *   ATNE_TRACK.event(event_type, data?, extra?)
 *     → POST a /api/pilot/event (fire-and-forget, no bloqueja UI)
 *
 *   ATNE_TRACK.requireFeedback({ reason, onDone })
 *     → mostra el modal bloquejant de feedback al Pas 3
 *       reason: 'copy' | 'export' | 'leave'
 *       onDone(decision): callback amb 'submitted' | 'skipped'
 *
 * Cal incloure DESPRÉS d'auth.js (perquè ATNE_AUTH.email estigui llest).
 *
 * Convenció event_type:
 *   - adapt_started, adapt_done, adapt_error
 *   - refine_started, refined
 *   - complement_generated, complement_deleted, complement_edited
 *   - copied, exported, manual_edit, saved
 *   - biblioteca_opened, draft_loaded
 *   - pas_change, model_switch, preset_applied
 *   - rubric_submitted, feedback_skipped, feedback_submitted, consent_shown
 *
 * Vegeu _PILOT_EVENT_TYPES a server.py per la whitelist autoritzada.
 */
(function () {
  'use strict';

  var ENDPOINT = '/api/pilot/event';
  var FEEDBACK_ENDPOINT_BASE = '/api/history';

  function _docent() {
    try {
      if (window.ATNE_AUTH && window.ATNE_AUTH.email) return window.ATNE_AUTH.email;
      return localStorage.getItem('atne_user_email') || '';
    } catch (e) { return ''; }
  }

  function _currentSessionId() {
    // Si pas3.html exposa una variable global d'adapt_id, l'aprofitem.
    try {
      if (window.__atne_current_adapt_id) return window.__atne_current_adapt_id;
      // Per defecte, generem un UUID lleuger per session de pestanya.
      if (!window.__atne_session_id) {
        window.__atne_session_id =
          'sess-' + Date.now() + '-' + Math.random().toString(36).slice(2, 8);
      }
      return window.__atne_session_id;
    } catch (e) { return null; }
  }

  function _historyId() {
    try {
      // pas3.html guarda historyId quan ha desat l'adaptació al backend.
      if (window.__atne_current_history_id) return window.__atne_current_history_id;
      // O bé via state global de app.js (workspace antic).
      if (window.state && window.state.historyId) return window.state.historyId;
      return null;
    } catch (e) { return null; }
  }

  function _step() {
    try {
      // Detecta a quina pàgina som per inferir el pas.
      var path = location.pathname || '';
      if (path.indexOf('pas1') !== -1) return 'pas1';
      if (path.indexOf('pas2') !== -1) return 'pas2';
      if (path.indexOf('pas3') !== -1) return 'pas3';
      if (path.indexOf('consent') !== -1) return 'consent';
      if (window.state && window.state.step) return 'pas' + window.state.step;
      return null;
    } catch (e) { return null; }
  }

  function event(eventType, data, extra) {
    if (!eventType) return;
    var payload = {
      event_type: eventType,
      session_id: (extra && extra.session_id) || _currentSessionId(),
      history_id: (extra && extra.history_id) || _historyId(),
      step: (extra && extra.step) || _step(),
      docent_id: _docent() || null,
      data: data || {},
    };
    try {
      // keepalive perquè events com 'exported' no es perdin si la pàgina marxa
      fetch(ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
        keepalive: true,
      }).catch(function () { /* no bloquejant */ });
    } catch (e) { /* no bloquejant */ }
  }

  // ── Modal bloquejant de feedback ──────────────────────────────────────

  var MODAL_HTML = [
    '<div id="atne-fb-modal" style="position:fixed;inset:0;background:rgba(20,20,30,0.55);',
    'z-index:99999;display:flex;align-items:center;justify-content:center;',
    'font-family:Inter,system-ui,sans-serif;padding:16px">',
    '  <div style="background:#fff;max-width:480px;width:100%;border-radius:14px;',
    '       padding:24px 26px;box-shadow:0 12px 40px rgba(0,0,0,0.25)">',
    '    <h2 style="margin:0 0 6px;font-family:Fraunces,Georgia,serif;font-size:22px;color:#1f1f2c">',
    '      Una valoració ràpida ',
    '      <span style="font-family:Inter,sans-serif;font-size:13px;color:#6b6b7a;font-weight:400">(opcional)</span>',
    '    </h2>',
    '    <p style="margin:0 0 18px;color:#454555;line-height:1.45;font-size:14px">',
    '      Si vols, dona\'ns la teva opinió d\'aquesta adaptació en 5 segons.',
    '      Ens ajuda a millorar ATNE durant el pilot. Si tens pressa, ometre-ho és perfectament correcte.',
    '    </p>',
    '    <div style="display:flex;gap:8px;justify-content:center;margin:14px 0 18px">',
    '      <button class="atne-fb-star" data-star="1" type="button"',
    '              style="background:#fff;border:1.5px solid #d4d4dc;border-radius:8px;',
    '                     padding:10px 14px;font-size:18px;cursor:pointer">★ 1</button>',
    '      <button class="atne-fb-star" data-star="2" type="button"',
    '              style="background:#fff;border:1.5px solid #d4d4dc;border-radius:8px;',
    '                     padding:10px 14px;font-size:18px;cursor:pointer">★ 2</button>',
    '      <button class="atne-fb-star" data-star="3" type="button"',
    '              style="background:#fff;border:1.5px solid #d4d4dc;border-radius:8px;',
    '                     padding:10px 14px;font-size:18px;cursor:pointer">★ 3</button>',
    '    </div>',
    '    <div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:18px;justify-content:center">',
    '      <label style="font-size:13px;color:#3a3a48;display:flex;align-items:center;gap:6px;cursor:pointer">',
    '        <input type="checkbox" data-fb="usar_classe"> L\'usaré tal qual',
    '      </label>',
    '      <label style="font-size:13px;color:#3a3a48;display:flex;align-items:center;gap:6px;cursor:pointer">',
    '        <input type="checkbox" data-fb="retocar"> L\'hauré de retocar',
    '      </label>',
    '      <label style="font-size:13px;color:#3a3a48;display:flex;align-items:center;gap:6px;cursor:pointer">',
    '        <input type="checkbox" data-fb="no_usar"> No la usaré',
    '      </label>',
    '    </div>',
    '    <textarea id="atne-fb-comment" placeholder="Comentari opcional…"',
    '              style="width:100%;min-height:60px;border:1px solid #d4d4dc;border-radius:8px;',
    '                     padding:8px 10px;font-family:inherit;font-size:13px;',
    '                     resize:vertical;box-sizing:border-box;margin-bottom:16px"></textarea>',
    '    <div style="display:flex;gap:10px;justify-content:space-between;align-items:center">',
    '      <button id="atne-fb-skip" type="button"',
    '              style="background:#fff;color:#3a3a48;border:1.5px solid #d4d4dc;',
    '                     border-radius:8px;padding:10px 22px;font-weight:500;font-size:14px;',
    '                     cursor:pointer;font-family:inherit">Omet i continua</button>',
    '      <button id="atne-fb-send" type="button"',
    '              style="background:#4c3fc4;color:#fff;border:none;border-radius:8px;',
    '                     padding:10px 22px;font-weight:600;font-size:14px;',
    '                     cursor:pointer;font-family:inherit">Envia i continua</button>',
    '    </div>',
    '  </div>',
    '</div>'
  ].join('');

  var _modalShown = false;
  var _selectedStar = null;

  function _ensureModalCss() {
    if (document.getElementById('atne-fb-modal-css')) return;
    var st = document.createElement('style');
    st.id = 'atne-fb-modal-css';
    st.textContent = [
      '.atne-fb-star.sel{background:#fff5d9 !important;border-color:#f5b300 !important;color:#7a4f00}',
      '.atne-fb-star:hover{border-color:#bbb !important}'
    ].join('\n');
    document.head.appendChild(st);
  }

  function requireFeedback(opts) {
    opts = opts || {};
    var historyId = opts.historyId || _historyId();
    var reason = opts.reason || 'leave';
    var onDone = typeof opts.onDone === 'function' ? opts.onDone : function () {};

    // Si no tenim historyId, no podem associar el feedback. Deixem passar.
    if (!historyId) { onDone('skipped_no_history'); return; }

    // Mostra modal una sola vegada per sessió
    if (_modalShown) { onDone('already_shown'); return; }
    _modalShown = true;

    _ensureModalCss();
    var div = document.createElement('div');
    div.innerHTML = MODAL_HTML;
    document.body.appendChild(div);

    function close(decision) {
      try { document.body.removeChild(div); } catch (e) { /* */ }
      onDone(decision);
    }

    var modal = document.getElementById('atne-fb-modal');
    var stars = modal.querySelectorAll('.atne-fb-star');
    stars.forEach(function (b) {
      b.addEventListener('click', function () {
        _selectedStar = parseInt(b.dataset.star, 10);
        stars.forEach(function (x) { x.classList.toggle('sel', parseInt(x.dataset.star, 10) === _selectedStar); });
      });
    });

    document.getElementById('atne-fb-skip').addEventListener('click', function () {
      event('feedback_skipped', { reason: reason });
      close('skipped');
    });

    document.getElementById('atne-fb-send').addEventListener('click', function () {
      var checks = modal.querySelectorAll('input[type=checkbox][data-fb]');
      var review = {};
      checks.forEach(function (c) { review[c.dataset.fb] = !!c.checked; });
      var comment = (document.getElementById('atne-fb-comment').value || '').trim();
      var body = { review_items: review };
      if (_selectedStar) body.rating = _selectedStar;
      if (comment) body.comment = comment;
      try {
        fetch(FEEDBACK_ENDPOINT_BASE + '/' + historyId, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(body),
          keepalive: true,
        }).catch(function () { /* */ });
      } catch (e) { /* */ }
      event('feedback_submitted', {
        rating: _selectedStar,
        review: review,
        has_comment: !!comment,
        reason: reason,
      });
      close('submitted');
    });
  }

  // Permet rearmar el modal per a una nova adaptació (la pas3.html ho farà
  // quan es genera una versió nova).
  function resetFeedbackGate() { _modalShown = false; _selectedStar = null; }

  window.ATNE_TRACK = {
    event: event,
    requireFeedback: requireFeedback,
    resetFeedbackGate: resetFeedbackGate,
  };
})();
