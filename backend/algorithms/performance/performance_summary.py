"""
Performance Summary
Resumo executivo da performance profissional.
"""

from typing import Dict, Any


class PerformanceSummary:
    def __init__(self):
        self.version = "1.0"

    def summarize(self, dims: Dict[str, float]) -> Dict[str, Any]:
        if not dims:
            return {"summary": "Nenhuma dimensão disponível."}

        top = max(dims, key=dims.get)

        return {
            "version": self.version,
            "top_dimension": top,
            "message": f"Maior força atual identificada em: {top}.",
            "raw": dims,
        }
