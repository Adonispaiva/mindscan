# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\coaching_v4\analysis\coaching_behavior_analyzer.py
# Última atualização: 2025-12-11T09:59:27.542857

class CoachingBehaviorAnalyzer:
    """
    Analisa padrões comportamentais para determinar pontos de intervenção.
    """

    @staticmethod
    def analyze(profile: dict):
        return {
            "risk_points": [k for k, v in profile.items() if v < 40],
            "strengths": [k for k, v in profile.items() if v > 70]
        }
