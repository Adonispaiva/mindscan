"""
DASS – PROFILE BUILDER (Versão ULTRA SUPERIOR)
Constrói o perfil completo do DASS clássico (stress, anxiety, depression)
com camadas de enriquecimento, faixas normativas e índices interpretativos.
"""

from typing import Dict
from .dass_norms import DASSNorms
from .dass_risk_flags import DASSRiskFlags
from .dass_factor_map import DASSFactorMap


class DASSProfileBuilder:

    def __init__(self):
        self.norms = DASSNorms()
        self.flags = DASSRiskFlags()
        self.factors = DASSFactorMap()

    def build(self, raw_scores: Dict[str, float]) -> Dict:
        """
        Retorna um perfil completo e enriquecido do DASS clássico.
        """
        weighted = self.factors.weighted_scores(raw_scores)
        flags = self.flags.classify(raw_scores)
        norms = self.norms.classify(raw_scores)

        profile = {}

        for domain in raw_scores.keys():
            profile[domain] = {
                "raw_score": raw_scores[domain],
                "weighted_score": weighted.get(domain),
                "norm_class": norms.get(domain),
                "risk_flag": flags.get(domain),
                "description": self.factors.FACTOR_STRUCTURE[domain]["description"]
            }

        return {
            "domain_profiles": profile,
            "global_intensity": round(sum(weighted.values()) / len(weighted), 2)
        }
