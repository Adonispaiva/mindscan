# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\mi_risk_detector.py
# Última atualização: 2025-12-11T09:59:20.872348

class MIRiskDetector:
    """
    Identifica riscos comportamentais baseados nos instrumentos.
    """

    @staticmethod
    def detect(results: dict) -> dict:
        if not results:
            return {}

        risks = {}

        if "big5" in results:
            neuro = results["big5"].get("neuroticismo", 50)
            if neuro > 70:
                risks["estresse"] = "alto"

        if "teique" in results:
            autocontrole = results["teique"].get("autocontrole", 50)
            if autocontrole < 30:
                risks["impulsividade"] = "elevada"

        if "dass21" in results:
            depressao = results["dass21"].get("depressao", 0)
            if depressao > 14:
                risks["depressao_indicativa"] = "atenção necessária"

        return risks
