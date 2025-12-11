# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\mindgen\charts\composite_behavioral_chart.py
# Última atualização: 2025-12-11T09:59:27.699099

class CompositeBehavioralChart:
    """
    Combina múltiplos gráficos (radar + linha + heatmap) em um layout único.
    """

    @staticmethod
    def assemble(blocks: dict):
        return {
            "type": "composite",
            "blocks": list(blocks.keys())
        }
