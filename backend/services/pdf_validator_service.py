# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf_validator_service.py
# Última atualização: 2025-12-11T09:59:21.105108

# -*- coding: utf-8 -*-
"""
pdf_validator_service.py
------------------------

Valida PDFs gerados pelo MindScan antes de exportação.
Verifica:
- existência do arquivo
- páginas válidas
- tamanho mínimo
- estrutura básica

Evita que relatórios corrompidos cheguem ao usuário final.
"""

import os
from typing import Dict, Any
from PyPDF2 import PdfReader


class PDFValidatorService:

    MIN_SIZE_BYTES = 10_000  # mínimo aproximado para um PDF real

    @staticmethod
    def validate(pdf_path: str) -> Dict[str, Any]:
        errors = []

        if not os.path.exists(pdf_path):
            errors.append("Arquivo PDF não foi encontrado.")

        if os.path.exists(pdf_path) and os.path.getsize(pdf_path) < PDFValidatorService.MIN_SIZE_BYTES:
            errors.append("O PDF gerado está abaixo do tamanho mínimo esperado.")

        try:
            reader = PdfReader(pdf_path)
            if len(reader.pages) == 0:
                errors.append("PDF inválido: nenhuma página encontrada.")
        except Exception:
            errors.append("PDF inválido ou corrompido.")

        return {
            "valido": len(errors) == 0,
            "erros": errors
        }
