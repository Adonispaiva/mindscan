# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf_engine.py
# Última atualização: 2025-12-11T09:59:21.105108

# -*- coding: utf-8 -*-
"""
pdf_engine.py
-------------

Motor central de conversão HTML → PDF usando WeasyPrint.
Usado pelos renderers corporativos e premium.
"""

from weasyprint import HTML
from typing import Optional


class PDFEngine:

    @staticmethod
    def html_to_pdf(html_string: str, output_path: str) -> str:
        """
        Recebe HTML como string e salva PDF no caminho especificado.
        """
        try:
            HTML(string=html_string).write_pdf(output_path)
            return output_path
        except Exception as e:
            raise RuntimeError(f"Erro ao converter HTML em PDF: {e}")

    @staticmethod
    def html_file_to_pdf(html_path: str, output_path: str) -> str:
        """
        Recebe caminho de arquivo HTML e salva PDF no caminho especificado.
        """
        try:
            HTML(filename=html_path).write_pdf(output_path)
            return output_path
        except Exception as e:
            raise RuntimeError(f"Erro ao converter arquivo HTML em PDF: {e}")

