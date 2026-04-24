/*
 * ATNE — Auth client (lanet)
 *
 * Flux:
 *  1. Si no hi ha token → redirigeix a lanet_bridge.php (FJE)
 *  2. El bridge valida el cookie tokenNet i redirigeix de tornada amb
 *     ?atne_token=XXX&atne_login=mamor a la URL
 *  3. Guardem token i login a localStorage
 *  4. Monkey-patching de fetch: afegeix Authorization: Bearer a /api/*
 *  5. En cas de 401 → redirigeix al bridge de nou
 *
 * Carregar com a primer <script> del <head>, sense defer/async.
 */
(function () {
  'use strict';

  // URL del bridge PHP desplegat a FJE. Canviar si canvia el path al servidor.
  var BRIDGE_URL = (window.ATNE_CONFIG && window.ATNE_CONFIG.bridgeUrl)
    || 'https://apinet5.net.fje.edu/atne/lanet_bridge.php';

  var LS_TOKEN = 'atne_jwt';
  var LS_LOGIN = 'atne_login';

  function clearSession() {
    try {
      localStorage.removeItem(LS_TOKEN);
      localStorage.removeItem(LS_LOGIN);
      localStorage.removeItem('atne.docent_id');
      localStorage.removeItem('atne.docent_alias');
    } catch (e) { /* ignore */ }
  }

  function redirectToBridge() {
    clearSession();
    var back = location.origin + location.pathname + location.search;
    location.href = BRIDGE_URL + '?back=' + encodeURIComponent(back);
  }

  // 1. Captura token retornat pel bridge (?atne_token=...&atne_login=...)
  var urlParams = new URLSearchParams(location.search);
  var tokenFromBridge = urlParams.get('atne_token');
  var loginFromBridge = urlParams.get('atne_login');
  if (tokenFromBridge && loginFromBridge) {
    try {
      localStorage.setItem(LS_TOKEN, tokenFromBridge);
      localStorage.setItem(LS_LOGIN, loginFromBridge);
    } catch (e) { /* ignore */ }
    // Neteja els paràmetres de la URL (no deixar token exposat)
    try {
      var clean = new URL(location.href);
      clean.searchParams.delete('atne_token');
      clean.searchParams.delete('atne_login');
      history.replaceState(null, '', clean.pathname + (clean.search || ''));
    } catch (e) { /* ignore */ }
  }

  // 2. Llegim el token actual de localStorage
  var currentToken = null;
  var currentLogin = null;
  try {
    currentToken = localStorage.getItem(LS_TOKEN);
    currentLogin = localStorage.getItem(LS_LOGIN);
  } catch (e) { /* ignore */ }

  // 3. Si no hi ha token, redirigim al bridge
  if (!currentToken || !currentLogin) {
    redirectToBridge();
    throw new Error('ATNE: redirigint a lanet');
  }

  // 4. Exposem l'API d'auth (mateixa interfície que l'anterior per Supabase)
  window.ATNE_AUTH = {
    token:  currentToken,
    login:  currentLogin,
    email:  currentLogin,   // àlies de compatibilitat
    logout: function () { redirectToBridge(); },
  };

  // 5. Pinta l'avatar del docent (#docent-av)
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
        '<a href="/admin" target="_blank" rel="noopener">Admin <span class="admin-badge">ADMIN</span></a>' +
        '<a href="/ui/cuina.html" target="_blank" rel="noopener">Cuina (dev)</a>' +
        '<div class="sep"></div>' +
      '</div>' +
      '<div class="sep"></div>' +
      '<button id="admin-logout-btn">Canviar d\'usuari</button>';
    return div;
  }

  function attachMenuHandlers(btn, menu, alias) {
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
          if (window.ATNE_AUTH && typeof window.ATNE_AUTH.logout === 'function') {
            window.ATNE_AUTH.logout();
          } else {
            location.reload();
          }
        }
      };
    }
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
    if (document.getElementById('admin-menu')) return;

    var alias = '';
    try { alias = localStorage.getItem('atne.docent_alias') || ''; } catch (e) { /* ignore */ }
    var displayName = alias || currentLogin || '';
    if (displayName) {
      btn.textContent = displayName[0].toUpperCase();
      btn.title = 'Docent · ' + displayName;
    }
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
        var isAdminPath = url.indexOf('/api/admin/') >= 0 || url.indexOf('/api/audit/') >= 0;
        if (!isAdminPath) {
          redirectToBridge();
        }
      }
      return resp;
    });
  };
})();
