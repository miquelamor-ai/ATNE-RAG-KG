/*
 * ATNE — Auth client
 *
 * Gestiona la sessió de Supabase (Google OAuth, restringit a @fje.edu):
 *  - Captura l'access_token del fragment d'URL després del login
 *  - El desa a localStorage i l'envia com Authorization: Bearer a cada fetch /api/*
 *  - Si no hi ha token vàlid, redirigeix a Supabase OAuth
 *  - Si un endpoint retorna 401, forceja re-login
 *
 * Carregar com a primer <script> del <head>, sense defer/async.
 */
(function () {
  'use strict';

  var SUPABASE_URL = 'https://qlftykfqjwaxucoeqcjv.supabase.co';
  var LS_TOKEN = 'atne_jwt';
  var LS_EMAIL = 'atne_user_email';

  function parseJwt(token) {
    try {
      var base = token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/');
      while (base.length % 4) base += '=';
      return JSON.parse(decodeURIComponent(escape(atob(base))));
    } catch (e) {
      return null;
    }
  }

  function isValid(token) {
    if (!token) return false;
    var p = parseJwt(token);
    if (!p || !p.exp) return false;
    return p.exp > Math.floor(Date.now() / 1000) + 30;
  }

  function clearSession() {
    try {
      localStorage.removeItem(LS_TOKEN);
      localStorage.removeItem(LS_EMAIL);
    } catch (e) { /* ignore */ }
  }

  function redirectToLogin() {
    clearSession();
    var back = location.origin + location.pathname + location.search;
    // prompt=select_account força que Google mostri sempre el selector de
    // comptes, evitant que auto-triï un Gmail personal obert al navegador
    // (que seria rebutjat per la restricció Internal @fje.edu).
    location.href = SUPABASE_URL
      + '/auth/v1/authorize?provider=google'
      + '&redirect_to=' + encodeURIComponent(back)
      + '&prompt=select_account';
  }

  // 1. Captura el token del fragment d'URL (després del redirect de Supabase)
  if (location.hash && location.hash.indexOf('access_token=') !== -1) {
    var params = new URLSearchParams(location.hash.substring(1));
    var tok = params.get('access_token');
    if (tok) {
      var payload = parseJwt(tok);
      var email = payload && payload.email ? String(payload.email).toLowerCase() : '';
      if (email.indexOf('@fje.edu') !== -1) {
        try {
          localStorage.setItem(LS_TOKEN, tok);
          localStorage.setItem(LS_EMAIL, email);
        } catch (e) { /* ignore */ }
      }
      // Netegem el hash per no deixar el token exposat a la barra
      try {
        history.replaceState(null, '', location.pathname + location.search);
      } catch (e) { /* ignore */ }
    }
  }

  // 2. Llegim el token actual de localStorage
  var currentToken = null;
  try { currentToken = localStorage.getItem(LS_TOKEN); } catch (e) { /* ignore */ }

  // 3. Si no n'hi ha o ha expirat, redirigim a login
  if (!isValid(currentToken)) {
    redirectToLogin();
    // Aturem l'execució de scripts posteriors (ens n'anem de pàgina)
    throw new Error('ATNE: redirigint a login');
  }

  // 4. Exposem l'API d'auth
  var email = null;
  try { email = localStorage.getItem(LS_EMAIL); } catch (e) { /* ignore */ }
  window.ATNE_AUTH = {
    token: currentToken,
    email: email,
    logout: function () { redirectToLogin(); },
  };

  // 5. Pinta l'avatar del docent (#docent-av) amb la inicial de l'alias i,
  // si la pàgina no té menú natiu (#admin-menu), l'injecta + estils i lliga
  // els handlers de toggle i logout. pas1 ja té HTML i CSS propis i la seva
  // pròpia funció _updateDocentBtn — aquest hook només completa pas2 i pas3.
  var MENU_CSS = [
    '.admin-menu{position:absolute;top:calc(100% + 6px);right:0;background:#fff;',
    'border:1px solid var(--paper-line,#e4e0da);border-radius:var(--r-md,8px);',
    'box-shadow:var(--sh-lg,0 8px 24px rgba(0,0,0,.12));padding:6px;min-width:180px;',
    'z-index:200;display:none}',
    '.admin-menu.on{display:block}',
    '.admin-menu a,.admin-menu button{display:flex;align-items:center;gap:8px;',
    'width:100%;padding:8px 10px;font-size:13px;color:var(--ink-800,#2a2a2a);',
    'text-decoration:none;background:none;border:none;border-radius:var(--r-sm,6px);',
    'cursor:pointer;font-family:inherit;text-align:left}',
    '.admin-menu a:hover,.admin-menu button:hover{background:var(--cream-2,#f5f1ea);',
    'color:var(--primary,#4c3fc4)}',
    '.admin-menu .sep{height:1px;background:var(--paper-line,#e4e0da);margin:4px 0}',
    '.admin-badge{font-size:9px;font-weight:700;background:var(--primary,#4c3fc4);',
    'color:#fff;border-radius:3px;padding:1px 4px;margin-left:auto}'
  ].join('');

  function ensureMenuStyles() {
    if (document.getElementById('atne-auth-menu-styles')) return;
    var st = document.createElement('style');
    st.id = 'atne-auth-menu-styles';
    st.textContent = MENU_CSS;
    document.head.appendChild(st);
  }

  function buildMenu(alias) {
    var div = document.createElement('div');
    div.className = 'admin-menu';
    div.id = 'admin-menu';
    div.innerHTML =
      '<div id="admin-menu-top" style="padding:6px 10px 4px;font-size:11px;color:var(--ink-500,#6b6b6b);border-bottom:1px solid var(--paper-line,#e4e0da);margin-bottom:4px">' + alias + '</div>' +
      '<div id="admin-links" style="display:none">' +
        '<a href="/admin">Admin <span class="admin-badge">ADMIN</span></a>' +
        '<a href="/ui/cuina.html">Cuina (dev)</a>' +
        '<div class="sep"></div>' +
      '</div>' +
      '<div class="sep"></div>' +
      '<button id="admin-logout-btn">Canviar d\'usuari</button>';
    return div;
  }

  function attachMenuHandlers(btn, menu, alias) {
    // Assegura que el contenidor del botó és posicionat per ancorar el menú.
    var parent = btn.parentElement;
    if (parent && getComputedStyle(parent).position === 'static') {
      parent.style.position = 'relative';
    }
    btn.onclick = function (e) { e.stopPropagation(); menu.classList.toggle('on'); };
    document.addEventListener('click', function () { menu.classList.remove('on'); });
    var logout = menu.querySelector('#admin-logout-btn');
    if (logout) {
      logout.onclick = function () {
        if (confirm('Estàs identificat/da com a ' + alias + '.\nVols sortir i canviar d\'usuari?')) {
          try {
            localStorage.removeItem('atne.docent_id');
            localStorage.removeItem('atne.docent_alias');
          } catch (e) { /* ignore */ }
          if (window.ATNE_AUTH && typeof window.ATNE_AUTH.logout === 'function') {
            window.ATNE_AUTH.logout();
          } else {
            location.reload();
          }
        }
      };
    }
    // Mostra enllaços admin si el docent té rol admin (best-effort).
    var did = '';
    try { did = localStorage.getItem('atne.docent_id') || ''; } catch (e) { /* ignore */ }
    if (did) {
      fetch('/api/docent/is-admin?docent_id=' + encodeURIComponent(did))
        .then(function (r) { return r.ok ? r.json() : {}; })
        .then(function (d) {
          if (d && d.is_admin) {
            var links = menu.querySelector('#admin-links');
            if (links) links.style.display = '';
          }
        })
        .catch(function () { /* ignore */ });
    }
  }

  function paintAvatar() {
    var btn = document.getElementById('docent-av');
    if (!btn) return;
    // Si pas1 ja té el seu menú propi (amb lògica _updateDocentBtn), no fem res.
    if (document.getElementById('admin-menu')) return;

    var alias = '';
    try { alias = localStorage.getItem('atne.docent_alias') || ''; } catch (e) { /* ignore */ }
    var em = (window.ATNE_AUTH && window.ATNE_AUTH.email) || '';
    var displayName = alias || em;
    if (displayName) {
      btn.textContent = displayName[0].toUpperCase();
      btn.title = 'Docent · ' + (em || alias);
    }
    // Injecta menú i handlers per a pas2/pas3.
    ensureMenuStyles();
    var menu = buildMenu(displayName);
    btn.insertAdjacentElement('afterend', menu);
    attachMenuHandlers(btn, menu, displayName);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', paintAvatar);
  } else {
    paintAvatar();
  }

  // 6. Monkey-patch fetch: afegeix Authorization a crides /api/* del mateix origen
  var originalFetch = window.fetch.bind(window);
  window.fetch = function (input, init) {
    init = init || {};
    var url = typeof input === 'string' ? input : (input && input.url) || '';
    var isApi = url.indexOf('/api/') === 0 ||
                url.indexOf(location.origin + '/api/') === 0;
    if (isApi) {
      var headers = new Headers(init.headers || (typeof input !== 'string' ? input.headers : undefined));
      if (!headers.has('Authorization')) {
        headers.set('Authorization', 'Bearer ' + window.ATNE_AUTH.token);
      }
      init.headers = headers;
    }
    return originalFetch(input, init).then(function (resp) {
      if (isApi && resp.status === 401) {
        // Sessió expirada o invàlida → re-login
        redirectToLogin();
      }
      return resp;
    });
  };
})();
