# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\analytics\metrics\metrics_service.py
# Última atualização: 2025-12-11T09:59:20.730228

import time
from collections import defaultdict

class MetricsService:
    """
    Sistema interno de métricas:
    - Latência média por endpoint
    - Contagem de requisições
    - Erros por rota
    """

    counters = defaultdict(int)
    timers = defaultdict(list)
    errors = defaultdict(int)

    @staticmethod
    def track_request(path: str, start_time: float):
        duration = round(time.time() - start_time, 4)
        MetricsService.timers[path].append(duration)
        MetricsService.counters[path] += 1

    @staticmethod
    def track_error(path: str):
        MetricsService.errors[path] += 1

    @staticmethod
    def get_snapshot():
        snapshot = {}
        for path, times in MetricsService.timers.items():
            snapshot[path] = {
                "requests": MetricsService.counters[path],
                "avg_latency": round(sum(times) / len(times), 4) if times else 0,
                "errors": MetricsService.errors[path]
            }
        return snapshot
