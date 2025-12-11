# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\generative\mi_conflict_radar.py
# Última atualização: 2025-12-11T09:59:20.903579

class MIConflictRadar:
    """
    Identifica potenciais disparadores de conflitos comportamentais.
    """

    @staticmethod
    def detect(results: dict) -> dict:
        radars = {}

        ext = results.get("big5", {}).get("extroversao", 50)
        ama = results.get("big5", {}).get("amabilidade", 50)

        radars["dominance_trigger"] = ext > 70
        radars["relational_trigger"] = ama < 40

        return radars
