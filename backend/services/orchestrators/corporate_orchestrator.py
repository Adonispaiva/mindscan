# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\orchestrators\corporate_orchestrator.py
# Última atualização: 2025-12-11T09:59:21.167629

# -*- coding: utf-8 -*-
"""
corporate_orchestrator.py
-------------------------

Orquestra todos os engines corporativos, gerando o payload final
que alimenta o Corporate Renderer.
"""

from typing import Dict, Any, List

from services.engines.corporate_summary_builder import CorporateSummaryBuilder
from services.engines.corporate_competency_engine import CorporateCompetencyEngine
from services.engines.corporate_behavior_engine import CorporateBehaviorEngine
from services.engines.corporate_risk_engine import CorporateRiskEngine
from services.engines.corporate_growth_engine import CorporateGrowthEngine
from services.engines.corporate_culture_engine import CorporateCultureEngine

from services.helpers.data_sanitizer import DataSanitizer


class CorporateOrchestrator:

    def __init__(self, payload: Dict[str, Any]):
        self.payload = DataSanitizer.sanitize(payload)

    def build_summary(self) -> Dict[str, Any]:
        builder = CorporateSummaryBuilder(self.payload)
        return builder.build()

    def build_sections(self) -> List[Dict[str, Any]]:
        return [
            CorporateCompetencyEngine(self.payload).build(),
            CorporateBehaviorEngine(self.payload).build(),
            CorporateRiskEngine(self.payload).build(),
            CorporateGrowthEngine(self.payload).build(),
            CorporateCultureEngine(self.payload).build(),
        ]

    def build(self) -> Dict[str, Any]:
        """
        Retorna o payload completo preparado para o CorporateRenderer.
        """
        return {
            "test_id": self.payload.get("test_id", ""),
            "context": self.payload.get("context", {}),
            "summary": self.build_summary(),
            "sections": self.build_sections(),
        }
