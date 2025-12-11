# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\ui\themes\theme_manager_v4.py
# Última atualização: 2025-12-11T09:59:27.886588

class ThemeManagerV4:
    """
    Gerencia temas visuais do MindScan Web Enterprise.
    """

    THEMES = {
        "default": {
            "primary": "#1A73E8",
            "secondary": "#185ABC",
            "background": "#F5F7FA"
        },
        "dark": {
            "primary": "#0F172A",
            "secondary": "#1E293B",
            "background": "#000000"
        }
    }

    @staticmethod
    def get(theme: str):
        return ThemeManagerV4.THEMES.get(theme, ThemeManagerV4.THEMES["default"])
