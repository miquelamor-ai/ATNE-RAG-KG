"""Verificacio rapida post-refactor: les funcions re-exportades via server.py
retornen exactament el mateix que les mateixes funcions del modul nou."""
import sys
sys.path.insert(0, '.')

from server import (
    _strip_latex_artifacts, _post_process_llm_output,
    clean_gemini_output, post_process_adaptation,
    MECR_MAX_WORDS, FORBIDDEN_WORDS,
)
from adaptation import post_process as pp

# 1. Les funcions de `server` son EXACTAMENT les mateixes que les d'`adaptation.post_process`
assert _strip_latex_artifacts is pp._strip_latex_artifacts, "server.X != pp.X"
assert clean_gemini_output is pp.clean_gemini_output, "server.X != pp.X"

# 2. LaTeX: fletxes
r = _strip_latex_artifacts(r'El preu $\rightarrow$ 10 euros')
assert r == 'El preu \u2192 10 euros', f"fletxa fail: {r!r}"

# 3. LaTeX: text placeholder
r = _strip_latex_artifacts(r'hola $\text{res}$ mon')
assert r == 'hola ___ mon', f"text fail: {r!r}"

# 4. English words
r = _post_process_llm_output('owners i workers a la factory')
assert r == 'propietaris i treballadors a la fàbrica', f"english fail: {r!r}"

# 5. Typos
r = _post_process_llm_output('possuïen moltes terres')
assert r == 'posseïen moltes terres', f"typo fail: {r!r}"

# 6. Concatenacions
r = _post_process_llm_output('La Revolrevolució industrial')
assert 'Revolrevolució' not in r, f"concat fail: {r!r}"
assert 'revolució' in r, f"concat fail: {r!r}"

# 7. clean_gemini_output — normalitza heading sense espai
r = clean_gemini_output('##Preguntes de comprensió\n\ntext')
assert r.startswith('## Preguntes'), f"heading fail: {r!r}"

# 8. post_process_adaptation — metriques
report = post_process_adaptation('Hola mon. Aixo es una prova.', 'A1')
assert report['metrics']['paraules'] == 6, f"metrics fail: {report}"
assert isinstance(report['warnings'], list), f"warnings fail: {report}"

# 9. Constants preservades
assert MECR_MAX_WORDS['A1'] == 8
assert MECR_MAX_WORDS['B2'] == 25
assert 'cosa' in FORBIDDEN_WORDS

print("OK - 9 checks passed. Refactor post_process.py preserva comportament.")
