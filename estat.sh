#!/usr/bin/env bash
# estat.sh — taulell automàtic de l'estat del repo ATNE
# Ús: ./estat.sh   (des de dins del repo)
# Genera la part "objectiva" del taulell del dia; la part de coordinació
# (qui treballa què, què espera decisió teva) l'afegeixes tu a mà a sota.

set -e
echo "═══════════════════════════════════════════════════════════"
echo "  ESTAT ATNE — $(date '+%Y-%m-%d %H:%M')"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Branca actual i si el working tree està net
echo "▸ WORKING TREE"
echo "  Branca activa: $(git branch --show-current)"
if [ -n "$(git status --porcelain)" ]; then
  echo "  ⚠️  HI HA CANVIS SENSE DESAR (un altre xat hi treballa?):"
  git status --porcelain | head -8 | sed 's/^/      /'
else
  echo "  ✅ net (cap canvi pendent)"
fi
echo ""

# Fetch silenciós per comparar amb origin (read-only)
git fetch origin --quiet 2>/dev/null || echo "  (no s'ha pogut fer fetch; estat local)"

# Totes les branques: posició vs main
echo "▸ BRANQUES vs main"
MAIN=$(git rev-parse origin/main 2>/dev/null || git rev-parse main)
for b in $(git for-each-ref --format='%(refname:short)' refs/heads/ refs/remotes/origin/ | grep -v HEAD | sed 's|origin/||' | sort -u); do
  [ "$b" = "main" ] && continue
  if git rev-parse --verify "$b" >/dev/null 2>&1; then
    ahead=$(git rev-list --count main..$b 2>/dev/null || echo "?")
    behind=$(git rev-list --count $b..main 2>/dev/null || echo "?")
    if [ "$ahead" = "0" ]; then
      echo "  ✅ $b — ja dins de main (punter antic, es pot esborrar)"
    else
      echo "  🔵 $b — $ahead ahead · $behind behind"
    fi
  fi
done
echo ""

# main local vs origin
echo "▸ main vs origin/main"
la=$(git rev-parse --short main 2>/dev/null)
oa=$(git rev-parse --short origin/main 2>/dev/null)
if [ "$la" = "$oa" ]; then
  echo "  ✅ sincronitzats ($la)"
else
  echo "  ⚠️  main local=$la · origin=$oa (push pendent?)"
fi
echo ""
echo "▸ Últims 3 commits a main"
git log main --oneline -3 2>/dev/null | sed 's/^/  /'
echo ""
echo "─── (la part de coordinació — qui treballa què, què espera"
echo "     decisió teva — l'afegeixes tu a sota) ───"
