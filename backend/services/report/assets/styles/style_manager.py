# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\report\assets\styles\style_manager.py
# Última atualização: 2025-12-11T09:59:21.276887

class StyleManager:
    """
    Carrega estilos, paletas e configurações visuais dos relatórios.
    """

    DEFAULT_STYLES = {
        "font_family": "Arial",
        "primary_color": "#2A4B7C",
        "secondary_color": "#6F8FBF",
        "accent_color": "#D98E04"
    }

    @staticmethod
    def get():
        return StyleManager.DEFAULT_STYLES
