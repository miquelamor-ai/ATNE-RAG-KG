"""
evaluator_agent.py — BLOC 3: Agent avaluador LLM-as-a-judge.

L'agent rep:
  - Text original
  - Perfil declarat (caracteristiques, MECR, DUA)
  - System prompts generats per CADA branca (Hardcoded i RAG)
  - Textos adaptats per CADA branca
  - Metriques BLOC 1-2 precalculades

L'agent fa:
  1. Verifica que cada system prompt es coherent amb el perfil declarat
  2. Avalua cada text adaptat amb criteris C1-C5 (+C6 si creuament)
  3. Compara les dues branques i emet un veredicte

Referencia: docs/decisions/avaluacio_agent_v2.md
"""

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

_client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options=types.HttpOptions(timeout=180_000),
)

MODEL = "gemini-2.5-flash"

# ═══════════════════════════════════════════════════════════════════════════════
# SYSTEM PROMPT DE L'AVALUADOR
# ═══════════════════════════════════════════════════════════════════════════════

EVALUATOR_SYSTEM = """Ets un avaluador pedagogic expert i esceptic. La teva feina es avaluar i comparar adaptacions de textos educatius generades per dues branques d'un sistema (Hardcoded i RAG).

REGLES:
1. NO aprovies per defecte. Puntua basant-te EXCLUSIVAMENT en evidencia present al text.
2. Si una instruccio del perfil NO te evidencia directa al text adaptat, puntua baix.
3. Justifica cada puntuacio en UNA frase concisa.
4. Retorna NOMES el JSON demanat, sense text addicional ni blocs de codi (```).
5. Escriu en catala.

TASCA PER CADA CAS:

## FASE 1: Auditoria dels system prompts
Per cada branca, respon:
- El system prompt es coherent amb el perfil declarat? (si/no + motiu)
- Quines instruccions rellevants hi falten? (llista breu)
- Quines instruccions son irrellevants o contradictories? (llista breu)

## FASE 2: Avaluacio dels textos adaptats
Per cada branca, puntua de l'1 al 5:

C1 COHERENCIA: El text es internament consistent? Les idees flueixen logicament? Hi ha connectors?
C2 ADEQUACIO AL PERFIL: Les instruccions del perfil s'han aplicat? Hi ha evidencia directa?
C3 PRESERVACIO CURRICULAR: El contingut original es mante sense omissions ni errors?
C4 ADEQUACIO MECR: Lexic, sintaxi i complexitat corresponen al MECR declarat?
C5 PRELLICO FUNCIONAL: Hi ha glossari previ o organitzador que prepari cognitivament?
C6 COHERENCIA CREUAMENT: (NOMES si 2+ perfils) S'han aplicat tots els perfils sense contradiccio?

INVERSIO C2 PER ALTES CAPACITATS:
Si el perfil es altes_capacitats o DUA=Enriquiment, C2 es: "El text ofereix aprofundiment, connexions complexes i repte cognitiu? S'han suprimit les regles de simplificacio?"

## FASE 3: Comparacio
- Quina branca es millor en forma? Per que?
- Quina branca es millor en fons? Per que?
- Veredicte global: quina branca ha produit la millor adaptacio per a AQUEST cas?
"""

# ═══════════════════════════════════════════════════════════════════════════════
# USER PROMPT (template per a cada cas)
# ═══════════════════════════════════════════════════════════════════════════════

USER_PROMPT_TEMPLATE = """## Cas: {cas_id}

### PERFIL DECLARAT
- Perfils actius: {perfils_actius}
- MECR sortida: {mecr}
- DUA: {dua}
- Etapa: {etapa}
- Genere: {genere}

### TEXT ORIGINAL
{text_original}

---

### BRANCA HARDCODED

**System prompt (instruccions de perfil enviades):**
{prompt_hardcoded}

**Metriques forma (precalculades):**
{forma_hardcoded}

**Text adaptat:**
{text_hardcoded}

---

### BRANCA RAG

**System prompt (instruccions filtrades enviades):**
{prompt_rag}

**Metriques forma (precalculades):**
{forma_rag}

**Retrieval Recall:** {recall_rag}

**Text adaptat:**
{text_rag}

---

Retorna el JSON amb l'estructura seguent (sense blocs de codi):
{{
  "cas_id": "{cas_id}",
  "auditoria_prompt": {{
    "hardcoded": {{
      "coherent_amb_perfil": true/false,
      "motiu": "...",
      "instruccions_absents": ["..."],
      "instruccions_irrellevants": ["..."]
    }},
    "rag": {{
      "coherent_amb_perfil": true/false,
      "motiu": "...",
      "instruccions_absents": ["..."],
      "instruccions_irrellevants": ["..."]
    }}
  }},
  "avaluacio": {{
    "hardcoded": {{
      "C1": {{"p": 1-5, "j": "..."}},
      "C2": {{"p": 1-5, "j": "..."}},
      "C3": {{"p": 1-5, "j": "..."}},
      "C4": {{"p": 1-5, "j": "..."}},
      "C5": {{"p": 1-5, "j": "..."}},
      "puntuacio_fons": 0.0
    }},
    "rag": {{
      "C1": {{"p": 1-5, "j": "..."}},
      "C2": {{"p": 1-5, "j": "..."}},
      "C3": {{"p": 1-5, "j": "..."}},
      "C4": {{"p": 1-5, "j": "..."}},
      "C5": {{"p": 1-5, "j": "..."}},
      "puntuacio_fons": 0.0
    }}
  }},
  "comparacio": {{
    "millor_forma": "hardcoded" o "rag",
    "motiu_forma": "...",
    "millor_fons": "hardcoded" o "rag",
    "motiu_fons": "...",
    "veredicte": "hardcoded" o "rag" o "empat",
    "motiu_veredicte": "..."
  }}
}}
"""


def build_eval_prompt(
    cas_id: str,
    perfils_actius: list[str],
    mecr: str,
    dua: str,
    etapa: str,
    genere: str,
    text_original: str,
    prompt_hardcoded: str,
    text_hardcoded: str,
    forma_hardcoded: dict,
    prompt_rag: str,
    text_rag: str,
    forma_rag: dict,
    recall_rag: float,
) -> str:
    """Construeix el prompt de l'usuari per a un cas d'avaluacio."""
    return USER_PROMPT_TEMPLATE.format(
        cas_id=cas_id,
        perfils_actius=", ".join(perfils_actius),
        mecr=mecr,
        dua=dua,
        etapa=etapa,
        genere=genere,
        text_original=text_original,
        prompt_hardcoded=prompt_hardcoded,
        text_hardcoded=text_hardcoded,
        forma_hardcoded=json.dumps(forma_hardcoded, ensure_ascii=False, indent=2),
        prompt_rag=prompt_rag,
        text_rag=text_rag,
        forma_rag=json.dumps(forma_rag, ensure_ascii=False, indent=2),
        recall_rag=recall_rag,
    )


def evaluate_case(user_prompt: str) -> dict:
    """
    Envia un cas a l'LLM avaluador i retorna el JSON d'avaluacio.

    Usa Gemini Flash amb el system prompt esceptic.
    """
    response = _client.models.generate_content(
        model=MODEL,
        contents=[
            types.Content(role="user", parts=[types.Part(text=user_prompt)]),
        ],
        config=types.GenerateContentConfig(
            system_instruction=EVALUATOR_SYSTEM,
            temperature=0.2,  # Baix per consistencia
            max_output_tokens=8192,
        ),
    )

    raw = response.text if response.text else ""
    raw = raw.strip()

    if not raw:
        return {"error": "Resposta buida de l'avaluador", "raw_response": ""}

    # Estrategia 1: buscar el JSON entre el primer { i l'últim }
    start = raw.find("{")
    end = raw.rfind("}")
    if start != -1 and end != -1:
        candidate = raw[start:end + 1]
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass

    # Estrategia 2: netejar blocs ```json ... ```
    import re
    json_block = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", raw, re.DOTALL)
    if json_block:
        try:
            return json.loads(json_block.group(1).strip())
        except json.JSONDecodeError:
            pass

    return {
        "error": "No s'ha pogut parsejar el JSON de l'avaluador",
        "raw_response": raw[:2000],
    }


# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS per construir el prompt de la branca Hardcoded
# ═══════════════════════════════════════════════════════════════════════════════

def get_hardcoded_profile_block(profile_keys: list[str]) -> str:
    """Retorna el bloc de perfil de la branca Hardcoded (constants de prompt_blocks.py)."""
    try:
        from prompt_blocks import PROFILE_BLOCKS
        parts = []
        for key in profile_keys:
            block = PROFILE_BLOCKS.get(key, "")
            if block:
                parts.append(block)
        return "\n\n".join(parts) if parts else "(cap bloc de perfil)"
    except ImportError:
        return "(prompt_blocks.py no disponible en aquesta branca)"
