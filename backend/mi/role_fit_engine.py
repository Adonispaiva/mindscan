# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\role_fit_engine.py
# Última atualização: 2025-12-11T09:59:20.872348

class RoleFitEngine:
    """
    Analisa compatibilidade com cargos baseando-se em múltiplos instrumentos.
    """

    ROLE_REQUIREMENTS = {
        "lider": {"extroversao": 60, "consciencia": 55, "autocontrole": 50},
        "analista": {"consciencia": 65, "amabilidade": 50},
        "comercial": {"extroversao": 70, "empatia": 60}
    }

    @staticmethod
    def evaluate(role: str, results: dict) -> dict:
        req = RoleFitEngine.ROLE_REQUIREMENTS.get(role.lower())
        if not req:
            return {"role": role, "fit": False, "reason": "Cargo não mapeado."}

        score = 0
        max_score = len(req)

        for trait, threshold in req.items():
            value = results.get("big5", {}).get(trait, 50) if trait in results.get("big5", {}) \
                else results.get("teique", {}).get(trait, 50)
            if value >= threshold:
                score += 1

        fit_ratio = score / max_score
        return {
            "role": role,
            "fit": fit_ratio >= 0.6,
            "ratio": round(fit_ratio, 2)
        }
