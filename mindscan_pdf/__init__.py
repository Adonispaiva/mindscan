#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mindscan_pdf — Pacote oficial instalável do MindScan PDF Engine
---------------------------------------------------------------

Este módulo expõe a API pública do motor de PDFs do MindScan,
permitindo que outros sistemas importem o pacote:

    from mindscan_pdf import PDFBuilder, WeasyRenderer

Também registra os metadados básicos para ferramentas de distribuição.
"""

from pathlib import Path

# Exposição pública da API
from pdf_builder import PDFBuilder
from backend.services.pdf.renderers.weasy_renderer import WeasyRenderer
from backend.services.pdf.renderers.reportlab_renderer import ReportLabRenderer
from backend.services.pdf.renderers.matplotlib_ready import GraphGenerator

__all__ = [
    "PDFBuilder",
    "WeasyRenderer",
    "ReportLabRenderer",
    "GraphGenerator",
]

# Metadados
__version__ = "1.0.0"
__author__ = "Inovexa Software"
__description__ = "MindScan PDF Engine — Relatórios psicoprofissionais Premium"
__package_root__ = Path(__file__).resolve().parent
