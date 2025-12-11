# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\ui\dashboard_widget_binder.py
# Última atualização: 2025-12-11T09:59:27.870966

class DashboardWidgetBinder:
    """
    Conecta widgets aos seus respectivos providers de dados.
    """

    @staticmethod
    def bind(widget_class, provider, *args, **kwargs):
        data = provider.fetch(*args, **kwargs)
        return widget_class.render(data)
