<?php
// Auth FJE (producció). En local, si no existeix, s'omet.
$netsecure = __DIR__ . '/../../lib/NETSecure/NETSecure.php';
if (file_exists($netsecure)) {
    include $netsecure;
}
?>
<!DOCTYPE html>
<html lang="ca">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ATNE — Adaptador de textos</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      font-size: 14px;
      background: #f5f5f0;
      color: #1a1a1a;
      height: 100dvh;
      display: flex;
      flex-direction: column;
    }

    header {
      background: #1a3a2a;
      color: #fff;
      padding: 12px 20px;
      display: flex;
      align-items: center;
      gap: 12px;
      flex-shrink: 0;
    }
    header h1 { font-size: 16px; font-weight: 600; letter-spacing: .3px; }
    header span { font-size: 12px; opacity: .6; }

    .workspace {
      display: grid;
      grid-template-columns: 260px 1fr 1fr;
      gap: 0;
      flex: 1;
      overflow: hidden;
    }

    /* --- PANELL SELECTORS --- */
    .panel-selectors {
      background: #fff;
      border-right: 1px solid #e0ddd8;
      padding: 16px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 18px;
    }

    .field-group label.group-label {
      display: block;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: .6px;
      color: #888;
      margin-bottom: 6px;
    }

    select {
      width: 100%;
      padding: 7px 10px;
      border: 1px solid #d8d5d0;
      border-radius: 6px;
      background: #fafaf8;
      font-size: 13px;
      color: #1a1a1a;
      cursor: pointer;
    }
    select:focus { outline: 2px solid #1a3a2a; outline-offset: 1px; }

    .checkbox-list { display: flex; flex-direction: column; gap: 8px; }

    .checkbox-item {
      display: flex;
      align-items: center;
      gap: 8px;
      cursor: pointer;
    }
    .checkbox-item input[type=checkbox] {
      width: 15px; height: 15px;
      accent-color: #1a3a2a;
      cursor: pointer;
      flex-shrink: 0;
    }
    .checkbox-item span { font-size: 13px; line-height: 1.3; }

    #l1-wrap {
      display: none;
      margin-top: 6px;
      padding-left: 23px;
    }
    #l1-wrap input {
      width: 100%;
      padding: 5px 8px;
      border: 1px solid #d8d5d0;
      border-radius: 5px;
      font-size: 12px;
      background: #fafaf8;
    }
    #l1-wrap input:focus { outline: 2px solid #1a3a2a; outline-offset: 1px; }
    #l1-wrap .hint { font-size: 11px; color: #aaa; margin-top: 3px; }

    .btn-adaptar {
      width: 100%;
      padding: 11px;
      background: #1a3a2a;
      color: #fff;
      border: none;
      border-radius: 7px;
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
      letter-spacing: .3px;
      transition: background .15s;
    }
    .btn-adaptar:hover { background: #245038; }
    .btn-adaptar:disabled { background: #a0b0a8; cursor: not-allowed; }

    /* --- PANELLS TEXT --- */
    .panel-text {
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }

    .panel-text + .panel-text {
      border-left: 1px solid #e0ddd8;
    }

    .panel-header {
      padding: 10px 16px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: .6px;
      color: #888;
      border-bottom: 1px solid #e8e5e0;
      background: #fafaf8;
      flex-shrink: 0;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .panel-header .model-badge {
      font-size: 11px;
      font-weight: 500;
      text-transform: none;
      letter-spacing: 0;
      color: #1a3a2a;
      background: #e8f0eb;
      padding: 2px 8px;
      border-radius: 10px;
    }

    textarea {
      flex: 1;
      width: 100%;
      padding: 16px;
      border: none;
      resize: none;
      font-size: 14px;
      line-height: 1.6;
      background: #fff;
      color: #1a1a1a;
      font-family: inherit;
    }
    textarea:focus { outline: none; }
    textarea::placeholder { color: #bbb; }

    .result-area {
      flex: 1;
      padding: 16px;
      overflow-y: auto;
      background: #fff;
      font-size: 14px;
      line-height: 1.7;
      color: #1a1a1a;
    }

    .result-area.empty { color: #bbb; font-style: italic; }

    .result-area p { margin-bottom: .9em; }
    .result-area p:last-child { margin-bottom: 0; }
    .result-area h2, .result-area h3 {
      font-size: 13px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: .5px;
      color: #555;
      margin: 1.4em 0 .5em;
      padding-bottom: 4px;
      border-bottom: 1px solid #eee;
    }
    .result-area ul { padding-left: 18px; margin-bottom: .9em; }
    .result-area li { margin-bottom: .3em; }

    /* Spinner */
    .spinner {
      display: none;
      width: 22px; height: 22px;
      border: 3px solid #d0d8d4;
      border-top-color: #1a3a2a;
      border-radius: 50%;
      animation: spin .7s linear infinite;
      margin: 40px auto;
    }
    @keyframes spin { to { transform: rotate(360deg); } }

    .error-msg {
      color: #b94040;
      font-size: 13px;
      padding: 12px;
      background: #fff5f5;
      border-radius: 6px;
      border: 1px solid #f0c0c0;
    }

    /* Scrollbar discreta */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #ccc; border-radius: 3px; }
  </style>
</head>
<body>

<header>
  <h1>ATNE</h1>
  <span>Adaptador de textos educatius</span>
</header>

<div class="workspace">

  <!-- SELECTORS -->
  <div class="panel-selectors">

    <div class="field-group">
      <label class="group-label" for="nivell">Nivell</label>
      <select id="nivell">
        <option value="A1">A1 — Lectura Fàcil</option>
        <option value="A2">A2 — Bàsic</option>
        <option value="B1" selected>B1 — Intermedi</option>
        <option value="B2">B2 — Avançat</option>
        <option value="C1">C1 — Acadèmic</option>
        <option value="enriquiment">Enriquiment</option>
      </select>
    </div>

    <div class="field-group">
      <label class="group-label">Perfil</label>
      <div class="checkbox-list">
        <label class="checkbox-item">
          <input type="checkbox" name="perfil" value="nouvingut" id="cb-nouvingut">
          <span>Nouvingut</span>
        </label>
        <div id="l1-wrap">
          <input type="text" id="l1" placeholder="Llengua d'origen (ex: àrab)">
          <div class="hint">Opcional — per traduir el glossari</div>
        </div>
        <label class="checkbox-item">
          <input type="checkbox" name="perfil" value="tdah">
          <span>TDAH</span>
        </label>
        <label class="checkbox-item">
          <input type="checkbox" name="perfil" value="dislexia">
          <span>Dislèxia / TDL</span>
        </label>
        <label class="checkbox-item">
          <input type="checkbox" name="perfil" value="tea">
          <span>TEA</span>
        </label>
        <label class="checkbox-item">
          <input type="checkbox" name="perfil" value="altes_capacitats">
          <span>Altes capacitats</span>
        </label>
      </div>
    </div>

    <div class="field-group">
      <label class="group-label">Complements</label>
      <div class="checkbox-list">
        <label class="checkbox-item">
          <input type="checkbox" name="complement" value="glossari">
          <span>Glossari</span>
        </label>
        <label class="checkbox-item">
          <input type="checkbox" name="complement" value="preguntes">
          <span>Preguntes de comprensió</span>
        </label>
      </div>
    </div>

    <div class="field-group">
      <label class="group-label" for="model">Model</label>
      <select id="model">
        <option value="o1-mini">o1-mini — Raonament</option>
        <option value="gpt-4.1">GPT-4.1</option>
        <option value="gpt-4o" selected>GPT-4o ★</option>
        <option value="gpt-4o-mini">GPT-4o mini</option>
        <option value="gpt-4.1-mini">GPT-4.1 mini</option>
      </select>
    </div>

    <button class="btn-adaptar" id="btn-adaptar" onclick="adaptar()">Adaptar</button>

  </div>

  <!-- TEXT ORIGINAL -->
  <div class="panel-text">
    <div class="panel-header">Text original</div>
    <textarea id="text-original" placeholder="Enganxa aquí el text que vols adaptar..."></textarea>
  </div>

  <!-- TEXT ADAPTAT -->
  <div class="panel-text">
    <div class="panel-header">
      <span>Text adaptat</span>
      <span class="model-badge" id="model-badge" style="display:none"></span>
    </div>
    <div class="result-area empty" id="result">
      El text adaptat apareixerà aquí.
    </div>
    <div class="spinner" id="spinner"></div>
  </div>

</div>

<script>
  // Mostra/amaga el camp L1 quan se selecciona Nouvingut
  document.getElementById('cb-nouvingut').addEventListener('change', function () {
    document.getElementById('l1-wrap').style.display = this.checked ? 'block' : 'none';
  });

  function adaptar() {
    const text = document.getElementById('text-original').value.trim();
    if (!text) {
      alert('Enganxa un text primer.');
      return;
    }

    const nivell      = document.getElementById('nivell').value;
    const model       = document.getElementById('model').value;
    const l1          = document.getElementById('l1').value.trim();
    const perfils     = [...document.querySelectorAll('input[name=perfil]:checked')].map(c => c.value);
    const complements = [...document.querySelectorAll('input[name=complement]:checked')].map(c => c.value);

    const btn     = document.getElementById('btn-adaptar');
    const spinner = document.getElementById('spinner');
    const result  = document.getElementById('result');
    const badge   = document.getElementById('model-badge');

    btn.disabled    = true;
    btn.textContent = 'Adaptant...';
    result.style.display  = 'none';
    spinner.style.display = 'block';
    badge.style.display   = 'none';

    fetch('api/adaptar.php', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ text, nivell, perfils, complements, model, l1 }),
    })
    .then(r => r.json())
    .then(data => {
      spinner.style.display = 'none';
      result.style.display  = 'block';
      btn.disabled    = false;
      btn.textContent = 'Adaptar';

      if (data.error) {
        result.className = 'result-area';
        result.innerHTML = `<div class="error-msg">⚠ ${data.error}</div>`;
        return;
      }

      result.className = 'result-area';
      result.innerHTML = renderText(data.adapted);
      badge.textContent   = model;
      badge.style.display = 'inline-block';
    })
    .catch(err => {
      spinner.style.display = 'none';
      result.style.display  = 'block';
      btn.disabled    = false;
      btn.textContent = 'Adaptar';
      result.className = 'result-area';
      result.innerHTML = `<div class="error-msg">⚠ Error de connexió: ${err.message}</div>`;
    });
  }

  // Conversió bàsica de markdown a HTML
  function renderText(text) {
    return text
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      .replace(/^#{1,3} (.+)$/gm, '<h2>$1</h2>')
      .replace(/^[-•] (.+)$/gm, '<li>$1</li>')
      .replace(/(<li>.*<\/li>)/gs, m => `<ul>${m}</ul>`)
      .replace(/\n{2,}/g, '</p><p>')
      .replace(/\n/g, '<br>')
      .replace(/^/, '<p>').replace(/$/, '</p>')
      .replace(/<p><\/p>/g, '')
      .replace(/<p>(<h[23]>)/g, '$1')
      .replace(/(<\/h[23]>)<\/p>/g, '$1')
      .replace(/<p>(<ul>)/g, '$1')
      .replace(/(<\/ul>)<\/p>/g, '$1');
  }
</script>

</body>
</html>
