"""
Advanced PDF Engine — MindScan

Camada de orquestração para geração de PDFs.
(Implementação gráfica delegada aos renderers.)
"""

from typing import Dict, Any


class PDFEngineAdvanced:
    def generate(self, payload: Dict[str, Any], renderer) -> bytes:
        if not hasattr(renderer, "build"):
            raise ValueError("Renderer inválido")
        return renderer.build(payload)
