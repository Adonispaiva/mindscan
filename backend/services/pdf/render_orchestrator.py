# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\render_orchestrator.py
# Última atualização: 2025-12-11T09:59:21.200087

# render_orchestrator.py — Orquestração de Renderers MindScan
# Autor: Leo Vinci — Inovexa Software

from .pdf_service import PDFService


class RenderOrchestrator:
    """
    Orquestrador central do ecossistema PDF MindScan.
    Permite selecionar o tipo de relatório e aciona o renderer apropriado.
    """

    def __init__(self, assets_path: str):
        self.service = PDFService(assets_path)

    def generate(self, mode: str, output_path: str, data: dict):
        mode = mode.lower()

        if mode == "premium":
            return self.service.generate_premium(output_path, data)

        if mode == "executive":
            return self.service.generate_executive(output_path, data)

        if mode == "psychodynamic":
            return self.service.generate_psychdynamic(output_path, data)

        raise ValueError(f"Modo de relatório inválido: {mode}")
