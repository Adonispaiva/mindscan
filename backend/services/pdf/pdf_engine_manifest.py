# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\pdf_engine_manifest.py
# Última atualização: 2025-12-11T09:59:21.184463

# pdf_engine_manifest.py — Manifesto Final do PDF Engine MindScan
# Autor: Leo Vinci — Inovexa Software
# ---------------------------------------------------------------
# Documento oficial de declaração do ecossistema de PDF do MindScan.
# Este manifesto é usado para:
# - Auditoria
# - Versionamento
# - Verificação de integridade estrutural
# - Documentação interna
# - Autodescrição do sistema PDF

from .pdf_metadata import (
    PDF_ENGINE_VERSION,
    PDF_ENGINE_NAME,
    PDF_ENGINE_VENDOR,
    PDF_SUPPORTED_FORMATS,
)
from .premium_renderer import PremiumRenderer
from .executive_renderer import ExecutiveRenderer
from .psychodynamic_renderer import PsychodynamicRenderer
from .pdf_service import PDFService
from .pdf_validator import PDFValidator
from .pdf_diagnostics import PDFDiagnostics
from .pdf_registry import PDFRegistry
from .pdf_exceptions import (
    PDFEngineError,
    PDFRenderError,
    PDFPayloadError,
    PDFAssetError,
)


MANIFEST = {
    "engine": {
        "name": PDF_ENGINE_NAME,
        "version": PDF_ENGINE_VERSION,
        "vendor": PDF_ENGINE_VENDOR,
        "supported_modes": PDF_SUPPORTED_FORMATS,
    },
    "modules": {
        "renderers": [
            "PremiumRenderer",
            "ExecutiveRenderer",
            "PsychodynamicRenderer",
        ],
        "core": [
            "PDFService",
            "PDFRegistry",
            "PDFValidator",
            "PDFDiagnostics",
        ],
        "exceptions": [
            "PDFEngineError",
            "PDFRenderError",
            "PDFPayloadError",
            "PDFAssetError",
        ],
    },
    "status": "Operational",
    "description": (
        "Manifesto oficial do MindScan PDF Engine. "
        "Todos os componentes declarados são necessários para a operação "
        "completa dos renderizadores Premium, Executive e Psychodynamic."
    ),
}


def get_manifest():
    """
    Retorna o manifesto completo do PDF Engine.
    """
    return MANIFEST
