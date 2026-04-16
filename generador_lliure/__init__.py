"""generador_lliure — m\u00f2dul a\u00efllat de generaci\u00f3 de textos de qualitat Arena.

Aquest m\u00f2dul genera textos educatius des de zero a partir dels par\u00e0metres
del Pas 2 d'ATNE (tema, g\u00e8nere, tipologia, to, llargada, curs, mat\u00e8ria).

Principi rector: a\u00efllat del pipeline d'adaptaci\u00f3. Cap import de
`build_system_prompt`, `instruction_catalog`, `post_process_catalan` ni cap
altra pe\u00e7a contaminadora. L'\u00fanic pont amb server.py \u00e9s `_call_llm_raw`
(dispatcher de providers sense el prefix "TEXT ORIGINAL A ADAPTAR").

\u00cbs el resultat del di\u00e0leg del 2026-04-15 entre Miquel i Claude, motivat pel
cas del castell medieval on Gemma 4 31B produ\u00efa prosa acad\u00e8mica adulta en
comptes de manual escolar de 5\u00e8 de prim\u00e0ria. Veure pla a
`.claude/plans/sorted-juggling-locket.md`.
"""

from .orquestrador import generar, generar_stream

__all__ = ["generar", "generar_stream"]
