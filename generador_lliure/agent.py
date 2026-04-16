"""Agent LLM del m\u00f2dul generador_lliure.

Encapsula la crida a un LLM via `server._call_llm_raw` (\u00fanic pont amb el
codi antic d'ATNE). Responsabilitat \u00fanica: donat un system, un user i un
model_id, retornar el text generat. Res m\u00e9s.

Aquest agent NO fa:
- Construcci\u00f3 de prompt (\u00e9s al m\u00f2dul `prompt.py`)
- Validaci\u00f3 de par\u00e0metres (\u00e9s a l'orquestrador)
- Post-processament del text generat
- Cap crida a `build_system_prompt`, `instruction_catalog`, `post_process_catalan`
- Cap l\u00f2gica de fallback ni retry (ho fa `_call_llm_raw` amb rotaci\u00f3 de claus)
"""

from __future__ import annotations


class AgentGenerador:
    """Wrapper prim sobre `_call_llm_raw` per a generaci\u00f3 des de zero.

    `model_id` pot ser:
    - un \u00e0lies curt: "gemma3", "qwen", "gpt-4o", "mistral-large"...
    - un model_id llarg: "gemma-3-12b-it", "qwen/qwen3.5-27b"...
    - una string buida → fall-back a l'ATNE_MODEL via `_resolve_model`.
    """

    def __init__(
        self,
        model_id: str,
        temperature: float = 1.0,
        top_p: float = 0.95,
        max_tokens: int = 2048,
    ):
        self.model_id = model_id or ""
        self.temperature = float(temperature)
        self.top_p = float(top_p)
        self.max_tokens = int(max_tokens)

    def generate(self, system: str, user: str) -> str:
        """Genera text. Pot aixecar RuntimeError si totes les claus fallen."""
        # Import local per evitar cicle en arrencada (server.py \u00e9s el que
        # importa aquest m\u00f2dul). L'import local es resol al moment de la
        # primera crida, quan server.py ja est\u00e0 totalment inicialitzat.
        from server import _call_llm_raw

        return _call_llm_raw(
            model_id=self.model_id,
            system_prompt=system,
            user_text=user,
            temperature=self.temperature,
            top_p=self.top_p,
            max_tokens=self.max_tokens,
        )

    def generate_stream(self, system: str, user: str):
        """Genera text en mode streaming.

        Retorna un generador s\u00edncron de chunks (str) a mesura que el LLM
        els produeix. Cost i tokens totals id\u00e8ntics a `generate()`; l'\u00fanic
        avantatge \u00e9s que el consumidor (endpoint SSE al Pas 2) pot
        re-emetre cada chunk al frontend per a una UX en temps real.
        """
        from server import _call_llm_stream

        return _call_llm_stream(
            model_id=self.model_id,
            system_prompt=system,
            user_text=user,
            temperature=self.temperature,
            top_p=self.top_p,
            max_tokens=self.max_tokens,
        )
