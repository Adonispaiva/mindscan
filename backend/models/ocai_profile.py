# ocai_profile.py
# MindScan Rebuild – Modelo do Perfil OCAI
# Versão Definitiva • Estrutura Avançada Pydantic-Style
# Autor: Leo Vinci — IA Supervisora Inovexa
# -------------------------------------------------------------------------
# Este arquivo padroniza o modelo de saída do módulo OCAI, garantindo:
#   - estrutura tipada e validada
#   - compatibilidade com mindscan_result.py
#   - uso direto pelo Diagnostic Engine e Reporting
#   - representação final da cultura organizacional
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
class OCAIProfile:
    """
    Estrutura definitiva do Perfil Cultural OCAI.
    """

    profiles: Dict[str, float]                 # Clan, Adhocracia, Mercado, Hierarquia (0–100)
    dominant_profile: Dict[str, Any]          # Perfil dominante estruturado
    generated_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())

    def __post_init__(self):
        require(isinstance(self.profiles, dict) and len(self.profiles) == 4,
                "profiles deve conter exatamente 4 perfis: C, A, M, H.")

        for key, val in self.profiles.items():
            require(key in ["C", "A", "M", "H"],
                    f"Perfil inválido no OCAI: {key}")
            require(isinstance(val, (int, float)),
                    f"Valor inválido no perfil {key}.")
            require(0 <= val <= 100,
                    f"Valor fora do intervalo 0–100 no perfil {key}.")

        require(isinstance(self.dominant_profile, dict) and len(self.dominant_profile) > 0,
                "dominant_profile deve ser um dicionário válido.")

        require("code" in self.dominant_profile and "name" in self.dominant_profile,
                "dominant_profile precisa conter 'code' e 'name'.")

        require(isinstance(self.generated_at, str) and len(self.generated_at) > 0,
                "generated_at inválido.")

    # ------------------------------------------------------------------
    # Conversões finais
    # ------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        return {
            "profiles": self.profiles,
            "dominant_profile": self.dominant_profile,
            "generated_at": self.generated_at
        }

    def summary(self) -> Dict[str, Any]:
        return {
            "dominant": self.dominant_profile.get("name"),
            "score": self.dominant_profile.get("score"),
            "profiles": self.profiles
        }
