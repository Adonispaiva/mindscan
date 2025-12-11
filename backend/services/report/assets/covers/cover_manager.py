# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\report\assets\covers\cover_manager.py
# Última atualização: 2025-12-11T09:59:21.276887

class CoverManager:
    """
    Gerencia capas diferentes para relatórios:
    - Executive
    - Technical
    - Psychodynamic
    - Premium
    """

    covers = {
        "executive": "covers/executive_cover.png",
        "technical": "covers/technical_cover.png",
        "psychodynamic": "covers/psychodynamic_cover.png",
        "premium": "covers/premium_cover.png"
    }

    @staticmethod
    def get(report_type: str):
        return CoverManager.covers.get(report_type, CoverManager.covers["executive"])
