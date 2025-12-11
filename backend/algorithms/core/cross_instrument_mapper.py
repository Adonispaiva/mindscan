# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\core\cross_instrument_mapper.py
# Última atualização: 2025-12-11T09:59:20.620871

class CrossInstrumentMapper:
    """
    Relaciona outputs de diferentes instrumentos em parâmetros comparáveis.
    """

    @staticmethod
    def map_traits(big5: dict, teique: dict) -> dict:
        if not big5 or not teique:
            return {}

        return {
            "estabilidade_global": (100 - big5.get("neuroticismo", 50) + teique.get("autocontrole", 50)) / 2,
            "sociabilidade_afetiva": (big5.get("extroversao", 50) + teique.get("empatia", 50)) / 2
        }

    @staticmethod
    def map_culture(ocai: dict) -> dict:
        if not ocai:
            return {}
        return {
            "cultura_predominante": max(ocai, key=ocai.get),
            "intensidade_cultural": max(ocai.values())
        }
