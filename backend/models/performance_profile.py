# performance_profile.py
# MindScan Rebuild – Modelo de Performance
# Versão Definitiva • Estrutura Avançada Pydantic-Style
# Autor: Leo Vinci — IA Supervisora Inovexa
# -------------------------------------------------------------------------
# Este arquivo padroniza a estrutura de saída do algoritmo de Performance
# do MindScan, garantindo:
#   - tipagem forte
#   - validação completa
#   - integração com mindscan_result.py
#   - compatibilidade absoluta com o Diagnostic Engine
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
class PerformanceProfile:
    """
    Estrutura oficial de resultados de Performance MindScan.
    """

    results: Dict[str, float]                 # scores normalizados (0–100)
    overall: float                            # score final geral
    metadata: Dict[str, Any]                  # descrições, ranges, fatores etc.
    generated_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())

    def __post_init__(self):
        require(isinstance(self.results, dict) and len(self.results) > 0,
                "results deve ser um dicionário com valores numéricos.")

        for key, val in self.results.items():
            require(isinstance(val, (int, float)),
                    f"Valor de '{key}' inválido: deve ser numérico.")
            require(0 <= val <= 100,
                    f"Valor fora do intervalo permitido (0–100): {key}={val}")

        require(isinstance(self.overall, (int, float)),
                "overall deve ser numérico.")
        require(0 <= self.overall <= 100,
                "overall fora do intervalo permitido 0–100.")

        require(isinstance(self.metadata, dict),
                "metadata deve ser um dicionário válido.")

        require(isinstance(self.generated_at, str) and len(self.generated_at) > 0,
                "generated_at inválido.")

    # ------------------------------------------------------------------
    # Conversões finais
    # ------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        return {
            "results": self.results,
            "overall": self.overall,
            "metadata": self.metadata,
            "generated_at": self.generated_at
        }

    def summary(self) -> Dict[str, Any]:
        return {
            "overall": self.overall,
            "dimensions": list(self.results.keys()),
        }
