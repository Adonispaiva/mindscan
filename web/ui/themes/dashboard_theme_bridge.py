# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\ui\themes\dashboard_theme_bridge.py
# Última atualização: 2025-12-11T09:59:27.886588

from .theme_manager_v4 import ThemeManagerV4

class DashboardThemeBridge:
    """
    Unifica temas entre Dashboard e demais módulos Web.
    """

    @staticmethod
    def resolve(theme: str):
        return ThemeManagerV4.get(theme)
