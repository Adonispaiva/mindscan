# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\performance\performance_dimensions.py
# Última atualização: 2025-12-11T09:59:20.698978

"""
Performance Dimensions
Processa os valores normalizados e calcula as dimensões principais:
- Produtividade
- Execução
- Autonomia
- Consistência Operacional
- Prioridade & Foco
"""

from typing import Dict


class PerformanceDimensions:
    def __init__(self):
        self.version = "1.0"

        # Mapeamento genérico item → dimensão
        self.mapping = {
            "produtividade": ["prod_1", "prod_2", "prod_3"],
            "execucao": ["exec_1", "exec_2", "exec_3"],
            "autonomia": ["auto_1", "auto_2", "auto_3"],
            "consistencia": ["cons_1", "cons_2", "cons_3"],
            "foco": ["foco_1", "foco_2", "foco_3"],
        }

    def compute(self, normalized: Dict[str, float]) -> Dict[str, float]:
        dims = {}

        for dim, items in self.mapping.items():
            values = [normalized.get(i, 0) for i in items]
            dims[dim] = sum(values) / len(values) if values else 0.0

        return dims
