# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\ui\styles\corporate_style_manager.py
# Última atualização: 2025-12-11T09:59:27.886588

class CorporateStyleManager:
    """
    Estilos visuais corporativos aplicados a relatórios e dashboards.
    """

    STYLE = {
        "title_color": "#003366",
        "accent_color": "#006699",
        "font": "Segoe UI"
    }

    @staticmethod
    def get():
        return CorporateStyleManager.STYLE
