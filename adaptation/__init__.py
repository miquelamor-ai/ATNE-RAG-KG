"""Paquet d'adaptació d'ATNE — mòduls extrets de server.py.

Els submòduls contenen helpers i pipelines que abans vivien dins del
monòlit `server.py`. Tot el que altres fitxers del repo importen amb
`from server import X` continua funcionant: `server.py` els re-exporta.

Mòduls:
    post_process — neteja determinista de la sortida LLM (LaTeX, typos,
                   paraules angleses, concatenacions de prefix) i
                   verificació de longitud de frases / paraules prohibides.
"""
