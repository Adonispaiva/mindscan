# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\pdf_validator.py
# Última atualização: 2025-12-11T09:59:21.184463

# pdf_validator.py — Validador de integridade do PDF Engine
# Autor: Leo Vinci — Inovexa Software

from .pdf_metadata import PDF_SUPPORTED_FORMATS


class PDFValidator:
    """
    Validador estrutural do PDF Engine.
    Garante consistência, formato e integridade do pipeline.
    """

    def validate_mode(self, mode: str):
        mode = mode.lower()
        if mode not in PDF_SUPPORTED_FORMATS:
            raise ValueError(
                f"Modo inválido: {mode}. Modos suportados: {PDF_SUPPORTED_FORMATS}"
            )
        return True

    def validate_payload(self, data: dict):
        if not isinstance(data, dict):
            raise TypeError("O payload do relatório deve ser um dicionário.")

        if len(data.keys()) == 0:
            raise ValueError("Payload vazio para geração de PDF.")

        return True
