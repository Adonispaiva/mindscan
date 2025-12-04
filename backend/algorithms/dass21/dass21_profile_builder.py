"""
DASS21 Profile Builder — Versão ULTRA SUPERIOR
--------------------------------------------------------------

Constrói um perfil psicológico completo a partir das três
dimensões do DASS21, organizando:

- níveis individuais
- combinação emocional geral
- indicadores complementares
- perfil psicológico sintético
"""

from typing import Dict, Any


class DASS21ProfileBuilder:
    def __init__(self):
        self.version = "2.0-ultra"

    def classify(self, value: float) -> str:
        if value < 30:
            return "baixo"
        if value < 60:
            return "moderado"
        return "alto"

    def composite(self, dep: float, ans: float, st: float) -> str:
        if dep >= 65 and ans >= 55:
            return "depressivo-ansioso"
        if st >= 70:
            return "sobrecarga emocional"
        if dep < 30 and ans < 30 and st < 30:
            return "estável"
        return "misto"

    def run(self, scores: Dict[str, float]) -> Dict[str, Any]:
        d = scores.get("depressao", 0)
        a = scores.get("ansiedade", 0)
        s = scores.get("stress", 0)

        return {
            "module": "dass21_profile_builder",
            "version": self.version,
            "levels": {
                "depressao": self.classify(d),
                "ansiedade": self.classify(a),
                "stress": self.classify(s),
            },
            "profile": self.composite(d, a, s),
        }
