"""
Big5 Profile Builder — Versão Ultra Superior
--------------------------------------------

Constrói o PERFIL FINAL Big Five, unificando:
- dimensões
- forças
- riscos
- necessidades emocionais
- insights
- crosslinks
- padrões enriquecidos
- predição

É o “núcleo de integração” usado pelo relatório Master.
"""

from typing import Dict, Any


class Big5ProfileBuilder:
    def __init__(self):
        self.version = "2.0-ultra"

    def build(
        self,
        dims: Dict[str, float],
        strengths: Dict[str, str],
        risks: Dict[str, str],
        needs: Dict[str, str],
        insights: Dict[str, str],
        crosslinks: Dict[str, Any],
        enrichment: Dict[str, Any],
        prediction: Dict[str, Any],
    ) -> Dict[str, Any]:

        top = max(dims, key=dims.get) if dims else None

        return {
            "module": "Big5",
            "version": self.version,
            "top_dimension": top,
            "dimensions": dims,
            "insights": insights,
            "strengths": strengths,
            "risks": risks,
            "needs": needs,
            "crosslinks": crosslinks,
            "enrichment": enrichment,
            "prediction": prediction,
        }
