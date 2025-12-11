# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\export_v4\styles\export_style_manager_v4.py
# Última atualização: 2025-12-11T09:59:27.636599

class ExportStyleManagerV4:
    """
    Controla estilos unificados de exportação (cores, fontes, espaçamentos).
    """

    STYLE = {
        "font": "Segoe UI",
        "title_color": "#1A73E8",
        "text_color": "#333333"
    }

    @staticmethod
    def get():
        return ExportStyleManagerV4.STYLE
