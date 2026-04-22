# Exemple — El cicle de l'aigua (Primària CM, Ciències Naturals, MECR A2)

Aquest exemple mostra el comportament esperat de la skill
`generate-illustracions` aplicada a un text adaptat per a alumnat de 4t de
Primària amb MECR A2.

## Text adaptat ORIGINAL (sense il·lustracions)

```markdown
### El cicle de l'aigua

L'aigua es mou pel planeta. No es gasta. Canvia de forma.

Primer, el sol escalfa l'aigua del mar. L'aigua es converteix en vapor.
El vapor puja al cel. Això es diu evaporació.

Després, el vapor es fa fred a dalt. El vapor es converteix en gotes
petites. Les gotes formen els núvols. Això es diu condensació.

Quan hi ha moltes gotes, cauen a terra. Cauen com pluja, neu o pedra.
Això es diu precipitació.

L'aigua torna als rius. Els rius porten l'aigua al mar. I el cicle
comença de nou.
```

## Text adaptat AMB marcadors d'il·lustracions

```markdown
### El cicle de l'aigua

L'aigua es mou pel planeta. No es gasta. Canvia de forma.

[IMATGE: Warm morning sun shining over a calm blue-green sea, faint wisps of water vapour rising gently from the surface towards the sky, three-quarter view, eye-level, soft horizon line.]

Primer, el sol escalfa l'aigua del mar. L'aigua es converteix en vapor.
El vapor puja al cel. Això es diu evaporació.

[IMATGE: Two large fluffy white clouds against a pale blue sky, small water droplets visible forming inside the clouds, three-quarter view, eye-level, soft gentle breeze, no ground visible.]

Després, el vapor es fa fred a dalt. El vapor es converteix en gotes
petites. Les gotes formen els núvols. Això es diu condensació.

[IMATGE: A soft rainfall descending from grey cumulus clouds onto a green meadow with a small stream, three-quarter view, waist-up framing of the meadow, gentle afternoon light, no people visible.]

Quan hi ha moltes gotes, cauen a terra. Cauen com pluja, neu o pedra.
Això es diu precipitació.

L'aigua torna als rius. Els rius porten l'aigua al mar. I el cicle
comença de nou.
```

## Raonament de cada marcador

### Marcador 1 — Evaporació

> Warm morning sun shining over a calm blue-green sea, faint wisps of
> water vapour rising gently from the surface towards the sky,
> three-quarter view, eye-level, soft horizon line.

- **Subjecte primer**: "Warm morning sun" — obre amb l'element visual dominant.
- **Acció concreta**: "rising gently from the surface" — verb actiu, no
  abstracte.
- **Viewpoint explícit**: "three-quarter view, eye-level".
- **Setting específic**: "calm blue-green sea".
- **Lighting**: "warm morning" — reforça l'hora del dia.
- **Sense estil**: no apareix "watercolor", "flat", etc. (ho afegeix el
  backend).
- **Sense "white background"**: evitem el bug blanc-sobre-blanc; el
  `positive_suffix` ja posa "soft cream paper background".

### Marcador 2 — Condensació

> Two large fluffy white clouds against a pale blue sky, small water
> droplets visible forming inside the clouds, three-quarter view,
> eye-level, soft gentle breeze, no ground visible.

- **Quantitat concreta**: "Two large fluffy white clouds" — millor que "some
  clouds".
- **Contrast explícit**: "against a pale blue sky" — evita el bug clàssic
  de núvols blancs invisibles sobre fons clar.
- **Detall pedagògic**: "small water droplets visible forming inside" —
  reforça el concepte de condensació.
- **Composició**: "no ground visible" — manté el focus a dalt.

### Marcador 3 — Precipitació

> A soft rainfall descending from grey cumulus clouds onto a green meadow
> with a small stream, three-quarter view, waist-up framing of the
> meadow, gentle afternoon light, no people visible.

- **Matís d'estat d'ànim**: "soft rainfall" en lloc de "heavy rain" o
  "storm" — evita el to fosc de la iteració 1 de les proves.
- **Connexió amb el pas següent**: "a small stream" prepara visualment el
  següent paràgraf sobre rius.
- **Evita humans**: "no people visible" — FLUX-schnell falla sovint en
  anatomia, millor evitar-los si no aporten.
- **Enquadrament parcial**: "waist-up framing" — evita superfícies
  complexes a baix.

## Prompt FINAL que rep FLUX (construcció del backend)

Per al marcador 1, el prompt complet enviat a Pollinations serà aproximadament:

```
Cozy watercolour children's textbook illustration, soft warm palette of
ochre, sap green and cream, gentle paper grain, subtle vignette,
three-quarter view, storybook aesthetic. Warm morning sun shining over a
calm blue-green sea, faint wisps of water vapour rising gently from the
surface towards the sky, three-quarter view, eye-level, soft horizon
line. Single clear focal point, clean composition, soft cream paper
background, gentle shadow under the subject, no text, no letters, no
captions, no signage.
```

I els paràmetres de Pollinations:

```
model=flux
seed=<hash del document>       (mateixa per a totes les imatges)
enhance=false                  (CRÍTIC: no reescriure)
safe=true
private=true
width=1024
height=768
nologo=true
referrer=atne-fje
```

## Notes pedagògiques

- **Màxim 3 marcadors per aquest document** — respecta el límit general
  de la skill (3-4 per document) i és adequat al nombre de fases del cicle.
- **No marcador al darrer paràgraf** ("L'aigua torna als rius...") — és un
  tancament conceptual ja inclòs en el marcador 3, afegir-n'hi un seria
  redundant.
- **Si un docent vol un marcador més** per al riu del final, podria ser:
  > A gentle river winding through a green valley towards a distant sea,
  > three-quarter view, eye-level, soft afternoon light, no people
  > visible.
  Però cal valorar si realment afegeix comprensió o és decoratiu.
