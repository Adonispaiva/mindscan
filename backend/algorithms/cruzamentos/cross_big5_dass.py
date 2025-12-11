# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\cruzamentos\cross_big5_dass.py
# Última atualização: 2025-12-11T09:59:20.636480

"""
CROSS Big5 × DASS21 — Versão ULTRA SUPERIOR
-------------------------------------------------------------

Relaciona traços de personalidade (Big Five) com indicadores
psicológicos clínicos (DASS21):

- depressão
- ansiedade
- estresse

Objetivo:
Antecipar padrões combinados de vulnerabilidade emocional
e interpretar riscos a partir do encaixe entre traços e sintomas.
"""

from typing import Dict, Any


class CrossBig5DASS:
    def __init__(self):
        self.version = "2.0-ultra"

    def generate(self, big5: Dict[str, float], dass: Dict[str, float]) -> Dict[str, Any]:
        patterns = {}

        # 1) Neuroticismo → ansiedade e estresse
        if big5.get("neuroticismo", 0) >= 65:
            if dass.get("ansiedade", 0) >= 55:
                patterns["ansiedade_instabilidade"] = (
                    "Neuroticismo elevado combinado com ansiedade acima da média."
                )

            if dass.get("stress", 0) >= 60:
                patterns["stress_reatividade"] = (
                    "Alta reatividade emocional amplificada por níveis elevados de estresse."
                )

        # 2) Baixa extroversão e depressão
        if big5.get("extroversao", 0) <= 30 and dass.get("depressao", 0) >= 50:
            patterns["isolamento_depressivo"] = (
                "Tendência a retraimento emocional combinada com indicadores de depressão."
            )

        # 3) Conscienciosidade baixa + estresse alto
        if big5.get("conscienciosidade", 0) <= 35 and dass.get("stress", 0) >= 60:
            patterns["stress_execucao"] = (
                "Possível colapso de execução devido a baixa estruturação sob alto estresse."
            )

        return {
            "module": "cross_big5_dass",
            "version": self.version,
            "patterns": patterns,
        }
