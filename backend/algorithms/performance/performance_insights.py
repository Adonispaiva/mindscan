# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\performance\performance_insights.py
# Última atualização: 2025-12-11T09:59:20.714601

"""
Performance Insights
Gera insights interpretativos com base nas dimensões de performance.
"""

from typing import Dict


class PerformanceInsights:
    def __init__(self):
        self.version = "1.0"

        self.templates = {
            "produtividade": "Capacidade de entregar volume consistente de trabalho.",
            "execucao": "Nível de eficiência na conclusão de tarefas.",
            "autonomia": "Habilidade de operar com independência e responsabilidade.",
            "consistencia": "Estabilidade e previsibilidade na execução.",
            "foco": "Prioridade adequada e direcionamento mental.",
        }

    def generate(self, dims: Dict[str, float]) -> Dict[str, str]:
        insights = {}

        for dim, value in dims.items():
            base = self.templates.get(dim, "Padrão observável na dimensão.")
            if value >= 70:
                insights[dim] = f"{base} — performance elevada e consistente."
            elif value >= 40:
                insights[dim] = f"{base} — nível moderado, com espaço para expansão."
            else:
                insights[dim] = f"{base} — ponto de atenção para desenvolvimento."

        return insights
