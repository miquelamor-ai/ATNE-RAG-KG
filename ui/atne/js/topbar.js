/*
 * ATNE — topbar.js  (zoom + pantalla completa compartit)
 *
 * Carregar en <head> SENSE defer: s'ha d'aplicar el zoom abans de pintar
 * per evitar el parpelleig de layout (FOUC).
 * Clau localStorage: 'atne.app_zoom'  (0.6 – 1.8, pas 0.1)
 */
(function () {
  'use strict';

  var KEY = 'atne.app_zoom';

  function clamp(v) { return Math.max(0.6, Math.min(1.8, v)); }
  function round1(v) { return Math.round(v * 10) / 10; }
  function readZoom() { return clamp(round1(parseFloat(localStorage.getItem(KEY) || '1'))); }

  function applyZoom(z) {
    z = clamp(round1(z));
    document.documentElement.style.zoom = z;
    document.documentElement.style.minHeight = (100 / z) + 'vh';
    document.documentElement.style.setProperty('--app-zoom', z);
    try { localStorage.setItem(KEY, String(z)); } catch (e) {}
    var lbl = document.getElementById('zoom-label');
    if (lbl) lbl.textContent = Math.round(z * 100) + '%';
  }

  // Aplica el zoom desat IMMEDIATAMENT (abans que el CSS pinti)
  var _z = readZoom();
  if (_z !== 1) applyZoom(_z);

  function setup() {
    applyZoom(readZoom()); // reaplica per actualitzar el label

    document.getElementById('zoom-out')?.addEventListener('click', function () { applyZoom(readZoom() - 0.1); });
    document.getElementById('zoom-in')?.addEventListener('click',  function () { applyZoom(readZoom() + 0.1); });
    document.getElementById('zoom-label')?.addEventListener('click', function () { applyZoom(1); });

    document.getElementById('fullscreen-btn')?.addEventListener('click', function () {
      if (!document.fullscreenElement) document.documentElement.requestFullscreen && document.documentElement.requestFullscreen();
      else document.exitFullscreen && document.exitFullscreen();
    });

    document.addEventListener('fullscreenchange', function () {
      var btn = document.getElementById('fullscreen-btn');
      if (!btn) return;
      if (document.fullscreenElement) {
        btn.title = 'Sortir de pantalla completa (F11)';
        btn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 3v3a2 2 0 0 1-2 2H3m18 0h-3a2 2 0 0 1-2-2V3m0 18v-3a2 2 0 0 1 2-2h3M3 16h3a2 2 0 0 1 2 2v3"/></svg>';
      } else {
        btn.title = 'Pantalla completa (F11)';
        btn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 7V3h4M17 3h4v4M21 17v4h-4M7 21H3v-4"/></svg>';
      }
    });

    // Atalls de teclat estàndard
    document.addEventListener('keydown', function (e) {
      if (!(e.ctrlKey || e.metaKey)) return;
      if (e.key === '+' || e.key === '=') { e.preventDefault(); applyZoom(readZoom() + 0.1); }
      else if (e.key === '-') { e.preventDefault(); applyZoom(readZoom() - 0.1); }
      else if (e.key === '0') { e.preventDefault(); applyZoom(1); }
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', setup);
  else setup();
})();
