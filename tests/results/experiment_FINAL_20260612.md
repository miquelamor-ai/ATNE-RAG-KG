> ⚠️ **ARXIVAT** — Informe de treball del 12/06, SUPERAT per l'**ADR-002 (13/06)**.
> La valoració de gpt-4o aquí es basava en **self-judging**; el cross-judge net la
> corregeix. Vegeu `docs/adr/ADR-002-decisio-models-adaptador.md`.

# Experiment models Adaptador — informe FINAL · 2026-06-12

**Candidats:** gemini-3.5-flash · gemini-2.5-flash · gpt-5 · gpt-4o (baseline producció)
**Casos:** 6 sintètics (NOUV pre-A1, DI, TEA, dislèxia, 2e, AACC) · prompt = build_system_prompt real
**Cost total:** ~€1.0 (sota cap 2€)

## ⚠️ Caveat metodològic (jutge creuat incomplet)

- **J1 = gpt-4.1-mini: COMPLET** (cross-vendor per als candidats Gemini, auto per als GPT).
- **J2 (cross-vendor per als GPT) = NO completat avui.** El free tier de Gemini bloqueja:
  `gemini-2.5-flash` esgotat (20 req/dia) i `gemini-2.0-flash` té `limit: 0` (no és free).
  → Per completar el J2 cal: (a) demà (quota reset), o (b) **Vertex / Gemini de pagament**.
- Passada parcial prèvia (gemini-2.5-flash, 7 judicis) abans del bloqueig:
  gpt-5 auto 4.97 → **creuat 4.53** · gpt-4o auto 4.7 → **creuat 4.1** (self-judging confirmat).

## Dades COMPLETES i FIABLES (no depenen del J2)

### Latència i cost (deterministes)
| Candidat | Latència mediana | Tokens out mediana | Cost/gen | Veredicte |
|---|---|---|---|---|
| gpt-4o | **15s** | 1064 | €0.03 | ràpid |
| gemini-2.5-flash | 32s | 2387 | **€0** (free) | OK |
| gemini-3.5-flash | 42s | 1688 | €0 (free) | OK |
| **gpt-5** | **98s** ⚠ | **8304** ⚠ | €0.15 | **lent + car (raonament)** |

### Fons (C1-C5, jutge J1) PER CAS — les diferències són als EXTREMS
| Cas | gemini-3.5 | gemini-2.5 | gpt-5* | gpt-4o* |
|---|---|---|---|---|
| **NOUV_preA1** (extrem) | **3.6** | 4.6 | 4.8 | 4.0 |
| DI_moderat | 4.8 | 5 | 5 | 4.8 |
| TEA_n2 | 5 | 4.8 | 5 | 4.8 |
| DISLEXIA | (503) | 4.8 | 5 | 4.8 |
| 2e | (503) | (503) | 5 | 4.8 |
| AACC | 4.8 | 5 | 5 | 5 |

### C5 català PER CAS — el català fluixeja a l'extrem
| Cas | gemini-3.5 | gemini-2.5 | gpt-5* | gpt-4o* |
|---|---|---|---|---|
| **NOUV_preA1** (extrem) | 4 | 4 | 4 | **3** ⚠ |
| (resta de casos) | 5 | 5 | 5 | 5 |

*\* gpt-5/gpt-4o auto-jutjats per J1 (mateix proveïdor) → INFLATS. El creuat real era ~4.5/~4.1.*

## Lectures clau (el que importa per decidir)

1. **A NOUV_preA1 (el perfil més extrem: nouvingut pre-A1, àrab, alfabet no-llatí) és on es
   veuen les diferències** — just on Miquel deia que pesarien:
   - **gpt-4o cau a C5 català = 3** (la seva qualitat de català baixa a l'extrem). 🚩
   - gemini-3.5-flash cau a fons 3.6 (el més fluix global).
   - gemini-2.5-flash es manté sòlid (4.6, C5=4) sense caigudes.
   - gpt-5 "guanya" (4.8) PERÒ a **170s i 13.158 tokens** per a una adaptació pre-A1 → absurd.
2. **Self-judging confirmat** (gpt-4.1-mini inflava els GPT).
3. **Diferències petites** entre candidats viables → **mana compliance (UE/Vertex)**.

## Decisió → veure `docs/adr/ADR-002-decisio-models-adaptador.md`
- Prototip personal: **gemini-2.5-flash es manté** (consistent, free, sense caigudes als extrems).
- **gpt-5 descartat** (latència 98s + cost raonament). **gpt-4o qüestionat** (C5 català fluix a
  l'extrem + cross-score baix); mini-run gpt-4.1-mini/gpt-5-mini si l'stack queda OpenAI.
- Re-test trimestral (synthetic monitoring Fase 4).

## Pendent (no bloquejant)
Completar el J2 cross-vendor demà (quota Gemini reset) o via Vertex, per firmar els números GPT.
No canvia la decisió: gpt-5 fora per latència/cost (dada completa); gpt-4o pendent mini-run.
