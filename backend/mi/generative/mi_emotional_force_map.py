# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\generative\mi_emotional_force_map.py
# Última atualização: 2025-12-11T09:59:20.903579

class MIEmotionalForceMap:
    """
    Mapeia forças emocionais e pontos fracos do indivíduo.
    """

    @staticmethod
    def map(results: dict) -> dict:
        tei = results.get("teique", {})

        return {
            "fortes": {
                "empatia": tei.get("empatia", 50),
                "autocontrole": tei.get("autocontrole", 50)
            },
            "fracos": {
                "expressao": 100 - tei.get("expressao", 50)
            }
        }
