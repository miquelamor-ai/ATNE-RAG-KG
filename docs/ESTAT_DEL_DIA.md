# ESTAT DEL DIA — ATNE i projectes germans
> Taulell únic entre tots els xats. L'obro al matí, l'actualitzo quan canvio de
> tasca o tanco un xat, el llegeixo quan torno a una sessió després d'estona.
> Regla d'or: si una cosa no és aquí, no existeix. El cap no ha de recordar res.

**Data:** 2026-06-13  ·  **Última actualització:** 2026-06-13 (matí)

---

## 🔴 EL QUE ESPERA UNA ACCIÓ MEVA (push / merge / decisió)
> Només jo puc fer aquestes. Si la llista és buida, no tinc cap foc encès.

| Què | Branca / lloc | Pendent de | Bloqueja? |
|---|---|---|---|
| Sincronitzar main local amb origin | main (local 041c791 → origin e08fe44) | `git pull` (sense la teva ordre no el toco) | no |

---

## 🟡 EN MARXA ARA (xats treballant)
> Una fila per tasca activa. "Xat" = com el tinc anomenat o on és (Antigravity, claude.ai).

| Tasca | Xat / sessió | Branca | Working tree | Estat |
|---|---|---|---|---|
| _(cap tasca de codi activa)_ | | | | |

---

## ✅ TANCAT AVUI (per no re-obrir el fil sense voler)
> El que ja està fet i pujat/decidit. Si un xat torna a treure'l, és que no ho sap.

- Node 24 → main e08fe44, branques esborrades, límit 16/06 cobert
- J2 cross-judge → completat amb jutge gemini-2.5-flash, ADR-002 firmat
  _(21/21 judicis, rotació 6 claus; informe a `tests/results/experiment_combinat_20260613_113558.md`; ADR a `docs/adr/ADR-002-decisio-models-adaptador.md`. Dada completa: candidats empatats dins variància → decideix compliance; corregit l'artefacte self-judging de gpt-4o)_

---

## 📋 BACKLOG (quan hi hagi calma, sense pressa)
- Bloc B editor Novak (diferit a sessió pròpia)
- Verificar Actions reals al GitHub (canon-guards depèn del secret CORPUSFJE_PAT; gh no disponible a la màquina)

---

## ⚙️ MAPA D'INFRAESTRUCTURA (referència fixa, rarament canvia)
> Per no haver-ho de recordar ni preguntar a cap xat.

- **Repos:** `origin` = miquelamor-ai/ATNE-RAG-KG · `fje` = FundacioJesuitesEducacio/ATNE
- **Working tree local:** C:\Users\miquel.amor\Documents\GitHub\ATNE\  ⚠️ compartit entre xats
- **Projectes germans:** mineriaRAG (corpus/canon) · Itinerarium/mirar-coms (consum índex)
- **Regla de governança:** cap xat fa push/merge sense la meva ordre · cap xat canvia
  de branca si un altre treballa al working tree compartit.

---

### Com l'uso (3 moments)
1. **Obro un xat nou** → primera línia: "Vinc de [tasca], branca [X]; aquí vull [Z]". Enganxo context del taulell.
2. **Canvio de tasca o tanco un xat** → actualitzo les taules 🔴🟡✅ (30 segons).
3. **Torno a un xat after estona** → llegeixo el taulell abans de res. En 10 segons sé on soc.

### Quan val la pena un worktree
Si DOS xats han de tocar CODI alhora en branques diferents → `git worktree add ../ATNE-[tasca] [branca]`.
Un directori per tasca = cap xat mou el terra a un altre. (No cal per a tasques que només llegeixen o consulten.)
