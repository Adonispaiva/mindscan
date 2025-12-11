# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\services\web_log_service.py
# Última atualização: 2025-12-11T09:59:27.870966

class WebLogService:
    """
    Serviço de logging do MindScan Web.
    """

    logs = []

    @staticmethod
    def add(log: str):
        WebLogService.logs.append(log)

    @staticmethod
    def fetch():
        return WebLogService.logs
