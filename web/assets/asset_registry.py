# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\assets\asset_registry.py
# Última atualização: 2025-12-11T09:59:27.839711

class AssetRegistry:
    """
    Repositório de assets Web (ícones, logos, estilos).
    """

    ASSETS = {
        "logo_main": "/static/img/logo_mindscan.png",
        "icon_dashboard": "/static/icons/dashboard.svg"
    }

    @staticmethod
    def get(asset: str):
        return AssetRegistry.ASSETS.get(asset)
