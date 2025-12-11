# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\core\engine\engine.py
# Última atualização: 2025-12-11T09:59:27.558489

"""
MindScan — Cognitive Engine
Direção Técnica: Leo Vinci (Inovexa)

Este módulo implementa o motor cognitivo do sistema.
Responsável por:
    - fluxo de entrada (input pipeline)
    - execução de algoritmos psicológicos
    - aplicação de métricas
    - pontuação
    - geração de perfis
    - integração com o CORE e com o backend
"""

from datetime import datetime
from typing import Any, Dict, List, Callable

from core import corelog
from core.algorithms import base_algorithm
from core.metrics import metrics
from core.scoring import scorer
from core.profiles import profiler


class MindScanEngine:
    """
    Motor cognitivo de alto nível.
    Organiza todo o pipeline do MindScan.
    """

    def __init__(self, safe_mode: bool = False):
        self.safe_mode = safe_mode
        self.pre_hooks: List[Callable] = []
        self.post_hooks: List[Callable] = []
        corelog("MindScanEngine inicializada.")

    # ----------------------------------------------------------
    # Hook System
    # ----------------------------------------------------------
    def add_pre_hook(self, fn: Callable):
        self.pre_hooks.append(fn)
        corelog(f"Pre-hook registrado: {fn.__name__}")

    def add_post_hook(self, fn: Callable):
        self.post_hooks.append(fn)
        corelog(f"Post-hook registrado: {fn.__name__}")

    def _execute_hooks(self, hooks: List[Callable], payload: Dict):
        for fn in hooks:
            corelog(f"Executando hook: {fn.__name__}")
            try:
                fn(payload)
            except Exception as e:
                corelog(f"[ERRO] Hook {fn.__name__} falhou: {e}")

    # ----------------------------------------------------------
    # Processo Cognitivo Principal
    # ----------------------------------------------------------
    def process(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Pipeline cognitivo completo do MindScan:
            1. pré-processamento
            2. execução de algoritmos psicológicos
            3. cálculo de métricas
            4. scoring
            5. geração de perfil
            6. pós-processamento
        """

        start = datetime.now()
        corelog("========== MindScanEngine: INÍCIO DO PROCESSO ==========")

        payload = {"input": user_input, "timestamp": start, "stages": {}}

        # 1. Pré-processamento
        self._execute_hooks(self.pre_hooks, payload)

        # 2. Algoritmos psicológicos (baselines)
        try:
            algo_result = base_algorithm.run(user_input)
            payload["stages"]["algorithms"] = algo_result
        except Exception as e:
            corelog(f"[ERRO] Execução de algoritmos: {e}")
            algo_result = {}

        # 3. Métricas internas
        try:
            metric_result = metrics.evaluate(algo_result)
            payload["stages"]["metrics"] = metric_result
        except Exception as e:
            corelog(f"[ERRO] Métricas: {e}")
            metric_result = {}

        # 4. Scoring
        try:
            score = scorer.compute_score(algo_result, metric_result)
            payload["stages"]["score"] = score
        except Exception as e:
            corelog(f"[ERRO] Score: {e}")
            score = None

        # 5. Perfil psicológico
        try:
            profile = profiler.generate_profile(score, metric_result)
            payload["stages"]["profile"] = profile
        except Exception as e:
            corelog(f"[ERRO] Perfil: {e}")
            profile = {}

        # 6. Pós-processamento
        self._execute_hooks(self.post_hooks, payload)

        corelog("========== MindScanEngine: FIM DO PROCESSO ==========")

        return {
            "input": user_input,
            "algorithms": algo_result,
            "metrics": metric_result,
            "score": score,
            "profile": profile,
            "timestamp": start.isoformat(),
        }
