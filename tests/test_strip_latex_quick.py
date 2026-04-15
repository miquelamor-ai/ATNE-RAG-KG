"""Quick sanity test for _strip_latex_artifacts — pre-deploy smoke."""
import re

_LATEX_PATTERNS = [
    (r'\$\s*\\rightarrow\s*\$', '→'),
    (r'\$\s*\\leftarrow\s*\$', '←'),
    (r'\$\s*\\uparrow\s*\$', '↑'),
    (r'\$\s*\\downarrow\s*\$', '↓'),
    (r'\$\s*\\leftrightarrow\s*\$', '↔'),
    (r'\$\s*\\Rightarrow\s*\$', '⇒'),
    (r'\$\s*\\Leftarrow\s*\$', '⇐'),
    (r'\$\s*\\xrightarrow\{[^}]*\}\s*\$', '→'),
    (r'\$\s*\\xleftarrow\{[^}]*\}\s*\$', '←'),
    (r'\\rightarrow\b', '→'),
    (r'\\leftarrow\b', '←'),
    (r'\\uparrow\b', '↑'),
    (r'\\downarrow\b', '↓'),
    (r'\\leftrightarrow\b', '↔'),
    (r'\\Rightarrow\b', '⇒'),
    (r'\\Leftarrow\b', '⇐'),
]


def strip(text):
    if not text:
        return text
    for p, r in _LATEX_PATTERNS:
        text = re.sub(p, r, text)
    text = re.sub(r'\\{2,}_', '___', text)
    text = re.sub(r'\\{4,}', '___', text)
    return text


# TEST 1: $\rightarrow$ + runaway backslashes with underscore
t1 = r'La màquina de vapor. () $\rightarrow$ \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_'
r1 = strip(t1)
print('T1 IN :', repr(t1))
print('T1 OUT:', repr(r1))
assert '$\\rightarrow$' not in r1, "LaTeX arrow not stripped"
assert '\\\\\\\\' not in r1, "Runaway backslashes not stripped"
assert '→' in r1 and '___' in r1
print('T1 OK\n')

# TEST 2: omplir buits sense underscore (només backslashes)
t2 = r"L'\\\\\\\\\\\\\\\ és el moviment cap a la \\\\\\\\\\\\\\\."
r2 = strip(t2)
print('T2 IN :', repr(t2))
print('T2 OUT:', repr(r2))
assert '\\\\' not in r2
assert '___' in r2
print('T2 OK\n')

# TEST 3: Plain text with euro sign (must NOT touch)
t3 = 'Costa $10 euros. El procés: causa -> efecte'
r3 = strip(t3)
print('T3 IN :', repr(t3))
print('T3 OUT:', repr(r3))
assert r3 == t3, "Plain text was modified"
print('T3 OK\n')

# TEST 4: Proper Unicode arrow (must NOT touch)
t4 = 'Causa → Conseqüència'
r4 = strip(t4)
assert r4 == t4
print('T4 OK (Unicode arrow preserved)\n')

# TEST 5: $\xrightarrow{texto}$
t5 = r'Mesopotàmia $\xrightarrow{cap a l est}$ Índia'
r5 = strip(t5)
print('T5 IN :', repr(t5))
print('T5 OUT:', repr(r5))
assert 'xrightarrow' not in r5
assert '→' in r5
print('T5 OK\n')

# TEST 6: Orphan \rightarrow without dollars
t6 = r'Causa \rightarrow conseqüència'
r6 = strip(t6)
print('T6 IN :', repr(t6))
print('T6 OUT:', repr(r6))
assert '\\rightarrow' not in r6
assert '→' in r6
print('T6 OK\n')

# TEST 7: Real complement output from user's Case 2
t7 = r"""La màquina de vapor es feia servir per produir aliments. () $\rightarrow$ \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_
El carbó era la font d'energia principal. () $\rightarrow$ \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_
[Literal · omplir buits] L'\\\\\\\\\\\\\\\ és el moviment de gent que marxa del camp cap a la \\\\\\\\\\\\\\\."""
r7 = strip(t7)
print('T7 IN :')
print(t7)
print('T7 OUT:')
print(r7)
assert '\\rightarrow' not in r7
assert '\\\\\\\\' not in r7
assert '→' in r7
assert '___' in r7
print('T7 OK\n')

print('ALL TESTS PASSED')
