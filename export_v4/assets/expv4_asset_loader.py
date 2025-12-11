# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\export_v4\assets\expv4_asset_loader.py
# Última atualização: 2025-12-11T09:59:27.574098

class EXPV4AssetLoader:
    """
    Localiza e carrega assets necessários para exportações (logos, ícones).
    """

    @staticmethod
    def load(name: str):
        return f"/assets/{name}.bin"
