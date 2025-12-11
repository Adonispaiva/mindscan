# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\state\dashboard_state_manager.py
# Última atualização: 2025-12-11T09:59:27.870966

class DashboardStateManager:
    """
    Armazena estado atual do dashboard para navegação persistente.
    """

    state = {"active_tab": "overview"}

    @staticmethod
    def set_tab(tab: str):
        DashboardStateManager.state["active_tab"] = tab

    @staticmethod
    def get():
        return DashboardStateManager.state
