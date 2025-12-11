# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\esquemas\schema_profile_builder.py
# Última atualização: 2025-12-11T09:59:20.683445

"""
Schema Profile Builder
Constrói um perfil psicodinâmico intermediário com base nas dimensões
(item-level) antes do agrupamento em fatores e esquemas.
"""

from typing import Dict, Any

from .schema_dimensions import SchemaDimensions
from .schema_alerts import SchemaAlerts


class SchemaProfileBuilder:
    """
    Estrutura baseada no processamento item→dimensão,
    usada como camada adicional de análise no pipeline MindScan.
    """

    def __init__(self):
        self.version = "1.0"

        self.dim_engine = SchemaDimensions()
        self.alerts_engine = SchemaAlerts()

    def build(self, normalized: Dict[str, float]) -> Dict[str, Any]:
        dims = self.dim_engine.compute(normalized)
        alerts = self.alerts_engine.detect(normalized)

        predominant = sorted(
            dims.items(),
            key=lambda x: x[1],
            reverse=True
        )[:2]

        return {
            "module": "Esquemas",
            "version": self.version,
            "dimensions": dims,
            "alerts": alerts,
            "predominant_dimensions": [p[0] for p in predominant],
        }
