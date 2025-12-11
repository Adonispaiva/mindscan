# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\generative\mi_blindspot_detector.py
# Última atualização: 2025-12-11T09:59:20.887954

class MIBlindspotDetector:
    """
    Identifica pontos cegos comportamentais e de autopercepção.
    """

    @staticmethod
    def detect(results: dict) -> dict:
        blindspots = []

        if results.get("big5", {}).get("consciencia", 50) < 40:
            blindspots.append("Baixa consciência pode gerar inconsistências executivas.")

        if results.get("teique", {}).get("autocontrole", 50) < 45:
            blindspots.append("Autocontrole reduzido pode gerar reatividade emocional elevada.")

        return {
            "blindspots": blindspots,
            "count": len(blindspots)
        }
