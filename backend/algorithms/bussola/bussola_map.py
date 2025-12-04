"""
Bússola Map — Versão Ultra Superior
--------------------------------------------------------

Gera o mapa direcional completo, combinando:
- vetores principais
- quadrantes
- dominância dual
- estilo predominante
"""

from typing import Dict, Any


class BussolaMap:
    def __init__(self):
        self.version = "2.0-ultra"

    def build(self, vectors: Dict[str, float]) -> Dict[str, Any]:
        if not vectors:
            return {"map": "indefinido"}

        dominant = max(vectors, key=vectors.get)
        secondary = sorted(vectors, key=vectors.get, reverse=True)[1]

        return {
            "module": "Bussola",
            "version": self.version,
            "dominant": dominant,
            "secondary": secondary,
            "quadrant": f"{dominant}-{secondary}",
            "vectors": vectors,
        }
