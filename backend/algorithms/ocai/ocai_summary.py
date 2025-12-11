# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\ocai\ocai_summary.py
# Última atualização: 2025-12-11T09:59:20.698978

"""
OCAI Summary
Resumo executivo da cultura predominante, com interpretação curta.
"""

from typing import Dict


class OCAISummary:
    def __init__(self):
        self.version = "1.0"
        self.labels = {
            "clã": "Forte orientação colaborativa, pessoas em primeiro lugar.",
            "adhocracia": "Inovação, flexibilidade, foco em ideias.",
            "mercado": "Resultados, competição e agressividade estratégica.",
            "hierarquia": "Controle, previsibilidade e estabilidade.",
        }

    def summarize(self, dims: Dict[str, float]) -> Dict[str, str]:
        if not dims:
            return {"summary": "Nenhuma dimensão disponível."}

        # Identifica cultura predominante
        top = max(dims, key=dims.get)

        return {
            "top_culture": top,
            "message": self.labels.get(top, "Cultura predominante detectada."),
            "version": self.version,
        }
