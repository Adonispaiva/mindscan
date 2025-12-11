# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\esquemas\esquemas.py
# Última atualização: 2025-12-11T09:59:20.667799

"""
Esquemas — Módulo Principal
Executa:
- validação básica
- normalização
- classificação de esquemas
- geração de alertas
- mapa descritivo
- perfil agregado
- formatação final
"""

from typing import Dict, Any

from .esquemas_classifier import EsquemasClassifier
from .esquemas_alerts import EsquemasAlerts
from .esquemas_dimensions import EsquemasDimensions
from .esquemas_norms import EsquemasNorms
from .esquemas_profile_builder import EsquemasProfileBuilder
from .esquemas_summary import EsquemasSummary
from .esquemas_output_formatter import EsquemasOutputFormatter


class Esquemas:
    """
    Pipeline oficial de Esquemas Adaptativos no MindScan.
    """

    def __init__(self):
        self.version = "1.0"

        self.classifier = EsquemasClassifier()
        self.alerts = EsquemasAlerts()
        self.dimensions = EsquemasDimensions()
        self.norms = EsquemasNorms()
        self.profile = EsquemasProfileBuilder()
        self.summary = EsquemasSummary()
        self.formatter = EsquemasOutputFormatter()

    def run(self, raw_scores: Dict[str, float]) -> Dict[str, Any]:
        """
        Fluxo completo:
        1) normalização
        2) classificação dos esquemas
        3) geração de alertas
        4) construção de perfil
        5) resumo técnico
        6) formatação final
        """

        normalized = self.norms.normalize(raw_scores)
        dimensions = self.dimensions.compute(normalized)
        classified = self.classifier.classify(dimensions)
        alerts = self.alerts.detect(classified)
        profile = self.profile.build(classified)
        summary = self.summary.build(classified, alerts, profile)

        return self.formatter.format(
            scores=normalized,
            classified=classified,
            alerts=alerts,
            profile=profile,
            summary=summary,
        )
