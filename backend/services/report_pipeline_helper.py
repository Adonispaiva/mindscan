# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\report_pipeline_helper.py
# Última atualização: 2025-12-11T09:59:21.105108

# -*- coding: utf-8 -*-
"""
report_pipeline_helper.py
-------------------------

Auxiliar de pipeline — coordena a montagem final
do relatório corporativo antes da renderização.
"""

from typing import Dict, Any

from services.orchestrators.corporate_orchestrator import CorporateOrchestrator
from services.helpers.payload_integrator import PayloadIntegrator


class ReportPipelineHelper:

    @staticmethod
    def prepare_for_corporate_renderer(payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fluxo:
        1. Orquestra engines
        2. Integra payload original + payload estruturado
        3. Retorna resultado final para o CorporateRenderer
        """
        orchestrated = CorporateOrchestrator(payload).build()
        merged = PayloadIntegrator.merge(payload, orchestrated)
        return merged
