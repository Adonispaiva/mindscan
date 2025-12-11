# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\dass\dass_summary.py
# Última atualização: 2025-12-11T09:59:20.652172

"""
DASS – SUMMARY GENERATOR (Versão ULTRA SUPERIOR)
Gera resumo estruturado, de leitura rápida, consolidando
informações essenciais do DASS clássico.
"""

from typing import Dict


class DASSSummary:

    @staticmethod
    def summarize(profile: Dict) -> Dict:
        """
        Constrói resumo executivo do perfil DASS.
        """
        domains = profile.get("domain_profiles", {})
        global_intensity = profile.get("global_intensity", 0)

        highlights = []
        for dname, pdata in domains.items():
            risk = pdata.get("risk_flag")
            if risk in ("red", "orange"):
                highlights.append(
                    f"{dname.capitalize()} em estado crítico ({risk})."
                )

        return {
            "global_intensity": global_intensity,
            "critical_alerts": highlights,
            "domains": {
                d: {
                    "score": pdata["raw_score"],
                    "classification": pdata["norm_class"],
                    "risk": pdata["risk_flag"]
                }
                for d, pdata in domains.items()
            }
        }
