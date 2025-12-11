# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\mindgen\ui\adaptive_dashboard_layout.py
# Última atualização: 2025-12-11T09:59:27.730331

class AdaptiveDashboardLayout:
    """
    Monta layouts dinâmicos que se adaptam ao perfil analisado.
    """

    @staticmethod
    def build(context: dict):
        if context.get("stress") > 60:
            return {"layout": "stress_focus"}
        return {"layout": "balanced"}
