# ocai.py
# MindScan Rebuild – Algoritmo OCAI (Organizational Culture Assessment Instrument)
# Versão Final e Definitiva — Inovexa / MindScan
# Autor: Leo Vinci – IA Supervisora Inovexa
# Última atualização: 23/11/2025
# -------------------------------------------------------------------------
# OCAI avalia 6 dimensões culturais, cada uma distribuída entre 4 perfis:
#   - Clan (C)
#   - Adhocracia (A)
#   - Mercado (M)
#   - Hierarquia (H)
#
# O respondente distribui 100 pontos entre os 4 perfis em cada dimensão.
#
# Dimensões:
#   1. Características Dominantes
#   2. Liderança Organizacional
#   3. Gestão de Pessoas
#   4. Coesão Organizacional
#   5. Ênfase Estratégica
#   6. Critérios de Sucesso
#
# Resultado:
#   - Perfil cultural agregado
#   - Normalização 0–100
#   - Metadados completos
# -------------------------------------------------------------------------

from typing import Dict, Any


class OCAIModel:
    DIMENSIONS = {
        "D1": "Características Dominantes",
        "D2": "Liderança Organizacional",
        "D3": "Gestão de Pessoas",
        "D4": "Coesão Organizacional",
        "D5": "Ênfase Estratégica",
        "D6": "Critérios de Sucesso"
    }

    PROFILES = {
        "C": "Clan",
        "A": "Adhocracia",
        "M": "Mercado",
        "H": "Hierarquia"
    }

    NORMALIZATION_RANGE = (0, 100)

    PROFILE_DESCRIPTIONS = {
        "C": "Ambiente colaborativo, relações próximas, foco em pessoas.",
        "A": "Inovação, criatividade, flexibilidade organizacional.",
        "M": "Competitividade, metas agressivas, foco em resultados.",
        "H": "Estrutura, estabilidade, procedimentos e processos claros."
    }

    def __init__(self, responses: Dict[str, Dict[str, int]]):
        """
        responses exemplo:
        {
            "D1": {"C": 25, "A": 25, "M": 25, "H": 25},
            "D2": {"C": 40, "A": 20, "M": 20, "H": 20},
            ...
        }
        """
        self.responses = responses
        self._validate_inputs()

    # -------------------------------------------------------------
    # Validação
    # -------------------------------------------------------------

    def _validate_inputs(self):
        if not isinstance(self.responses, dict):
            raise ValueError("responses deve ser um dicionário.")

        for dim, dist in self.responses.items():
            if dim not in self.DIMENSIONS:
                raise ValueError(f"Dimensão inválida: {dim}")
            if not isinstance(dist, dict):
                raise ValueError(f"Distribuição inválida em {dim}")

            total = 0
            for profile, value in dist.items():
                if profile not in self.PROFILES:
                    raise ValueError(f"Perfil inválido: {profile}")
                if not isinstance(value, int):
                    raise ValueError(f"Pontuação inválida em {dim}/{profile}: {value}")
                if value < 0:
                    raise ValueError("Pontuações não podem ser negativas.")
                total += value

            if total != 100:
                raise ValueError(
                    f"A soma da dimensão {dim} deve ser 100. Soma atual: {total}"
                )

    # -------------------------------------------------------------
    # Normalização
    # -------------------------------------------------------------

    def _normalize(self, value: float) -> float:
        low, high = self.NORMALIZATION_RANGE
        return (value / 100) * (high - low) + low

    # -------------------------------------------------------------
    # Cálculo final
    # -------------------------------------------------------------

    def compute(self) -> Dict[str, Any]:
        # Soma agregada por perfil cultural
        aggregated = {p: 0 for p in self.PROFILES}

        for dim, dist in self.responses.items():
            for profile, value in dist.items():
                aggregated[profile] += value

        # Média por perfil (6 dimensões → divide por 6)
        averaged = {
            p: aggregated[p] / len(self.DIMENSIONS)
            for p in aggregated
        }

        # Normalização 0–100
        normalized = {
            p: round(self._normalize(v), 2)
            for p, v in averaged.items()
        }

        # Metadados completos
        metadata = {
            p: {
                "name": self.PROFILES[p],
                "raw": averaged[p],
                "normalized": normalized[p],
                "description": self.PROFILE_DESCRIPTIONS[p]
            }
            for p in averaged
        }

        # Perfil dominante
        dominant_profile = max(normalized, key=lambda k: normalized[k])

        return {
            "model": "OCAI – Perfil Cultural Organizacional",
            "profiles": normalized,
            "metadata": metadata,
            "dominant_profile": {
                "code": dominant_profile,
                "name": self.PROFILES[dominant_profile],
                "score": normalized[dominant_profile],
                "description": self.PROFILE_DESCRIPTIONS[dominant_profile]
            }
        }
