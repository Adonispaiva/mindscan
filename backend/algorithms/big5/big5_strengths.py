# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\big5\big5_strengths.py
# Última atualização: 2025-12-11T09:59:20.608841

"""
Big5 Strengths — Versão Ultra Superior
--------------------------------------

Identifica forças dominantes baseadas nas dimensões Big Five.
Inclui mapeamento, ranking, e descrição operacional.
"""

from typing import Dict


class Big5Strengths:
    def __init__(self):
        self.version = "2.0-ultra"

        self.map = {
            "abertura": "Criatividade, inovação, visão estratégica.",
            "conscienciosidade": "Disciplina, confiabilidade e execução superior.",
            "extroversao": "Comunicação, influência e energia social.",
            "amabilidade": "Negociação, empatia e colaboração.",
            "neuroticismo": "Percepção emocional refinada e sensibilidade contextual.",
        }

    def extract(self, dims: Dict[str, float]) -> Dict[str, str]:
        strengths = {}

        for dim, value in dims.items():
            if value >= 60:
                strengths[dim] = self.map.get(dim, "")

        return strengths
