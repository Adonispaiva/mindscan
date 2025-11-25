# schema_profile.py
# MindScan Rebuild – Modelo de Esquemas (Young Schema Model)
# Versão Definitiva • Estrutura Avançada Pydantic-Style
# Autor: Leo Vinci — IA Supervisora Inovexa
# -------------------------------------------------------------------------
# Estrutura final da representação dos 18 esquemas do modelo Young, com:
#   - 18 esquemas
#   - 5 domínios
#   - Metadados
#   - Normalização (0–100)
#   - Tipagem forte
#   - Validação rígida
#   - Compatibilidade plena com o Diagnostic Engine
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
class SchemaProfile:
    """
    Estrutura oficial dos Esquemas Iniciais Desadaptativos (Young).
    """

    results: Dict[str, float]          # { "AB": 72.5, "DA": 51.0, ... }
    domains: Dict[str, float]          # médias agregadas por domínio
    metadata: Dict[str, Any]           # descrições, ranges, explicações
    generated_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())

    EXPECTED_SCHEMAS = [
        "AB", "DA", "PE", "DV", "IS",
        "DI", "VU", "EM", "FR",
        "GR", "AI",
        "SU", "AS", "BA",
        "NP", "IE", "PI", "PU"
    ]

    def __post_init__(self):

        # ---------------------------------------------------------
        # Validar resultados individuais (18 esquemas)
        # ---------------------------------------------------------
        require(isinstance(self.results, dict), "results deve ser um dicionário.")

        for code in self.EXPECTED_SCHEMAS:
            require(code in self.results,
                    f"Esquema ausente no conjunto de resultados: {code}")

            value = self.results[code]
            require(isinstance(value, (int, float)),
                    f"Valor de {code} deve ser numérico.")
            require(0 <= value <= 100,
                    f"Valor de {code} fora do intervalo 0–100.")

        # ---------------------------------------------------------
        # Validar domínios
        # ---------------------------------------------------------
        require(isinstance(self.domains, dict), "domains deve ser um dicionário.")
        require(len(self.domains) == 5,
                "domains deve conter exatamente 5 domínios.")

        for key, val in self.domains.items():
            require(isinstance(val, (int, float)),
                    f"Domínio '{key}' deve ser numérico.")
            require(0 <= val <= 100,
                    f"Valor fora do intervalo 0–100 no domínio '{key}'.")

        # ---------------------------------------------------------
        # Metadados
        # ---------------------------------------------------------
        require(isinstance(self.metadata, dict),
                "metadata deve ser um dicionário.")
        require("descriptions" in self.metadata,
                "metadata precisa conter bloco 'descriptions'.")

        # ---------------------------------------------------------
        # Timestamp
        # ---------------------------------------------------------
        require(isinstance(self.generated_at, str) and len(self.generated_at) > 0,
                "generated_at inválido.")

    # ---------------------------------------------------------
    # Conversões
    # ---------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        return {
            "results": self.results,
            "domains": self.domains,
            "metadata": self.metadata,
            "generated_at": self.generated_at
        }

    def summary(self) -> Dict[str, Any]:
        # Retorna os 3 esquemas mais altos — visão crítica
        top3 = sorted(self.results.items(), key=lambda x: x[1], reverse=True)[:3]
        return {
            "top3": top3,
            "domains": self.domains
        }
