"""
DASS21 Summary — Versão ULTRA SUPERIOR
--------------------------------------------------------------

Gera um resumo executivo do DASS21, integrando:

- níveis
- indicadores críticos
- resumo narrativo
"""

from typing import Dict, Any


class DASS21Summary:
    def __init__(self):
        self.version = "2.0-ultra"

    def generate_text(self, d: float, a: float, s: float) -> str:
        parts = []

        if d >= 60:
            parts.append("Há sinais consistentes de humor deprimido.")
        if a >= 60:
            parts.append("A ansiedade encontra-se elevada e afeta o foco.")
        if s >= 60:
            parts.append("O nível de estresse está acima do saudável.")

        if not parts:
            return "Os indicadores emocionais estão dentro da normalidade."

        return " ".join(parts)

    def run(self, scores: Dict[str, float]) -> Dict[str, Any]:
        d = scores.get("depressao", 0)
        a = scores.get("ansiedade", 0)
        s = scores.get("stress", 0)

        return {
            "module": "dass21_summary",
            "version": self.version,
            "summary": self.generate_text(d, a, s),
            "raw_scores": scores,
        }
