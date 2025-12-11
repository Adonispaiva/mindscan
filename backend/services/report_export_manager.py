# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\report_export_manager.py
# Última atualização: 2025-12-11T09:59:21.105108

# -*- coding: utf-8 -*-
"""
report_export_manager.py
------------------------

Gerencia a exportação final de relatórios:
- coordena HTML + PDF
- aplica sanitização de HTML
- aplica pós-processamento do PDF
- retorna caminhos finais

Função central para padronizar a saída de todos os renderers.
"""

from typing import Dict, Any

from services.helpers.html_sanitizer import HTMLSanitizer
from services.pdf_tools.pdf_postprocessor import PDFPostProcessor


class ReportExportManager:

    @staticmethod
    def export(renderer, metadata: Dict[str, str]) -> Dict[str, str]:
        """
        Execução final.
        renderer: instância de qualquer renderer (corporate, executive, premium, etc)
        """
        # Gera HTML
        html_path = renderer.build_html()

        # Sanitiza HTML
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()

        sanitized = HTMLSanitizer.sanitize(html)

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(sanitized)

        # Gera PDF
        pdf_path = renderer.build_pdf()

        # Pós-processa PDF
        final_pdf = PDFPostProcessor.finalize(pdf_path, metadata)

        return {"html": html_path, "pdf": final_pdf}
