# Walktour kit

Visita guiada interactiva (tipus producte tour) basada en **Driver.js**.
Vanilla JS, sense dependencies, ~25 kb total.

Origen: extret de l'app ATNE (Fundació Jesuïtes Educació), on s'usa als 3
passos del flux principal.

---

## Què hi ha

| Fitxer | Què és |
|---|---|
| `driver.iife.js` | Llibreria Driver.js (v1.x, build IIFE) |
| `driver.css` | Estils del overlay, spotlight i popover |
| `tour-template.html` | Plantilla mínima funcional - obre-la al navegador i ja veuràs el tour |
| `README.md` | Aquest fitxer |

## Instal·lació

1. Copia `driver.iife.js` i `driver.css` al teu projecte (servits **localment**, no CDN).
2. Inclou-los a la pàgina:
   ```html
   <link rel="stylesheet" href="driver.css"/>
   <script src="driver.iife.js"></script>
   ```
3. Adapta el `steps[]` de la plantilla als selectors i textos de la teva app.

> **Per què local i no CDN?** A xarxes corporatives amb proxy/firewall (cas FJE)
> els CDN externs sovint estan bloquejats. Servir local = zero sorpreses.

## Anatomia d'un step

```js
{
  element: '#selector-css',           // si l'omets → modal central (sense ancoratge)
  popover: {
    title: 'Títol del bocadillo',
    description: 'Text. Accepta HTML: <b>negreta</b>, <br>, emojis.',
    side: 'bottom'                    // top | bottom | left | right
  },
  onHighlightStarted: () => {         // es crida ABANS de mostrar el popover
    // Prepara el DOM: obre un panell, canvia de tab, activa un mode...
  }
}
```

## Configuració global del tour

```js
driver.js.driver({
  showProgress: true,                 // "1 de 12" a la cantonada
  nextBtnText: 'Següent →',
  prevBtnText: '← Anterior',
  doneBtnText: 'Entès!',
  progressText: '{{current}} de {{total}}',
  onDestroyed: () => { /* restaurar UI quan l'usuari surt */ },
  steps: [ ... ]
}).drive();
```

## Trucs importants (apresos al pilot)

### 1. Un tour per pantalla, no un de sol llarguíssim
Cada pàgina, el seu `startTourX()`. Més de 25 steps seguits cansa.

### 2. Si l'element està ocult quan el tour hi arriba, falla
Usa `onHighlightStarted` per fer-lo visible primer:
```js
onHighlightStarted: () => {
  document.querySelector('details.opcions').open = true;
}
```

### 3. Auto-llançament només la primera visita
Si no, esdevé pesat:
```js
if (!localStorage.getItem('app.tour_done')) {
  localStorage.setItem('app.tour_done', '1');
  setTimeout(startTour, 600);
}
```

### 4. Si tens modal d'inici (login, consentiment...), espera que es tanqui
```js
const checkTour = setInterval(() => {
  const overlay = document.getElementById('login-overlay');
  if (!overlay || overlay.classList.contains('hidden')) {
    clearInterval(checkTour);
    setTimeout(startTour, 600);
  }
}, 300);
```

### 5. Restaura l'estat al sortir amb `onDestroyed`
El tour pot deixar la UI en un mode estrany (un `<details>` obert, una tab
activada artificialment...). Neteja-ho:
```js
onDestroyed: () => setMode('default')
```

### 6. Cuidado amb elements `position: fixed`
Si hi poses `side` o `align`, Driver.js pot crashejar. Per als FAB i botons
flotants, deixa el popover sense `side` (es posiciona automàticament).

## Quan NO usar walktour

Si l'usuari ja coneix l'app i només vol consultar què fa un botó concret,
el patró **"mode ajuda contextual"** funciona millor: cursor interrogant +
clic a qualsevol element per veure'n la descripció.

Els dos patrons poden conviure al mateix botó `?`: walktour la primera
visita, mode ajuda contextual a partir de la segona.

## Documentació oficial

https://driverjs.com - exemples, API completa, temes.

## Llicència

Driver.js: MIT (Kamran Ahmed). Aquesta plantilla i el README: lliures d'ús.
