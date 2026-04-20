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

  // 5. Monkey-patch fetch: afegeix Authorization a crides /api/* del mateix origen
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
