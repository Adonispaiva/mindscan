# pdf_service.py — Serviço central do MindScan PDF Engine
# Autor: Leo Vinci — Inovexa Software

from __future__ import annotations

from .premium_renderer import PremiumRenderer
from .executive_renderer import ExecutiveRenderer
from .psychodynamic_renderer import PsychodynamicRenderer


class PDFService:
    """
    Camada de serviço que expõe uma interface unificada
    para gerar qualquer tipo de relatório MindScan.
    """

    def __init__(self, assets_path: str):
        self.assets_path = assets_path

    def generate_premium(self, output_path: str, data: dict):
        renderer = PremiumRenderer(output_path, self.assets_path)
        return renderer.render(data)

    def generate_executive(self, output_path: str, data: dict):
        renderer = ExecutiveRenderer(output_path, self.assets_path)
        return renderer.render(data)

    def generate_psychodynamic(self, output_path: str, data: dict):
        renderer = PsychodynamicRenderer(output_path)
        return renderer.render(data)
