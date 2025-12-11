# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\routes\web_router_registry.py
# Última atualização: 2025-12-11T09:59:27.855343

class WebRouterRegistry:
    """
    Registra todas as rotas Web de forma centralizada.
    """

    routers = []

    @staticmethod
    def register(router):
        WebRouterRegistry.routers.append(router)

    @staticmethod
    def list():
        return WebRouterRegistry.routers
