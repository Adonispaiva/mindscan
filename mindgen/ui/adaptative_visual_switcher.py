# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\mindgen\ui\adaptative_visual_switcher.py
# Última atualização: 2025-12-11T09:59:27.728166

class AdaptiveVisualSwitcher:
    """
    Decide automaticamente qual visualização é mais relevante para o usuário.
    """

    @staticmethod
    def choose(context: dict):
        if context.get("leadership") > 70:
            return "leadership_trajectory"
        if context.get("emotional_load") > 60:
            return "emotional_curve"
        return "overview"
