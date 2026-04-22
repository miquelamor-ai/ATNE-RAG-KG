/*
 * ATNE — Consent gate (Sprint 1C, 2026-04-22)
 *
 * S'inclou immediatament després de auth.js a totes les pàgines pas1/pas2/pas3.
 * Si el docent (autenticat amb @fje.edu) no ha donat ni acceptat ni declinat el
 * consentiment per al pilot, redirigeix a /ui/atne/consent.html.
 *
 * Comprovacions:
 *   1) Si el docent encara no està autenticat → no fem res (auth.js ja redirigeix).
 *   2) Si l'usuari ja és a consent.html → no redirigim (evitar loop).
 *   3) Comprovem LocalStorage primer (rapid). Si no, intentem Supabase
 *      (`/api/pilot/consent/{email}`).
 *   4) Si no hi ha decisió → redirigir a consent.html.
 *
 * NO bloquegem la pàgina si Supabase falla — assumim acceptació tàcita
 * perquè el pilot no s'ha d'aturar per un problema de xarxa transitori.
 */
(function () {
  'use strict';

  if (location.pathname.indexOf('consent.html') !== -1) return;

  var STORAGE_KEY = 'atne_pilot_consent';
  var CONSENT_PAGE = '/ui/atne/consent.html';

  function getDocentEmail() {
    try {
      if (window.ATNE_AUTH && window.ATNE_AUTH.email) return window.ATNE_AUTH.email;
      return localStorage.getItem('atne_user_email') || '';
    } catch (e) { return ''; }
  }

  function localDecision() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return null;
      var p = JSON.parse(raw);
      return (p && (p.decision === 'accepted' || p.decision === 'declined')) ? p.decision : null;
    } catch (e) { return null; }
  }

  function persistDecisionLocally(decision, ts) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify({
        decision: decision,
        ts: ts || new Date().toISOString(),
      }));
    } catch (e) { /* ignore */ }
  }

  function redirectToConsent() {
    location.href = CONSENT_PAGE;
  }

  // 1) Si encara no hi ha auth, no fem res — auth.js gestionarà el login.
  var email = getDocentEmail();
  if (!email) return;

  // 2) Si tenim decisió local, deixa passar (cas habitual: ràpid).
  if (localDecision()) return;

  // 3) Mirem si Supabase recorda alguna decisió per aquest docent (canvi de
  //    navegador / esborrat de LocalStorage). Si retorna `accepted` o
  //    `declined`, sincronitzem a LocalStorage i deixem passar. Si retorna
  //    null, redirigim. Si falla la xarxa, assumim acceptació tàcita.
  fetch('/api/pilot/consent/' + encodeURIComponent(email))
    .then(function (r) { return r.ok ? r.json() : { ok: false }; })
    .then(function (d) {
      if (d && d.ok && d.decision) {
        persistDecisionLocally(d.decision, d.ts);
        return; // no redirect
      }
      redirectToConsent();
    })
    .catch(function () { /* xarxa fallida → no bloquegem */ });
})();
