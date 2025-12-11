# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\ui\dashboard_layout_manager.py
# Última atualização: 2025-12-11T09:59:27.870966

class DashboardLayoutManager:
    """
    Gerencia layouts do Dashboard via estrutura modular.
    """

    DEFAULT_LAYOUT = {
        "header": True,
        "sidebar": True,
        "widgets": ["global_stats", "team_map", "risk_overview"]
    }

    @staticmethod
    def get_default():
        return DashboardLayoutManager.DEFAULT_LAYOUT
