"""Quick sanity test for _strip_latex_artifacts — pre-deploy smoke."""
import re
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from adaptation.post_process import _strip_latex_artifacts as strip


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

# TEST 8: $\text{...}$ amb backslashes dins (cas nou sessio 15/04)
t8 = r'Augment de fàbriques $\rightarrow$ $\text{\\\\\\\\\\}$ (Opcions: Més contaminació / Més agricultura)'
r8 = strip(t8)
print('T8 IN :', repr(t8))
print('T8 OUT:', repr(r8))
assert r'\text' not in r8
assert r'\rightarrow' not in r8
assert '→' in r8
assert '___' in r8
print('T8 OK\n')

# TEST 9: \text{...} orfe sense $
t9 = r'El \text{\\\\\} i els canals van facilitar el comerç.'
r9 = strip(t9)
print('T9 IN :', repr(t9))
print('T9 OUT:', repr(r9))
assert r'\text' not in r9
assert '___' in r9
print('T9 OK\n')

# TEST 10: real prompt sortida complement amb tot junt
t10 = r"""[Literal · V/F amb justificació] Marca si és V o F:
La classe treballadora tenia condicions de vida molt bones. ( ) $\rightarrow$ ""
[Literal · omplir buits] El $\text{\\\\\\\\\\}$ i els canals van facilitar el comerç.
[Inferencial · relaciona] Augment de fàbriques $\rightarrow$ $\text{\\\\\\\\\\}$"""
r10 = strip(t10)
print('T10 IN :')
print(t10)
print('T10 OUT:')
print(r10)
assert r'\rightarrow' not in r10
assert r'\text{' not in r10
assert '→' in r10
assert '___' in r10
print('T10 OK\n')

# ── NOVES FUNCIONS DE POST-PROCESSAT ─────────────────────────────────────

_ENGLISH_REPLACEMENTS = {
    'owners': 'propietaris', 'owner': 'propietari',
    'workers': 'treballadors', 'worker': 'treballador',
    'factory': 'fàbrica', 'factories': 'fàbriques',
    'inventions': 'invencions', 'invention': 'invenció',
    'employees': 'empleats', 'employee': 'empleat',
}


def fix_english(text):
    if not text:
        return text
    for en, cat in _ENGLISH_REPLACEMENTS.items():
        text = re.sub(r'\b' + re.escape(en) + r'\b', cat, text)
        text = re.sub(r'\b' + re.escape(en.capitalize()) + r'\b', cat.capitalize(), text)
        text = re.sub(r'\b' + re.escape(en.upper()) + r'\b', cat.upper(), text)
    return text


_TYPO_FIXES = {
    'possuïen': 'posseïen', 'possuïa': 'posseïa',
    'luitar': 'lluitar', 'luita': 'lluita',
    'produïguessin': 'produïssin',
    'sobrecarga': 'sobrecàrrega', 'localizar': 'localitzar',
}


def fix_typos(text):
    if not text:
        return text
    for bad, good in _TYPO_FIXES.items():
        text = re.sub(r'\b' + re.escape(bad) + r'\b', good, text)
        text = re.sub(r'\b' + re.escape(bad.capitalize()) + r'\b', good.capitalize(), text)
    return text


_CONCAT_RE = re.compile(r'\b[A-Za-zÀ-ÿ]{8,25}\b')


def fix_concat(text):
    if not text:
        return text
    def repl(m):
        w = m.group(0)
        for i in range(3, len(w) - 2):
            if w[i:].lower().startswith(w[:i].lower()):
                return w[i:]
        return w
    return _CONCAT_RE.sub(repl, text)


def full_post_process(text):
    text = strip(text)
    text = fix_concat(text)
    text = fix_english(text)
    text = fix_typos(text)
    return text


print('\n── NOUS TESTS ──\n')

# T11: owners → propietaris
t11 = 'Persones riques que eren owners de les fàbriques. La Burgesia són els Owners.'
r11 = full_post_process(t11)
print('T11:', r11)
assert 'owners' not in r11.lower()
assert 'propietaris' in r11
assert 'Propietaris' in r11
print('T11 OK\n')

# T12: typos
t12 = 'La gent possuïa fàbriques i volia luitar contra la sobrecarga.'
r12 = full_post_process(t12)
print('T12:', r12)
assert 'possuïa' not in r12  # typo has disappeared
assert 'sobrecarga ' not in r12 and 'sobrecarga.' not in r12  # no castellanisme
assert 'posseïa' in r12
assert 'lluitar' in r12
assert 'sobrecàrrega' in r12
# Verificar que 'luitar' només apareix com a part de 'lluitar' (no com a mot sol)
assert re.search(r'\bluitar\b', r12) is None
print('T12 OK\n')

# T13: concatenacions
t13 = 'La Revolrevolució industrial va ser important. Els moviments sociasocials.'
r13 = full_post_process(t13)
print('T13:', r13)
assert 'Revolrevolució' not in r13
assert 'sociasocials' not in r13
assert 'revolució' in r13.lower()
assert 'socials' in r13
print('T13 OK\n')

# T14: Revolucirevolució (concat mes llarga)
t14 = 'La Revolucirevolució industrial'
r14 = full_post_process(t14)
print('T14:', r14)
assert 'Revolucirevolució' not in r14
assert 'revolució' in r14.lower()
print('T14 OK\n')

# T15: paraules legitimes no tocades
t15 = 'Conseqüències de la Revolució industrial per a la societat moderna.'
r15 = full_post_process(t15)
print('T15:', r15)
assert r15 == t15, f"Legitimate text modified: {repr(r15)}"
print('T15 OK\n')

# T16: LaTeX malformat $(ightarrow$
t16 = r'La classe treballadora. () $(ightarrow$ _____________'
r16 = full_post_process(t16)
print('T16:', r16)
assert '(ightarrow' not in r16
assert '→' in r16
print('T16 OK\n')

# T17: real complement output (combinat)
t17 = r"""La burgesia (les persones riques que eren owners de les fàbriques).
La classe treballadora possuïa pocs drets i volia luitar.
La Revolrevolució industrial va ser important.
Augment de fàbriques $\rightarrow$ $\text{\\\\\\\\}$"""
r17 = full_post_process(t17)
print('T17:')
print(r17)
assert 'owners' not in r17
assert 'possuïa' not in r17
assert re.search(r'\bluitar\b', r17) is None
assert 'Revolrevolució' not in r17
assert r'\rightarrow' not in r17
assert r'\text{' not in r17
print('T17 OK\n')

print('ALL TESTS PASSED')

# ── TESTS ADR-004: Preservació de fórmules matemàtiques i químiques ──────────
print('\n── TESTS ADR-004: fórmules STEAM ──\n')

# T18: fórmula inline simple — ha de sobreviure intacta
t18 = r'La força és $F = m \cdot a$ on $m$ és la massa.'
r18 = strip(t18)
print('T18:', r18)
assert '$F = m \\cdot a$' in r18, f"Fórmula F=ma destruïda: {repr(r18)}"
assert '$m$' in r18, f"Fórmula m destruïda: {repr(r18)}"
print('T18 OK (fórmules inline preservades)\n')

# T19: fórmula display ($$...$$) — ha de sobreviure intacta
t19 = r'La densitat és:' + '\n' + r'$$\rho = \frac{m}{V}$$' + '\n' + 'on m és la massa i V el volum.'
r19 = strip(t19)
print('T19:', r19)
assert r'$$\rho = \frac{m}{V}$$' in r19, f"Fórmula display destruïda: {repr(r19)}"
print('T19 OK (fórmula display preservada)\n')

# T20: fórmula química — ha de sobreviure intacta
t20 = r'La fotosíntesi: $6CO_2 + 6H_2O \rightarrow C_6H_{12}O_6 + 6O_2$'
r20 = strip(t20)
print('T20:', r20)
assert r'6CO_2 + 6H_2O \rightarrow C_6H_{12}O_6 + 6O_2' in r20, f"Fórmula química destruïda: {repr(r20)}"
print('T20 OK (fórmula química amb \\rightarrow preservada)\n')

# T21: fórmula STEAM + artefacte al mateix text — fórmula preservada, artefacte eliminat
t21 = r'La velocitat és $v = \frac{d}{t}$. Causa $\rightarrow$ efecte.'
r21 = strip(t21)
print('T21:', r21)
assert r'$v = \frac{d}{t}$' in r21, f"Fórmula v=d/t destruïda: {repr(r21)}"
# L'artefacte $\rightarrow$ (fletxa sola) ha de convertir-se a Unicode
assert '$\\rightarrow$' not in r21, f"Artefacte $\\rightarrow$ no eliminat: {repr(r21)}"
assert '→' in r21, f"Fletxa Unicode no present: {repr(r21)}"
print('T21 OK (fórmula preservada + artefacte eliminat)\n')

# T22: equació amb subíndexs i superíndexs
t22 = r'L\'energia cinètica és $E_k = \frac{1}{2}mv^2$.'
r22 = strip(t22)
print('T22:', r22)
assert r'$E_k = \frac{1}{2}mv^2$' in r22, f"Fórmula energia cinètica destruïda: {repr(r22)}"
print('T22 OK (equació amb sub/superíndex preservada)\n')

# T23: preu en euros ($ aïllat) — no ha de tocar-se
t23 = 'El material costa $15 euros per unitat.'
r23 = strip(t23)
print('T23:', r23)
assert r23 == t23, f"Preu en euros modificat: {repr(r23)}"
print('T23 OK (preu en euros no tocat)\n')

# T24: fórmula química ATNE pòster científic
t24 = r'El pH neutre és $pH = 7$ i l\'aigua és $H_2O$.'
r24 = strip(t24)
print('T24:', r24)
assert '$pH = 7$' in r24, f"Fórmula pH destruïda: {repr(r24)}"
assert '$H_2O$' in r24, f"Fórmula H2O destruïda: {repr(r24)}"
print('T24 OK (fórmules química i física preservades)\n')

print('ALL ADR-004 TESTS PASSED')
