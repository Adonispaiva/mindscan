# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\infrastructure\performance_profiler.py
# Última atualização: 2025-12-11T09:59:21.160629

# -*- coding: utf-8 -*-
"""
performance_profiler.py
-----------------------

Ferramenta de profiling interno para medir tempo de execução de
qualquer etapa crítica do MindScan.

Uso:
    with PerformanceProfiler.track("pipeline_corporate"):
        executar_pipeline()
"""

import time
from typing import Dict


class PerformanceProfiler:
    _results: Dict[str, float] = {}

    @classmethod
    def track(cls, name: str):
        class _ProfilerContext:
            def __enter__(self_):
                self_.start = time.perf_counter()

            def __exit__(self_, exc_type, exc, tb):
                duration = time.perf_counter() - self_.start
                cls._results[name] = duration

        return _ProfilerContext()

    @classmethod
    def get_results(cls) -> Dict[str, float]:
        return cls._results

    @classmethod
    def clear(cls):
        cls._results.clear()
