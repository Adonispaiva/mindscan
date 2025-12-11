# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\mindgen\ui\mindgen_theme_manager.py
# Última atualização: 2025-12-11T09:59:27.730331

class MindGenThemeManager:
    """
    Define temas visuais específicos do MindGen (independente do Web Enterprise).
    """

    THEMES = {
        "light": {"base": "#FFFFFF", "accent": "#1A73E8"},
        "dark": {"base": "#0D1117", "accent": "#58A6FF"}
    }

    @staticmethod
    def get(theme: str):
        return MindGenThemeManager.THEMES.get(theme, MindGenThemeManager.THEMES["light"])
