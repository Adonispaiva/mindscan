"""
CROSS Strengths — Versão ULTRA SUPERIOR
-------------------------------------------------------------

Integra forças comportamentais (Strengths) com:

- Big Five
- TEIQue
- Performance
- DASS21
- Cultura (OCAI)

Objetivo:
Identificar como forças naturais são amplificadas ou
bloqueadas por traços, emoções, sintomas e ambiente cultural.
"""

from typing import Dict, Any


class CrossStrengths:
    def __init__(self):
        self.version = "2.0-ultra"

    def generate(self, strengths: Dict[str, float], context: Dict[str, Dict[str, float]]) -> Dict[str, Any]:
        patterns = {}

        big5 = context.get("big5", {})
        teique = context.get("teique", {})
        dass = context.get("dass21", {})
        perf = context.get("performance", {})
        ocai = context.get("ocai", {})

        # Liderança × Extroversão × Expressividade
        if strengths.get("lideranca", 0) >= 60:
            if big5.get("extroversao", 0) >= 55 and teique.get("expressividade", 0) >= 55:
                patterns["lideranca_natural"] = (
                    "Força de liderança reforçada por extroversão e expressividade emocional."
                )

        # Criatividade × Abertura × Cultura de inovação
        if strengths.get("criatividade", 0) >= 60:
            if big5.get("abertura", 0) >= 65 and ocai.get("inovacao", 0) >= 60:
                patterns["criatividade_alinhada"] = (
                    "Criatividade forte com abertura alta perfeitamente ajustada à cultura inovadora."
                )

        # Execução × Consciência × Performance
        if strengths.get("execucao", 0) >= 55:
            if big5.get("conscienciosidade", 0) >= 60 and perf.get("consistencia", 0) >= 55:
                patterns["execucao_estrategica"] = (
                    "Execução forte amplificada por estrutura cognitiva e consistência operacional."
                )

        # Forças prejudicadas por DASS
        if strengths.get("autonomia", 0) >= 60 and dass.get("ansiedade", 0) >= 60:
            patterns["autonomia_prejudicada"] = (
                "Ansiedade elevada reduz expressão plena da força de autonomia."
            )

        return {"module": "cross_strengths", "version": self.version, "patterns": patterns}
