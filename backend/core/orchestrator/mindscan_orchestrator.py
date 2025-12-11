# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\core\orchestrator\mindscan_orchestrator.py
# Última atualização: 2025-12-11T09:59:20.792728

from backend.core.diagnostic.diagnostic_engine_v3 import DiagnosticEngineV3
from backend.core.interpretation.interpretation_pipeline import InterpretationPipeline
from backend.core.normalization.global_normalization import GlobalNormalization
from backend.core.compliance.compliance_engine import ComplianceEngine
from backend.services.report.assembler.report_assembler import ReportAssembler
from backend.api.compat.external_api_compat_layer import ExternalAPICompatLayer
from backend.integrations.events.event_dispatcher import EventDispatcher
from backend.integrations.events.integration_event_handlers import (
    IntegrationEventHandlers
)

class MindScanOrchestrator:
    """
    ORQUESTRADOR FINAL DO MINDSCAN ENTERPRISE v3.0
    Responsável por coordenar:
    - Execução científica
    - Interpretação avançada (MI)
    - Normalização final
    - Compliance
    - Geração de relatórios
    - Eventos internos / webhooks externos
    - Camada de compatibilidade externa
    """

    def __init__(self):
        # Registra handlers de eventos
        EventDispatcher.subscribe("diagnostic_completed",
                                  IntegrationEventHandlers.on_diagnostic_completed)
        EventDispatcher.subscribe("report_generated",
                                  IntegrationEventHandlers.on_report_generated)

    def run(self, test_id: str, raw_instruments: dict, report_type: str = "executive",
            context: dict = None, webhook_url: str = None) -> dict:
        """
        Execução total do MindScan:
        1. Diagnóstico científico completo
        2. Interpretação MI
        3. Normalização global
        4. Compliance
        5. Montagem de relatório
        6. Eventos internos
        7. Retorno para API externa
        """

        # 1 — Execução científica
        results = DiagnosticEngineV3.run(raw_instruments)

        # 2 — Interpretação narrativa
        interpreted = InterpretationPipeline.run(results)

        # 3 — Normalização final
        normalized = GlobalNormalization.apply(results)

        # 4 — Compliance
        sanitized = ComplianceEngine.sanitize(normalized)

        # Stream final de dados internos
        internal_payload = {
            "test_id": test_id,
            "results": sanitized,
            "interpreted": interpreted
        }

        # 5 — Geração de relatório e PDF
        report_info = ReportAssembler.assemble(report_type, test_id, {
            **sanitized,
            **interpreted
        })

        # 6 — Eventos internos
        EventDispatcher.emit("diagnostic_completed", {
            "test_id": test_id,
            "results": sanitized,
            "webhook_url": webhook_url
        })

        EventDispatcher.emit("report_generated", {
            "test_id": test_id,
            "report_path": report_info.get("file_path"),
            "webhook_url": webhook_url
        })

        # 7 — API externa (compat)
        external_payload = ExternalAPICompatLayer.convert({
            **sanitized,
            **interpreted
        })

        return {
            "status": "success",
            "test_id": test_id,
            "report": report_info,
            "external_payload": external_payload,
            "internal_payload": internal_payload
        }
