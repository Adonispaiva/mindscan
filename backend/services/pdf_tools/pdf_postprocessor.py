# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf_tools\pdf_postprocessor.py
# Última atualização: 2025-12-11T09:59:21.276887

# -*- coding: utf-8 -*-
"""
pdf_postprocessor.py
--------------------

Pós-processador de PDFs do MindScan Corporate.
Aplicado após a geração do PDF.
Funções:
- limpeza de metadados
- inserção de propriedades
- compressão
- validações finais
"""

import os
from typing import Dict
from PyPDF2 import PdfReader, PdfWriter


class PDFPostProcessor:

    @staticmethod
    def apply_metadata(pdf_path: str, metadata: Dict[str, str]) -> str:
        """
        Insere metadados no PDF (autor, título, etc.)
        """
        reader = PdfReader(pdf_path)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        writer.add_metadata({f"/{k}": v for k, v in metadata.items()})

        output_path = pdf_path
        with open(output_path, "wb") as f:
            writer.write(f)

        return output_path

    @staticmethod
    def optimize(pdf_path: str) -> str:
        """
        Operações simples de otimização (placeholder para compressão avançada).
        """
        return pdf_path

    @staticmethod
    def finalize(pdf_path: str, metadata: Dict[str, str]) -> str:
        """
        Executa todo o fluxo de pós-processamento.
        """
        pdf_path = PDFPostProcessor.apply_metadata(pdf_path, metadata)
        pdf_path = PDFPostProcessor.optimize(pdf_path)
        return pdf_path
