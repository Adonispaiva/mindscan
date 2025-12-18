"""
Persona Service — MindScan

Serviço de geração de personas.
Integra com o PersonaEngine.
"""

from backend.mi.persona.persona_engine import PersonaEngine


class PersonaService:
    def __init__(self):
        self.engine = PersonaEngine()

    def create_persona(self, results: dict) -> dict:
        return self.engine.generate(results)
