"""
CROSS Big5 × TEIQue — Versão ULTRA SUPERIOR
-------------------------------------------------------------

Relaciona traços de personalidade com dimensões emocionais
(TRAIT Emotional Intelligence Questionnaire).

Foca em:
- expressividade
- percepção emocional
- empatia
- autorregulação
- adaptabilidade emocional
"""

from typing import Dict, Any


class CrossBig5Teique:
    def __init__(self):
        self.version = "2.0-ultra"

    def generate(self, big5: Dict[str, float], teique: Dict[str, float]) -> Dict[str, Any]:
        patterns = {}

        # Neuroticismo + Baixa Regulação
        if big5.get("neuroticismo", 0) >= 65 and teique.get("regulacao", 0) <= 40:
            patterns["risco_emocional"] = (
                "Neuroticismo alto aliado à baixa regulação emocional — risco elevado."
            )

        # Amabilidade + Empatia
        if big5.get("amabilidade", 0) >= 60 and teique.get("empatia", 0) >= 55:
            patterns["empatia_situacional"] = (
                "Forte convergência entre amabilidade e empatia."
            )

        # Extroversão + Expressividade
        if big5.get("extroversao", 0) >= 60 and teique.get("expressividade", 0) >= 50:
            patterns["expressividade_social"] = (
                "Extroversão bem canalizada para comunicação emocional."
            )

        # Baixa Abertura + Baixa Adaptabilidade emocional
        if big5.get("abertura", 0) <= 30 and teique.get("adaptabilidade", 0) <= 40:
            patterns["rigidez_emocional"] = (
                "Possível rigidez emocional devido à baixa abertura e flexibilidade."
            )

        return {
            "module": "cross_big5_teique",
            "version": self.version,
            "patterns": patterns,
        }
