# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\cruzamentos\cross_big5_egos.py
# Última atualização: 2025-12-11T09:59:20.636480

"""
CROSS Big5 × EGOS — Versão ULTRA SUPERIOR
-------------------------------------------------------------

Relaciona as dimensões do Big Five com estruturas de ego
(Adulto, Crítico, Cuidador, Adaptado, Livre, etc.).

Objetivo:
Identificar conflitos, alinhamentos e predisposições entre
traços de personalidade e estados de ego dominantes.
"""

from typing import Dict, Any


class CrossBig5Egos:
    def __init__(self):
        self.version = "2.0-ultra"

    def generate(self, big5: Dict[str, float], egos: Dict[str, float]) -> Dict[str, Any]:
        output = {}

        # Ego Crítico elevado + Neuroticismo alto → autocrítica tóxica
        if egos.get("critico", 0) >= 60 and big5.get("neuroticismo", 0) >= 65:
            output["autocritica_toxica"] = (
                "Ego crítico elevado amplificado por neuroticismo alto."
            )

        # Ego Adulto forte + Conscienciosidade alta → maturidade operacional
        if egos.get("adulto", 0) >= 60 and big5.get("conscienciosidade", 0) >= 55:
            output["maturidade_operacional"] = (
                "Alta responsabilidade emocional combinada com estruturação cognitiva."
            )

        # Ego Livre alto + Abertura alta → criatividade não convencional
        if egos.get("livre", 0) >= 60 and big5.get("abertura", 0) >= 70:
            output["criatividade_livre"] = (
                "Expressão criativa intensa, com forte personalidade de inovação divergente."
            )

        return {
            "module": "cross_big5_egos",
            "version": self.version,
            "patterns": output,
        }
