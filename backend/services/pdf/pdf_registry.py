# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\pdf_registry.py
# Última atualização: 2025-12-11T09:59:21.184463

# pdf_registry.py — Registro sob demanda do PDF Engine
# Autor: Leo Vinci — Inovexa Software

from .pdf_service import PDFService


class PDFRegistry:
    """
    Registro sob demanda do PDF Engine.
    Só inicializa o PDFService no momento da solicitação.
    """

    def __init__(self, assets_path: str):
        self.assets_path = assets_path
        self._service = None

    def get_service(self) -> PDFService:
        """
        Inicializa o PDFService apenas quando necessário.
        """
        if self._service is None:
            self._service = PDFService(self.assets_path)
        return self._service
