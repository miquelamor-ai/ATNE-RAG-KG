#!/usr/bin/env bash
# log.sh — Actualitza la capçalera d'estat del SESSION_LOG.md automàticament
# Ús: bash log.sh
# Posa aquest script a l'arrel del repo ATNE.
# Genera la secció "ESTAT ACTUAL" al principi del SESSION_LOG.md
# amb les dades objectives del repo (branques, commits, CI).
# La part de coordinació (xats actius, decisions pendents) l'afegeixes tu a mà.

set -e
LOGFILE="SESSION_LOG.md"
TMPFILE=$(mktemp)

# ── Capçalera d'estat ─────────────────────────────────────────────────────────
cat > "$TMPFILE" << HEADER
# ATNE — SESSION LOG i ESTAT DEL PROJECTE
> **Instrucció d'ús:** executa \`bash log.sh\` per actualitzar la secció d'estat.
> La part objectiva (branques, commits) s'omple automàticament.
> La part de coordinació (xats actius, decisions) l'actualitzes tu a mà sota.

---

## 🗂️ ESTAT ACTUAL — $(date '+%Y-%m-%d %H:%M')

### Repositori
HEADER

# Fetch silenciós
git fetch origin --quiet 2>/dev/null || true

# Branca activa i working tree
echo "- **Branca activa:** \`$(git branch --show-current)\`" >> "$TMPFILE"
if [ -n "$(git status --porcelain)" ]; then
  UNTRACKED=$(git status --porcelain | grep "^??" | wc -l | tr -d ' ')
  MODIFIED=$(git status --porcelain | grep -v "^??" | wc -l | tr -d ' ')
  echo "- **Working tree:** ⚠️ $MODIFIED fitxers modificats · $UNTRACKED untracked" >> "$TMPFILE"
else
  echo "- **Working tree:** ✅ net" >> "$TMPFILE"
fi

# main local vs origin
LOCAL=$(git rev-parse --short main 2>/dev/null || echo "?")
ORIGIN=$(git rev-parse --short origin/main 2>/dev/null || echo "?")
if [ "$LOCAL" = "$ORIGIN" ]; then
  echo "- **main vs origin:** ✅ sincronitzats (\`$LOCAL\`)" >> "$TMPFILE"
else
  echo "- **main vs origin:** ⚠️ local=\`$LOCAL\` · origin=\`$ORIGIN\`" >> "$TMPFILE"
fi

# Últims 3 commits
echo "" >> "$TMPFILE"
echo "**Últims commits a main:**" >> "$TMPFILE"
git log main --oneline -3 2>/dev/null | sed 's/^/- \`/' | sed 's/ /\` /' >> "$TMPFILE"

# Branques obertes vs main
echo "" >> "$TMPFILE"
echo "**Branques obertes (ahead de main):**" >> "$TMPFILE"
FOUND=0
for b in $(git for-each-ref --format='%(refname:short)' refs/heads/ refs/remotes/origin/ \
           | grep -v HEAD | sed 's|origin/||' | sort -u); do
  [ "$b" = "main" ] && continue
  if git rev-parse --verify "$b" >/dev/null 2>&1; then
    ahead=$(git rev-list --count main..$b 2>/dev/null || echo "0")
    behind=$(git rev-list --count $b..main 2>/dev/null || echo "0")
    if [ "$ahead" -gt "0" ] 2>/dev/null; then
      echo "- \`$b\` — $ahead ahead · $behind behind" >> "$TMPFILE"
      FOUND=1
    fi
  fi
done
[ "$FOUND" = "0" ] && echo "- *(cap branca ahead de main)*" >> "$TMPFILE"

# Secció de coordinació (manual)
cat >> "$TMPFILE" << COORD

### 🔴 Espera decisió meva
<!-- Actualitza manualment: push/merge/decisions pendents -->
- 

### 🟡 En marxa (xats actius)
<!-- Actualitza manualment: qui treballa què i a quina branca -->
- 

### 📋 Backlog
- RAG/KG desactivat des del 9/04 — decidir reactivar o retirar
- Neteja branques velles a origin (~15 punters antics)
- Bucle de millora (ADR-003) — bloquejat fins al DPO FJE
- Tercer jutge Claude per al framework d'avaluació
- SVG diagrames a l'export PDF/DOCX
- Multi-agent (Adaptador→Auditor→Corrector→Traductor)
- Memòria triàdica (StudentMemory/ClassMemory/SubjectProfile)
- Decisió motor institucional FJE
- Gemma 4 com a motor sobirà

---

COORD

# Afegir el contingut existent del SESSION_LOG (sense la capçalera antiga si existeix)
if [ -f "$LOGFILE" ]; then
  # Saltar la capçalera antiga (fins al primer "---" + línia buida)
  awk '/^---$/{found++} found>=2{print}' "$LOGFILE" >> "$TMPFILE" || \
  grep -v "^# ATNE" "$LOGFILE" | tail -n +3 >> "$TMPFILE"
fi

mv "$TMPFILE" "$LOGFILE"
echo "✅ $LOGFILE actualitzat — $(date '+%H:%M')"
echo "   Recorda omplir les seccions 🔴 i 🟡 manualment (o demanar-ho al xat)."
