# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\bussola_profile.py
# Última atualização: 2025-12-11T09:59:20.948776

# bussola_profile.py
# MindScan Rebuild – Modelo da Bússola de Competências
# Versão Definitiva • Estrutura Avançada Pydantic-Style
# Autor: Leo Vinci — IA Supervisora Inovexa
# -------------------------------------------------------------------------
# Estrutura oficial para representar o resultado da Bússola de Competências
# com validação forte, tipagem estática e compatibilidade total com:
#   - bussola.py
#   - Diagnostic Engine
#   - Runtime Kernel
#   - mindscan_result.py
# -------------------------------------------------------------------------

from dataclasses import dataclass, field
from typing import Dict, Any
import datetime


class ValidationError(Exception):
    pass


def require(condition: bool, message: str):
    if not condition:
        raise ValidationError(message)


@dataclass
class BussolaProfile:
    """
    Estrutura oficial do perfil de Competências (Bússola MindScan).
    Dimensões esperadas:
        E, X, R, C, L, A, P
    """

    results: Dict[str, float]                 # valores normalizados (0–100)
    metadata: Dict[str, Any]                  # descrições, ranges, significado
    generated_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())

    EXPECTED_KEYS = ["E", "X", "R", "C", "L", "A", "P"]

    def __post_init__(self):
        require(isinstance(self.results, dict) and len(self.results) == 7,
                "results deve conter exatamente 7 dimensões da Bússola.")

        for key in self.EXPECTED_KEYS:
            require(key in self.results,
                    f"Dimensão ausente na Bússola: {key}")
            value = self.results[key]
            require(isinstance(value, (int, float)),
                    f"Valor de {key} deve ser numérico.")
            require(0 <= value <= 100,
                    f"Valor de {key} fora do intervalo 0–100.")

        require(isinstance(self.metadata, dict),
                "metadata deve ser um dicionário.")
        require(isinstance(self.generated_at, str) and len(self.generated_at) > 0,
                "generated_at inválido.")

    # ---------------------------------------------------------
    # Conversões finais
    # ---------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        return {
            "results": self.results,
            "metadata": self.metadata,
            "generated_at": self.generated_at
        }

    def summary(self) -> Dict[str, Any]:
        return {
            "top": max(self.results, key=self.results.get),
            "top_score": max(self.results.values()),
            "dimensions": list(self.results.keys())
        }
