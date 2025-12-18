"""
Prompt Engine — MindScan

Gera prompts dinâmicos para interação com o usuário ou outros sistemas.
Baseado nos resultados e personas.
"""

from typing import Dict, Any


class PromptEngine:
    def generate_prompt(self, persona: Dict[str, Any]) -> str:
        """
        Gera um prompt dinâmico com base nas características da persona.

        :param persona: dados da persona.
        :return: prompt gerado.
        """
        return f"Olá {persona['name']}, com base no seu perfil, aqui estão as suas sugestões."
