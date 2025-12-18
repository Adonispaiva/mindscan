"""
Prompt Service — MindScan

Serviço de geração de prompts dinâmicos.
Integra com o PromptEngine.
"""

from backend.mi.prompts.prompt_engine import PromptEngine


class PromptService:
    def __init__(self):
        self.engine = PromptEngine()

    def create_prompt(self, persona: dict) -> str:
        return self.engine.generate_prompt(persona)
