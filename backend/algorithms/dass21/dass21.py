"""
DASS21 — Módulo Central
Versão ULTRA SUPERIOR
-------------------------------------------------------------

Processa pontuações do questionário DASS21:

- Depressão
- Ansiedade
- Estresse

Inclui:
- validação de entrada
- normalização
- classificação por níveis
- geração de insights estruturados
"""

from typing import Dict, Any


class DASS21:
    def __init__(self):
        self.version = "2.0-ultra"

    def validate(self, scores: Dict[str, float]) -> None:
        required = ["depressao", "ansiedade", "stress"]
        for key in required:
            if key not in scores:
                raise ValueError(f"Campo ausente: {key}")
            if not isinstance(scores[key], (int, float)):
                raise TypeError(f"Valor inválido para {key}")

    def normalize(self, scores: Dict[str, float]) -> Dict[str, float]:
        return {k: min(max(v, 0), 100) for k, v in scores.items()}

    def classify(self, scores: Dict[str, float]) -> Dict[str, str]:
        levels = {}
        for key, value in scores.items():
            if value < 30:
                levels[key] = "baixo"
            elif value < 60:
                levels[key] = "moderado"
            else:
                levels[key] = "alto"
        return levels

    def run(self, scores: Dict[str, float]) -> Dict[str, Any]:
        self.validate(scores)
        normalized = self.normalize(scores)
        classified = self.classify(normalized)

        return {
            "module": "dass21",
            "version": self.version,
            "normalized": normalized,
            "levels": classified,
        }
