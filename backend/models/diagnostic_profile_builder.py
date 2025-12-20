import logging
from typing import Dict, Any, Optional
# IMPORTAÇÃO CORRIGIDA: Saindo do modo absoluto para o relativo
from .diagnostic_matrix import DiagnosticMatrix
from ..services.algorithms.dass21 import DASS21Analyzer

logger = logging.getLogger(__name__)

class DiagnosticProfileBuilder:
    def __init__(self, raw_data: Dict[str, Any]):
        self.raw_data = raw_data
        self.profile = {}

    def build(self) -> Dict[str, Any]:
        logger.info("Iniciando construção do perfil de diagnóstico...")
        # Lógica de construção...
        return self.profile