"""
CROSS TEIQue × Big Five — Versão ULTRA SUPERIOR
-------------------------------------------------------------

Avalia combinações emocionais e cognitivas entre:

- TEIQue (regulação, empatia, expressividade, adaptabilidade)
- Big Five (traços estruturais da personalidade)

Objetivo:
Mapear influenciadores emocionais da personalidade e vice-versa.
"""

from typing import Dict, Any


class CrossTeiqueBig5:
    def __init__(self):
        self.version = "2.0-ultra"

    def generate(self, teique: Dict[str, float], big5: Dict[str, float]) -> Dict[str, Any]:
        patterns = {}

        # Emotividade × Neuroticismo
        if teique.get("regulacao", 0) <= 40 and big5.get("neuroticismo", 0) >= 65:
            patterns["vulnerabilidade_afetiva"] = (
                "Baixa regulação emocional intensificada por alto neuroticismo."
            )

        # Empatia × Amabilidade
        if teique.get("empatia", 0) >= 60 and big5.get("amabilidade", 0) >= 60:
            patterns["relacional_forte"] = (
                "Alinhamento emocional e social robusto: empatia + amabilidade."
            )

        # Expressividade × Extroversão
        if teique.get("expressividade", 0) >= 55 and big5.get("extroversao", 0) >= 55:
            patterns["comunicacao_amplificada"] = (
                "Expressividade emocional reforça traços extrovertidos."
            )

        # Abertura × Otimismo
        if big5.get("abertura", 0) >= 65 and teique.get("otimismo", 0) >= 60:
            patterns["visao_expansiva"] = (
                "Combinação de abertura mental e otimismo emocional — alta propensão à inovação."
            )

        return {"module": "cross_teique_big5", "version": self.version, "patterns": patterns}
