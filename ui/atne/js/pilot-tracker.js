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
  var _pageLoadTs = Date.now();

  function _deviceInfo() {
    try {
      return {
        screen_w: screen.width,
        screen_h: screen.height,
        is_mobile: screen.width < 768 || /Mobi|Android/i.test(navigator.userAgent),
        lang: navigator.language || '',
      };
    } catch (e) { return {}; }
  }

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
    var _data = Object.assign({ time_on_page_ms: Date.now() - _pageLoadTs }, data || {});
    var payload = {
      event_type: eventType,
      session_id: (extra && extra.session_id) || _currentSessionId(),
      history_id: (extra && extra.history_id) || _historyId(),
      step: (extra && extra.step) || _step(),
      docent_id: _docent() || null,
      data: _data,
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
      // PATCH a historial només si tenim history_id (Taller). Flash usa només events.
      if (historyId) {
        try {
          fetch(FEEDBACK_ENDPOINT_BASE + '/' + historyId, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body),
            keepalive: true,
          }).catch(function () { /* */ });
        } catch (e) { /* */ }
      }
      event('feedback_submitted', {
        rating: _selectedStar,
        review: review,
        has_comment: !!comment,
        reason: reason,
        mode: historyId ? 'taller' : 'flash',
      });
      close('submitted');
    });
  }

  // Permet rearmar el modal per a una nova adaptació (la pas3.html ho farà
  // quan es genera una versió nova).
  function resetFeedbackGate() {
    _modalShown = false;
    _selectedStar = null;
    _resetInline();  // Sprint 1D: també rearma la pill inline
  }

  // ── Inline feedback widget (Sprint 1D, 2026-04-23) ─────────────────────
  //
  // Pill persistent al Pas 3. Substitueix el modal bloquejant a l'export.
  // Filosofia: el docent valora QUAN vol (no quan el sistema l'interromp),
  // i només DESPRÉS d'haver vist com queda l'adaptació.
  // Sempre visible, mai bloqueja, no apareix repetidament un cop valorat.

  var _INLINE_HTML = [
    '<div id="atne-fb-pill" class="atne-fb-pill" role="region" aria-label="Valoració de l\'adaptació">',
    '  <button type="button" class="atne-fb-pill-collapsed" id="atne-fb-pill-btn" aria-expanded="false">',
    '    <span class="atne-fb-pill-icon" aria-hidden="true">',
    '      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">',
    '        <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>',
    '      </svg>',
    '    </span>',
    '    <span class="atne-fb-pill-label">Valora aquesta adaptació</span>',
    '  </button>',
    '  <div class="atne-fb-pill-panel" hidden>',
    '    <div class="atne-fb-pill-head">',
    '      <strong>Com t\'ha quedat?</strong>',
    '      <button type="button" class="atne-fb-pill-close" aria-label="Tancar">×</button>',
    '    </div>',
    '    <div class="atne-fb-pill-stars">',
    '      <button type="button" class="atne-fb-istar" data-star="1" aria-label="1 estrella">★ 1</button>',
    '      <button type="button" class="atne-fb-istar" data-star="2" aria-label="2 estrelles">★ 2</button>',
    '      <button type="button" class="atne-fb-istar" data-star="3" aria-label="3 estrelles">★ 3</button>',
    '    </div>',
    '    <div class="atne-fb-pill-checks">',
    '      <label><input type="checkbox" data-fb="usar_classe"> L\'usaré tal qual</label>',
    '      <label><input type="checkbox" data-fb="retocar"> L\'hauré de retocar</label>',
    '      <label><input type="checkbox" data-fb="no_usar"> No la usaré</label>',
    '    </div>',
    '    <textarea class="atne-fb-pill-comment" placeholder="Comentari opcional…"></textarea>',
    '    <div class="atne-fb-pill-actions">',
    '      <button type="button" class="atne-fb-pill-send">Envia</button>',
    '    </div>',
    '    <div class="atne-fb-pill-thanks" hidden>✓ Gràcies pel teu feedback</div>',
    '  </div>',
    '</div>',
  ].join('');

  var _INLINE_CSS = [
    '.atne-fb-pill{position:fixed;right:16px;bottom:16px;z-index:9000;font-family:Inter,system-ui,sans-serif}',
    '.atne-fb-pill-collapsed{display:flex;align-items:center;gap:8px;background:#4c3fc4;color:#fff;border:none;border-radius:999px;padding:10px 16px;font-size:13px;font-weight:500;cursor:pointer;box-shadow:0 6px 18px rgba(76,63,196,0.32);font-family:inherit;transition:transform .15s,box-shadow .2s}',
    '.atne-fb-pill-collapsed:hover{transform:translateY(-1px);box-shadow:0 8px 22px rgba(76,63,196,0.38)}',
    '.atne-fb-pill-collapsed.nudge{animation:atne-fb-nudge 1.2s ease-in-out 2}',
    '@keyframes atne-fb-nudge{0%,100%{transform:translateY(0)}25%{transform:translateY(-4px) scale(1.03)}50%{transform:translateY(0)}75%{transform:translateY(-2px)}}',
    '.atne-fb-pill.expanded .atne-fb-pill-collapsed{display:none}',
    '.atne-fb-pill-panel{background:#fff;border-radius:14px;padding:16px 18px;box-shadow:0 12px 36px rgba(0,0,0,0.18);border:1px solid #e6e6ee;max-width:320px;width:calc(100vw - 32px)}',
    '.atne-fb-pill-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;font-family:Fraunces,Georgia,serif}',
    '.atne-fb-pill-head strong{font-size:15px;color:#1f1f2c}',
    '.atne-fb-pill-close{background:none;border:none;font-size:22px;line-height:1;color:#6b6b7a;cursor:pointer;padding:0 4px}',
    '.atne-fb-pill-stars{display:flex;gap:6px;margin-bottom:10px}',
    '.atne-fb-istar{flex:1;background:#fff;border:1.5px solid #d4d4dc;border-radius:8px;padding:7px 8px;font-size:13px;cursor:pointer;font-family:inherit;color:#3a3a48}',
    '.atne-fb-istar.sel{background:#fff5d9;border-color:#f5b300;color:#7a4f00}',
    '.atne-fb-istar:hover{border-color:#aaa}',
    '.atne-fb-pill-checks{display:flex;flex-direction:column;gap:4px;margin-bottom:10px;font-size:12px;color:#3a3a48}',
    '.atne-fb-pill-checks label{display:flex;align-items:center;gap:6px;cursor:pointer}',
    '.atne-fb-pill-comment{width:100%;min-height:50px;border:1px solid #d4d4dc;border-radius:6px;padding:6px 8px;font-family:inherit;font-size:12px;resize:vertical;box-sizing:border-box;margin-bottom:10px}',
    '.atne-fb-pill-actions{display:flex;justify-content:flex-end;gap:6px}',
    '.atne-fb-pill-send{background:#4c3fc4;color:#fff;border:none;border-radius:6px;padding:7px 16px;font-size:13px;font-weight:600;cursor:pointer;font-family:inherit}',
    '.atne-fb-pill-send:disabled{opacity:0.6;cursor:default}',
    '.atne-fb-pill-thanks{margin-top:8px;color:#1f7a3e;font-size:12px;text-align:center;font-weight:500}',
    '.atne-fb-pill.submitted .atne-fb-pill-collapsed{background:#1f7a3e;box-shadow:0 4px 12px rgba(31,122,62,0.32)}',
    '.atne-fb-pill.submitted .atne-fb-pill-label::before{content:"✓ "}',
    '@media (max-width:600px){.atne-fb-pill{right:8px;bottom:8px}}',
  ].join('\n');

  var _inlineMounted = false;
  var _inlineSubmitted = false;
  var _inlineSelectedStar = null;

  function _ensureInlineCss() {
    if (document.getElementById('atne-fb-inline-css')) return;
    var st = document.createElement('style');
    st.id = 'atne-fb-inline-css';
    st.textContent = _INLINE_CSS;
    document.head.appendChild(st);
  }

  function _resetInline() {
    _inlineSubmitted = false;
    _inlineSelectedStar = null;
    var pill = document.getElementById('atne-fb-pill');
    if (!pill) return;
    pill.classList.remove('submitted', 'expanded');
    pill.style.display = '';
    var panel = pill.querySelector('.atne-fb-pill-panel');
    if (panel) panel.hidden = true;
    var thanks = pill.querySelector('.atne-fb-pill-thanks');
    if (thanks) thanks.hidden = true;
    pill.querySelectorAll('.atne-fb-istar').forEach(function (s) { s.classList.remove('sel'); });
    pill.querySelectorAll('input[type=checkbox][data-fb]').forEach(function (c) { c.checked = false; });
    var comment = pill.querySelector('.atne-fb-pill-comment');
    if (comment) comment.value = '';
    var sendBtn = pill.querySelector('.atne-fb-pill-send');
    if (sendBtn) sendBtn.disabled = false;
    var btn = pill.querySelector('.atne-fb-pill-collapsed');
    if (btn) {
      btn.style.display = '';
      btn.setAttribute('aria-expanded', 'false');
      var lab = btn.querySelector('.atne-fb-pill-label');
      if (lab) lab.textContent = 'Valora aquesta adaptació';
    }
  }

  function showInlineFeedback() {
    if (_inlineMounted) {
      _resetInline();
      return;
    }
    _ensureInlineCss();
    var holder = document.createElement('div');
    holder.innerHTML = _INLINE_HTML;
    document.body.appendChild(holder.firstElementChild);
    _inlineMounted = true;

    var pill = document.getElementById('atne-fb-pill');
    var btn = pill.querySelector('.atne-fb-pill-collapsed');
    var panel = pill.querySelector('.atne-fb-pill-panel');
    var closeBtn = pill.querySelector('.atne-fb-pill-close');
    var stars = pill.querySelectorAll('.atne-fb-istar');
    var sendBtn = pill.querySelector('.atne-fb-pill-send');
    var thanks = pill.querySelector('.atne-fb-pill-thanks');

    function expand() {
      pill.classList.add('expanded');
      panel.hidden = false;
      btn.setAttribute('aria-expanded', 'true');
    }
    function collapse() {
      pill.classList.remove('expanded');
      panel.hidden = true;
      btn.setAttribute('aria-expanded', 'false');
    }

    btn.addEventListener('click', expand);
    closeBtn.addEventListener('click', collapse);

    stars.forEach(function (s) {
      s.addEventListener('click', function () {
        _inlineSelectedStar = parseInt(s.dataset.star, 10);
        stars.forEach(function (x) {
          x.classList.toggle('sel', parseInt(x.dataset.star, 10) === _inlineSelectedStar);
        });
      });
    });

    sendBtn.addEventListener('click', function () {
      if (_inlineSubmitted) return;
      var historyId = _historyId();
      var review = {};
      pill.querySelectorAll('input[type=checkbox][data-fb]').forEach(function (c) {
        review[c.dataset.fb] = !!c.checked;
      });
      var comment = (pill.querySelector('.atne-fb-pill-comment').value || '').trim();
      var body = { review_items: review };
      if (_inlineSelectedStar) body.rating = _inlineSelectedStar;
      if (comment) body.comment = comment;

      if (historyId) {
        try {
          fetch('/api/history/' + historyId, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body),
            keepalive: true,
          }).catch(function () { /* */ });
        } catch (_) { /* */ }
      }
      event('feedback_submitted', {
        rating: _inlineSelectedStar,
        review: review,
        has_comment: !!comment,
        source: 'inline_pill',
      });

      _inlineSubmitted = true;
      sendBtn.disabled = true;
      thanks.hidden = false;
      pill.classList.add('submitted');
      var lab = btn.querySelector('.atne-fb-pill-label');
      if (lab) lab.textContent = 'Valoració enviada';
      // Auto-collapse perquè el docent pugui tornar a la feina
      setTimeout(function () { if (_inlineSubmitted) collapse(); }, 2200);
    });
  }

  // One-shot: animació subtil per cridar atenció a la pill després de la
  // primera "consumició" de l'adaptació (export, copy, print). No reapareix
  // si el docent ja ha valorat.
  function nudgeInlineFeedback() {
    if (_inlineSubmitted) return;
    if (!_inlineMounted) showInlineFeedback();
    var pill = document.getElementById('atne-fb-pill');
    if (!pill) return;
    var btn = pill.querySelector('.atne-fb-pill-collapsed');
    if (!btn) return;
    btn.classList.remove('nudge');
    void btn.offsetWidth; // forçar reflow per re-iniciar animació
    btn.classList.add('nudge');
  }

  function hideInlineFeedback() {
    var pill = document.getElementById('atne-fb-pill');
    if (pill) pill.style.display = 'none';
  }

  // pageView: registra visualització d'una pàgina informativa (saber-ne, etc.)
  // i envia page_leave amb durada quan l'usuari surt.
  function pageView(pageName) {
    event('page_view', Object.assign({ page: pageName, referrer: document.referrer || '' }, _deviceInfo()));
    window.addEventListener('beforeunload', function () {
      event('page_leave', { page: pageName, duration_ms: Date.now() - _pageLoadTs });
    });
  }

  // trackScrollDepth: listener de scroll al contenidor donat.
  // Envia scroll_depth quan l'usuari supera 25%, 50%, 75%, 100%.
  function trackScrollDepth(containerId, context) {
    var el = document.getElementById(containerId);
    if (!el) return;
    var reported = {};
    var milestones = [25, 50, 75, 100];
    function onScroll() {
      var scrolled = el.scrollTop + el.clientHeight;
      var total = el.scrollHeight;
      if (total <= 0) return;
      var pct = Math.round((scrolled / total) * 100);
      milestones.forEach(function (m) {
        if (pct >= m && !reported[m]) {
          reported[m] = true;
          event('scroll_depth', Object.assign({ depth_pct: m }, context || {}));
        }
      });
    }
    el.addEventListener('scroll', onScroll, { passive: true });
  }

  // trackFormAbandoned: detecta si l'usuari surt sense haver adaptat.
  // Cal cridar-lo a l'inici + actualitzar _hasAdapted = true quan es genera.
  function trackFormAbandoned(getHasAdapted, context) {
    window.addEventListener('beforeunload', function () {
      if (!getHasAdapted()) {
        event('form_abandoned', context || {});
      }
    });
  }

  // ── Captura global d'errors JS ────────────────────────────────────────────
  window.addEventListener('error', function (e) {
    try {
      event('client_error', {
        msg: e.message || '',
        file: (e.filename || '').replace(location.origin, ''),
        line: e.lineno || 0,
        col: e.colno || 0,
        type: 'js',
        page: location.pathname,
      });
    } catch (_) { /* no bloquejant */ }
  });

  window.addEventListener('unhandledrejection', function (e) {
    try {
      var msg = '';
      try { msg = String(e.reason && e.reason.message ? e.reason.message : e.reason); } catch (_) { msg = 'unknown'; }
      event('client_error', {
        msg: msg,
        type: 'promise',
        page: location.pathname,
      });
    } catch (_) { /* no bloquejant */ }
  });

  document.addEventListener('securitypolicyviolation', function (e) {
    try {
      event('client_error', {
        msg: 'CSP block: ' + (e.violatedDirective || '') + ' → ' + (e.blockedURI || ''),
        file: (e.sourceFile || '').replace(location.origin, ''),
        line: e.lineNumber || 0,
        type: 'csp',
        page: location.pathname,
      });
    } catch (_) { /* no bloquejant */ }
  });

  // ── Botó de suggeriment ───────────────────────────────────────────────────
  var SUGGESTION_HTML = [
    '<div id="atne-sug-modal" style="position:fixed;inset:0;background:rgba(20,20,30,0.45);',
    'z-index:99999;display:flex;align-items:center;justify-content:center;',
    'font-family:Inter,system-ui,sans-serif;padding:16px">',
    '  <div style="background:#fff;max-width:420px;width:100%;border-radius:14px;',
    '       padding:24px 26px;box-shadow:0 12px 40px rgba(0,0,0,0.22)">',
    '    <h2 style="margin:0 0 8px;font-family:Fraunces,Georgia,serif;font-size:20px;color:#1f1f2c">',
    '      Tens un suggeriment?',
    '    </h2>',
    '    <p style="margin:0 0 14px;color:#454555;font-size:13px;line-height:1.45">',
    '      Escriu el que vulguis: una idea, un problema, una pregunta.',
    '      Ho llegim tot.',
    '    </p>',
    '    <textarea id="atne-sug-text" placeholder="El teu suggeriment…"',
    '              style="width:100%;min-height:80px;border:1px solid #d4d4dc;border-radius:8px;',
    '                     padding:8px 10px;font-family:inherit;font-size:13px;',
    '                     resize:vertical;box-sizing:border-box;margin-bottom:16px"></textarea>',
    '    <div style="display:flex;gap:10px;justify-content:flex-end">',
    '      <button id="atne-sug-cancel" type="button"',
    '              style="background:#fff;color:#3a3a48;border:1.5px solid #d4d4dc;',
    '                     border-radius:8px;padding:9px 20px;font-size:14px;font-weight:500;',
    '                     cursor:pointer;font-family:inherit">Cancel·la</button>',
    '      <button id="atne-sug-send" type="button"',
    '              style="background:#4c3fc4;color:#fff;border:none;border-radius:8px;',
    '                     padding:9px 20px;font-size:14px;font-weight:600;',
    '                     cursor:pointer;font-family:inherit">Envia</button>',
    '    </div>',
    '  </div>',
    '</div>'
  ].join('');

  function openSuggestionBox(context) {
    if (document.getElementById('atne-sug-modal')) return;
    var div = document.createElement('div');
    div.innerHTML = SUGGESTION_HTML;
    document.body.appendChild(div);
    var ta = document.getElementById('atne-sug-text');
    setTimeout(function () { ta && ta.focus(); }, 80);

    function close() { try { document.body.removeChild(div); } catch (e) { /* */ } }

    document.getElementById('atne-sug-cancel').addEventListener('click', close);
    document.getElementById('atne-sug-send').addEventListener('click', function () {
      var text = (ta.value || '').trim();
      if (!text) { close(); return; }

      // Backup local IMMEDIAT (mai més perdrem un suggeriment per fallada de
      // xarxa o backend). Quedarà a localStorage fins que el backend confirmi.
      var backupKey = 'atne_sug_pending';
      var pending = [];
      try { pending = JSON.parse(localStorage.getItem(backupKey) || '[]'); } catch (e) { pending = []; }
      var localId = 'lcl-' + Date.now() + '-' + Math.random().toString(36).slice(2, 6);
      pending.push({
        id: localId,
        ts: new Date().toISOString(),
        text: text,
        context: context || {},
        docent: _docent() || null,
        page: location.pathname,
        sent: false,
      });
      try { localStorage.setItem(backupKey, JSON.stringify(pending.slice(-50))); } catch (e) { /* */ }

      // Enviament SÍNCRON amb verificació real de resposta. No usem el
      // fire-and-forget `event()` general perquè els suggeriments són
      // dades crítiques (no recuperables si es perden).
      var sendBtn = document.getElementById('atne-sug-send');
      sendBtn.disabled = true;
      sendBtn.textContent = 'Enviant…';

      var payload = {
        event_type: 'suggestion_submitted',
        session_id: _currentSessionId(),
        history_id: _historyId(),
        step: _step(),
        docent_id: _docent() || null,
        data: Object.assign({ text: text, _local_id: localId }, context || {}),
      };

      fetch(ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })
        .then(function (r) { return r.json().catch(function () { return { ok: r.ok }; }); })
        .then(function (resp) {
          if (resp && resp.ok) {
            // Marquem com enviat al backup local (no l'esborrem, queda
            // com a registre per si el dashboard no el mostra).
            try {
              var p = JSON.parse(localStorage.getItem(backupKey) || '[]');
              p.forEach(function (it) { if (it.id === localId) it.sent = true; });
              localStorage.setItem(backupKey, JSON.stringify(p));
            } catch (e) { /* */ }
            close();
            _showToast('Gràcies pel suggeriment!', '#1f1f2c');
          } else {
            _showSuggestionError(div, text, resp && resp.error);
          }
        })
        .catch(function (err) {
          _showSuggestionError(div, text, err && err.message);
        });
    });
  }

  function _showToast(text, bg) {
    var toast = document.createElement('div');
    toast.textContent = text;
    toast.style.cssText = 'position:fixed;bottom:24px;left:50%;transform:translateX(-50%);' +
      'background:' + (bg || '#1f1f2c') + ';color:#fff;padding:10px 22px;border-radius:8px;font-size:14px;' +
      'z-index:99999;font-family:Inter,sans-serif;pointer-events:none;max-width:90%;text-align:center';
    document.body.appendChild(toast);
    setTimeout(function () { try { document.body.removeChild(toast); } catch (e) { /* */ } }, 3500);
  }

  function _showSuggestionError(modalDiv, originalText, errMsg) {
    // No tanquem el modal: el text continua visible perquè el docent pugui
    // copiar-lo. Reactivem el botó i mostrem un missatge inline + toast.
    var sendBtn = document.getElementById('atne-sug-send');
    if (sendBtn) {
      sendBtn.disabled = false;
      sendBtn.textContent = 'Torna a provar';
    }
    var modalInner = modalDiv.querySelector('div > div');
    if (modalInner && !modalInner.querySelector('.atne-sug-err')) {
      var err = document.createElement('div');
      err.className = 'atne-sug-err';
      err.style.cssText = 'background:#fdecea;border:1px solid #f5b1a8;color:#8a1f15;' +
        'padding:8px 10px;border-radius:6px;font-size:12px;line-height:1.4;margin:0 0 12px';
      err.innerHTML = '<strong>No s\'ha pogut enviar.</strong> El text està desat localment ' +
        'i el podeu copiar (Cmd/Ctrl+A → Cmd/Ctrl+C). Avisa l\'equip ATNE si cal.' +
        (errMsg ? '<br><span style="font-family:monospace;font-size:11px">' + String(errMsg).slice(0, 200) + '</span>' : '');
      modalInner.insertBefore(err, modalInner.firstChild);
    }
    _showToast('Error enviant el suggeriment — text desat al navegador', '#8a1f15');
  }

  window.ATNE_TRACK = {
    event: event,
    requireFeedback: requireFeedback,            // legacy (pilot 1C, no s'usa al 1D)
    resetFeedbackGate: resetFeedbackGate,
    pageView: pageView,
    trackScrollDepth: trackScrollDepth,
    trackFormAbandoned: trackFormAbandoned,
    deviceInfo: _deviceInfo,
    openSuggestionBox: openSuggestionBox,
    // Sprint 1D — feedback inline persistent
    showInlineFeedback: showInlineFeedback,
    nudgeInlineFeedback: nudgeInlineFeedback,
    hideInlineFeedback: hideInlineFeedback,
  };
})();
