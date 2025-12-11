# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\ui\ui_renderer.py
# Última atualização: 2025-12-11T09:59:27.870966

class UIRenderer:
    """
    Renderiza widgets em formato neutro para APIs e Front-end.
    """

    @staticmethod
    def render_widget(widget, data):
        return widget.render(data)
