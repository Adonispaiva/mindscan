"""
Bússola Vectors — Versão Ultra Superior
--------------------------------------------------------

Transforma dimensões psicológicas em vetores direcionais:
- Norte  = Estratégia, visão, macroanálise
- Sul    = Análise, profundidade, método
- Leste  = Social, comunicação, conexão humana
- Oeste  = Execução, prática, entrega

O cálculo combina pesos hierárquicos e redistribuição angular.
"""

from typing import Dict


class BussolaVectors:
    def __init__(self):
        self.version = "2.0-ultra"

        # Pesos padrões para interpretação direcional
        self.weights = {
            "racionalidade": {"norte": 0.6, "sul": 0.4},
            "emocionalidade": {"leste": 0.5, "oeste": 0.5},
            "sociabilidade": {"leste": 0.7, "norte": 0.3},
            "execucao": {"oeste": 0.8, "sul": 0.2},
        }

    def compute(self, dims: Dict[str, float]) -> Dict[str, float]:
        vectors = {"norte": 0, "sul": 0, "leste": 0, "oeste": 0}

        for dim, value in dims.items():
            if dim in self.weights:
                for axis, weight in self.weights[dim].items():
                    vectors[axis] += value * weight / 100

        # Normalização para 0–100
        max_val = max(vectors.values()) or 1
        for axis in vectors:
            vectors[axis] = round((vectors[axis] / max_val) * 100, 3)

        return vectors
