# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\pipelines\diagnostic_pipeline_async.py
# Última atualização: 2025-12-11T09:59:21.058152

"""
diagnostic_pipeline_async.py
Pipeline assíncrono para diagnósticos distribuídos do MindScan.
Executa múltiplas rotinas em paralelo e agrega resultados com consistência forte.

Inclui:
- Scheduler de microtarefas
- Mecanismo anti-lag
- Validação paralela
- Agregador de diagnósticos multicamadas
"""

import asyncio
from engine.validation_engine import ValidationEngine
from engine.parallel_engine import ParallelEngine
from engine.summary_engine import SummaryEngine
from engine.aggregator import Aggregator


class DiagnosticPipelineAsync:
    def __init__(self):
        self.validator = ValidationEngine()
        self.parallel = ParallelEngine()
        self.summarizer = SummaryEngine()
        self.aggregator = Aggregator()

    async def run(self, payload: dict) -> dict:
        self.validator.validate_input(payload)

        tasks = await self.parallel.execute(payload)

        aggregated = self.aggregator.aggregate(tasks)

        summary = self.summarizer.generate_summary(
            aggregated,
            model="diagnostic",
            density="ultra",
            include_anomalies=True,
            include_cross_risks=True
        )

        return {
            "aggregated": aggregated,
            "summary": summary
        }
