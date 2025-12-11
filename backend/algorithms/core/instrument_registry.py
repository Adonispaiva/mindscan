# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\core\instrument_registry.py
# Última atualização: 2025-12-11T09:59:20.620871

class InstrumentRegistry:
    """
    Registra todos os instrumentos disponíveis no MindScan Enterprise.
    Usado para discoverability e pipelines dinâmicos.
    """

    instruments = {}

    @staticmethod
    def register(name: str, handler):
        InstrumentRegistry.instruments[name] = handler

    @staticmethod
    def get(name: str):
        return InstrumentRegistry.instruments.get(name)

    @staticmethod
    def list_all():
        return list(InstrumentRegistry.instruments.keys())
