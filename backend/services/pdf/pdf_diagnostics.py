# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\pdf_diagnostics.py
# Última atualização: 2025-12-11T09:59:21.184463

# pdf_diagnostics.py — Diagnóstico interno do PDF Engine
# Autor: Leo Vinci — Inovexa Software

from .pdf_metadata import PDF_ENGINE_VERSION, PDF_SUPPORTED_FORMATS
from .pdf_validator import PDFValidator


class PDFDiagnostics:
    """
    Executa verificações internas do PDF Engine:
    - valida modo
    - valida payload
    - retorna estado operacional
    """

    def __init__(self):
        self.validator = PDFValidator()

    def engine_status(self):
        return {
            "version": PDF_ENGINE_VERSION,
            "supported_modes": PDF_SUPPORTED_FORMATS,
            "operational": True
        }

    def validate(self, mode: str, payload: dict):
        self.validator.validate_mode(mode)
        self.validator.validate_payload(payload)

        return {"status": "OK", "mode": mode}
