# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\generative\mi_persona_synthesizer.py
# Última atualização: 2025-12-11T09:59:20.927433

class MIPersonaSynthesizer:
    """
    Combina múltiplos outputs MI para gerar uma persona comportamental.
    """

    @staticmethod
    def synthesize(blocks: dict) -> dict:
        persona = {
            "core_traits": blocks.get("deep_traits"),
            "social": blocks.get("social"),
            "leadership": blocks.get("leadership"),
            "stress": blocks.get("stress"),
            "opportunities": blocks.get("opps")
        }
        return persona
