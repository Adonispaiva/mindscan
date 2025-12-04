#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
async_pipeline.py — AsyncPDFPipeline (MindScan SynMind v2.0)
Autor: Leo Vinci (Inovexa)
----------------------------------------------------------------------------
Função:
    Pipeline ASSÍNCRONA completa do MindScan v2.0.
    Integra:
        - DataPreProcessorEngine (pré-processamento)
        - PDFBuilder (montagem das seções)
        - ReportEngine (HTML final)
        - PDFEngine (renderização PDF)
        - Telemetria Avançada

Este módulo não monta HTML manualmente.
Todo HTML é gerado exclusivamente pelo ReportEngine.
"""

import asyncio
from pathlib import Path
from typing import Dict, Any, Optional, List

from backend.services.pdf.engine.section_engine import DataPreProcessorEngine
from backend.services.pdf.pdf_builder import PDFBuilder
from backend.services.pdf.engine.report_engine import ReportEngine
from backend.services.pdf.engine.pdf_engine import PDFEngine

from backend.services.pdf.telemetry.telemetry_advanced import TelemetryAdvanced
from backend.services.pdf.telemetry.logger import PDFLogger
from backend.services.pdf.telemetry.resource_monitor import ResourceMonitor


class AsyncPDFPipeline:
    """
    Pipeline assíncrona de ponta a ponta (MindScan v2.0).
    """

    def __init__(
        self,
        preprocess_pipelines: Optional[List] = None,
        telemetry: Optional[TelemetryAdvanced] = None,
        logger: Optional[PDFLogger] = None,
        workers: int = 6,
    ):

        self.preprocess_pipelines = preprocess_pipelines or []
        self.telemetry = telemetry or TelemetryAdvanced()
        self.logger = logger or PDFLogger()
        self.workers = workers

        self.pre_processor = DataPreProcessorEngine(
            max_workers=workers,
            logger=self.logger,
            telemetry=self.telemetry
        )

        self.logger.info(
            f"AsyncPDFPipeline v2.0 inicializado (workers={workers}). "
            f"Pré-processadores: {len(self.preprocess_pipelines)}"
        )

    # ----------------------------------------------------------------------
    # Execução assíncrona do pipeline completo
    # ----------------------------------------------------------------------
    async def run_async(
        self,
        payload: Dict[str, Any],
        output_path: Optional[str] = None,
        template: str = "executive",
        renderer: str = "weasy",
    ) -> str:
        """
        Executa:
            1. Pré-processamento (paralelo)
            2. Montagem das seções (PDFBuilder)
            3. Geração do HTML final (ReportEngine)
            4. Render PDF (PDFEngine)
        """

        self.telemetry.iniciar("pipeline_async_total")
        self.logger.evento_pdf_iniciado(payload.get("usuario", {}).get("nome", "Usuário"))

        # 1. Pré-processamento (sync → rodado em executor)
        loop = asyncio.get_event_loop()
        processed_payload = await loop.run_in_executor(
            None,
            self.pre_processor.run,
            payload,
            self.preprocess_pipelines
        )

        # 2. Construção das seções
        builder = PDFBuilder(processed_payload, template=template)
        builder.validate()
        sections = builder.build_sections()

        # 3. HTML final
        engine = ReportEngine(template=template)
        css_text = builder.payload.get("css_text") or ""  # futuro: inject via CSS loader
        html_final = engine.combine(sections, css_text).decode("utf-8")

        # 4. Renderização PDF
        pdf_engine = PDFEngine(renderer=renderer)
        output_path = output_path or "relatorio_mindscan_async.pdf"

        pdf_file = await loop.run_in_executor(
            None,
            pdf_engine.render_pdf,
            html_final,
            css_text,
            output_path
        )

        # Telemetria final
        self.telemetry.registrar_tamanho_pdf(pdf_file)
        self.telemetry.finalizar("pipeline_async_total")
        self.telemetry.exportar()
        self.logger.evento_pdf_finalizado(pdf_file)

        return pdf_file
