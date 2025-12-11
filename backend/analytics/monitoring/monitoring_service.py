# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\analytics\monitoring\monitoring_service.py
# Última atualização: 2025-12-11T09:59:20.745854

import time

class MonitoringService:
    """
    Fornece ferramentas simples de tempo de execução
    para rastrear blocos críticos da aplicação.
    """

    @staticmethod
    def timed(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            out = func(*args, **kwargs)
            duration = round(time.time() - start, 4)
            return out, duration
        return wrapper
