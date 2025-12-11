# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\ui\icons\ui_icon_manager.py
# Última atualização: 2025-12-11T09:59:27.870966

class UIIconManager:
    """
    Centraliza ícones usados pela interface.
    """

    ICONS = {
        "home": "🏠",
        "stats": "📊",
        "risk": "⚠️"
    }

    @staticmethod
    def get(icon: str):
        return UIIconManager.ICONS.get(icon, "❓")
