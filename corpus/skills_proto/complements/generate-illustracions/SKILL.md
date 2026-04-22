---
name: generate-illustracions
description: >
  Use when the teacher has activated the "illustracions" complement (BETA).
  Instructs the LLM to insert [IMATGE: <concepte curt en català>] markers at
  key visual points in the adapted text. The BACKEND resolves each marker
  via a 3-step pipeline: (1) Wikimedia Commons search, (2) FLUX fallback,
  (3) skip if not renderable. The LLM only places markers; it does NOT
  write English briefs — that's the backend's job.
author: FJE — Fundació Jesuïtes Educació
version: 0.3.0-proto
complement_key: illustracions
agent_role: complements
tools_required:
  - name: image_generation
    provider: pollinations
    endpoint: "https://image.pollinations.ai/prompt/{prompt}"
    model: flux
    params:
      enhance: false         # CRITICAL: default rewrites prompt → breaks style consistency
      safe: true
      private: true
      width: 1024
      height: 768
      nologo: true
      referrer: atne-fje
      seed_strategy: document  # same seed for every image of the same document
    # Common positive suffix appended after style + subject (FLUX-schnell ignores
    # negative prompts, so phrase as positive).
    positive_suffix: >-
      Single clear focal point, clean composition,
      soft cream paper background,
      no text, no letters, no captions, no signage.
    # Seven validated style presets (empirical tests 2026-04-21/22).
    # Backend picks one based on teacher selection or default_mapping.
    default_preset: aquarela_storybook
    style_presets:
      vectorial_editorial:
        label_ca: "Vectorial editorial pla"
        spine: >-
          Flat vector illustration, clean geometric shapes, bold simple
          outlines, limited flat color palette, smooth shapes, friendly
          editorial style, no gradients, no texture, centered composition.
        default_for:
          mecr: [B1, B2, C1, C2]
          subjects: [socials, ciutadania, economia, filosofia, llengua]
      isometric_infografic:
        label_ca: "Isomètric infogràfic"
        spine: >-
          Isometric 3D illustration, 30 degree angle, clean geometric shapes,
          crisp edges, limited color palette with soft pastels, subtle
          shading, infographic textbook style, high clarity.
        default_for:
          mecr: [A2, B1, B2, C1, C2]
          subjects: [tecnologia, fisica, quimica, biologia_sistemes, matematiques]
      aquarela_storybook:
        label_ca: "Aquarel·la storybook"
        spine: >-
          Soft watercolor storybook illustration, gentle wet-edge washes,
          warm palette of ochre sap green and dusty blue, hand-drawn feel,
          cozy lighting, loose brushwork, paper texture background, children
          book aesthetic.
        default_for:
          mecr: [A1, A2]
          subjects: [literatura, contes, ciencies_naturals_primaria, religio]
          contexts: [lectura_facil, nouvinguts, primaria_inicial, primaria_mitja]
      icona_minimalista:
        label_ca: "Icona minimalista"
        spine: >-
          Minimalist flat icon, single concept, centered, thick rounded
          outlines, two or three flat colors, solid shapes, no gradient,
          generous padding, pictogram style, high legibility.
        default_for:
          contexts: [dua_acces, vocabulari_abstracte, glossari_visual]
      claymation_plastilina:
        label_ca: "Claymation plastilina"
        spine: >-
          Handmade claymation style, stop-motion plasticine figures, soft
          studio lighting, visible fingerprint texture, saturated but warm
          colors, shallow depth of field, tabletop scene, cheerful children's
          educational look.
        default_for:
          mecr: [A1, A2, B1]
          contexts: [primaria_stem_ludic, infantil]
      escala_grisos_carbonet:
        label_ca: "Escala de grisos (carbonet)"
        spine: >-
          Monochrome charcoal and graphite drawing, soft grey tones,
          hand-drawn on textured cream paper, expressive loose lines, subtle
          cross-hatching, high contrast, no color, editorial book
          illustration style, dignified historical feel.
        default_for:
          subjects: [historia, filosofia, literatura_classica]
          contexts: [impressio_bn, baixa_visio_contrast]
      fotografia_documental:
        label_ca: "Fotografia documental"
        spine: >-
          Vintage documentary photograph, warm sepia and amber tones, 35mm
          film grain, natural soft window light, shallow depth of field,
          authentic atmosphere, editorial photojournalism style, slight age
          patina.
        default_for:
          subjects: [natura, arquitectura, geografia, ciencies_actuals]
        # Reglament especific de transparencia (veure feedback Miquel 2026-04-22):
        restrictions:
          require_caption: "Il·lustració IA"        # caption sota la imatge al PDF/HTML
          people_framing: wide_or_silhouette_only   # si el subjecte inclou persones
          forbidden_framings: [close_up, portrait, waist_up_with_people]
          rationale: >-
            Les fotos IA amb persones en primer pla poden confondre's amb
            documents reals. Plans amplis, mitjana distancia o silueta son
            segurs. Sempre exportar amb caption "Il·lustració IA".
triggers:
  - path: params.complements.illustracions
    equals: true
---

# Afegir il·lustracions generades amb IA al text adaptat (BETA)

## Quan activar aquesta skill

Activar quan el docent ha marcat el complement **"Il·lustracions"** al Pas 2.
Les il·lustracions són **imatges generades per IA** (FLUX.1-schnell) que
s'insereixen al text adaptat per reforçar la comprensió de conceptes clau.

**Feature BETA — avisos obligatoris a la UI**:
- Qualitat NO garantida: la IA interpreta lliurement. Revisar sempre.
- Demora 1-3 min segons saturació del servei gratuït Pollinations.ai.

## IMPORTANT — Separació estricta de responsabilitats

**Tu (el LLM adaptador)** fas **només una cosa**: decidir ON posar el
marcador i escriure-hi un **concepte curt en català**.

**El backend** s'encarrega de tota la resta:
1. Un **agent Gemma 3** analitza el marcador + text original + text adaptat +
   paràgraf circumdant i produeix: query de cerca optimitzada, classificació
   (macroscòpic/metafòric/tècnic-micro), i brief visual en anglès si cal.
2. **Cerca Wikimedia Commons** amb la query. Si troba imatge de qualitat →
   la fa servir + atribució CC obligatòria.
3. **Fallback FLUX-schnell** amb el brief visual si Wikimedia no troba.
4. **Skip** si la classificació és tècnic-micro i no hi ha banc ni metàfora.

Així **tu no has d'escriure res en anglès, ni briefs, ni estils, ni
viewpoints**. Només el concepte en català.

## Els 7 presets disponibles

El frontmatter `style_presets` defineix 7 estils validats empíricament
(proves 2026-04-21/22 amb text del cicle de l'aigua i Revolució Industrial):

| Preset | Per a qui/què |
|---|---|
| `vectorial_editorial` | ESO+, humanitats, conceptes abstractes |
| `isometric_infografic` | STEM, processos, sistemes, diagrames |
| `aquarela_storybook` | Primària, LF, nouvinguts, literatura |
| `icona_minimalista` | DUA Accés, vocabulari, glossari visual |
| `claymation_plastilina` | Primària STEM lúdic, infantil |
| `escala_grisos_carbonet` | Història, filosofia, impressió B/N, baixa visió |
| `fotografia_documental` | Natura, arquitectura, geografia, ciència actual |

**Selecció**: el docent pot triar-ne un al Pas 2; si no, el backend aplica
el `default_for` del frontmatter (MECR + assignatura + context).

## Format del marcador

```
[IMATGE: <concepte curt en català>]
```

- **Delimitadors obligatoris**: `[IMATGE:` a l'inici, `]` al final. El backend
  extreu amb regex.
- **Idioma**: **català**. El backend tradueix i optimitza si cal.
- **En línia pròpia**, abans del paràgraf que introdueix el concepte
  (respecta la regla LF «imatges abans del text»).
- **Longitud**: **3-8 paraules**. Concepte nuclear, no descripció d'escena.

### Exemples de marcadors ben escrits

- `[IMATGE: cicle de l'aigua]`
- `[IMATGE: fàbrica tèxtil de la revolució industrial]`
- `[IMATGE: fulla capturant la llum del sol]`
- `[IMATGE: piràmide alimentària]`
- `[IMATGE: sistema solar]`

### Exemples de marcadors MAL escrits

- ❌ `[IMATGE: a beautiful green leaf with sunlight rays...]` (anglès + massa llarg)
- ❌ `[IMATGE: la revolució industrial]` (massa abstracte; millor una escena concreta)
- ❌ `[IMATGE: watercolor illustration of X]` (no ha d'incloure estil)

## Com escollir el concepte a il·lustrar

- Ha de ser **visualitzable** i **concret**. Un lloc, un objecte, una
  escena, un procés físic observable.
- **No** conceptes purament abstractes: "la democràcia", "la justícia",
  "l'amor" (a no ser que el paràgraf parli d'un exemple visual concret).
- Si el paràgraf parla d'un concepte tècnic-microscòpic (cèl·lula, àtom,
  enzim), **evita el marcador** o formula'l a nivell macroscòpic observable
  (ex: en lloc de `[IMATGE: cloroplasts]`, usa `[IMATGE: fulla verda sota el
  sol]`).

## On col·locar els marcadors

- **Abans** del paràgraf o secció que introdueix el concepte.
- **Màxim 1 marcador per secció major** (un títol H2/H3).
- **Màxim 3-4 marcadors per document sencer**. Més sobrecarrega
  pedagògicament i multiplica la demora de generació.
- **Mai** dins de llistes, taules, bastides, glossaris o altres complements.
  Només al cos del text adaptat.
- **Mai** abans d'un concepte trivial o purament verbal. Una il·lustració
  només si aporta ancoratge visual real.

## Regles estrictes de la sortida

1. **Preserva el text adaptat íntegre**. El marcador **s'afegeix**, no
   substitueix cap paràgraf.
2. El marcador va **en línia pròpia**, sense prefix ni sufix.
3. **NO generis una secció final** del tipus `## Il·lustracions` amb llista
   de descripcions. Els marcadors viuen inline al text adaptat.
4. **SEMPRE en català** dins el marcador. El backend tradueix si cal.
5. **NO afegeixis estil, paleta, viewpoint, enquadrament**. El backend ho
   afegeix automàticament.
6. **3-8 paraules** màxim dins el marcador. Concepte nuclear, no escena.
7. Si tens dubtes sobre si un concepte mereix il·lustració, **NO la posis**.
   Menys i millor.

## Exemple complet

Veure `assets/exemple-primaria-ciencies.md` (Cicle Mitjà, Ciències Naturals,
MECR A2, text sobre el cicle de l'aigua) per veure exemple abans/després
amb 3 marcadors ben col·locats i el raonament de cada descripció.

## Criteris d'èxit (per a revisors)

Una il·lustració generada amb aquesta skill compleix el criteri d'èxit si:

- **Es reconeix el concepte** que il·lustra (criteri mínim pedagògic).
- **Estil coherent** amb les altres il·lustracions del mateix document
  (mateix preset aplicat a totes).
- **Sense text escombraria** dins la imatge (per a tots els presets excepte
  casos futurs amb Qwen-Image).
- **Sense artefactes greus** (mans deformades, ulls descentrats). Si el
  preset és fotografia, **sense retrats**.
- **Apropiada a l'edat** de l'alumnat destinatari.

Si falla qualsevol, el docent pot fer servir **Regenerar** (mateixa
descripció, seed diferent) o **Substituir** (penjar-ne una de pròpia).
