# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\generative\mi_emotional_regulation_engine.py
# Última atualização: 2025-12-11T09:59:20.903579

class MIEmotionalRegulationEngine:
    """
    Avalia e gera estratégias de regulação emocional baseadas no perfil.
    """

    @staticmethod
    def regulate(results: dict) -> dict:
        tei = results.get("teique", {})
        autocontrole = tei.get("autocontrole", 50)
        estresse = tei.get("estresse", 50)

        return {
            "regulation_score": round((autocontrole * 0.7) + (100 - estresse) * 0.3, 2),
            "suggested_techniques": [
                "Respiração diafragmática",
                "Ajuste cognitivo",
                "Pausa estratégica em conflitos"
            ]
        }
