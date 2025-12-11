# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\infrastructure\error_monitor.py
# Última atualização: 2025-12-11T09:59:21.159629

# -*- coding: utf-8 -*-
"""
error_monitor.py
----------------

Sistema interno de monitoramento de erros.
Registra exceções, origem, contexto e metadados.
Futuro: integração com Sentry, Datadog ou SynMind Monitor.
"""

import traceback
from typing import Dict, Any, List


class ErrorMonitor:
    _errors: List[Dict[str, Any]] = []

    @classmethod
    def capture(cls, err: Exception, context: Dict[str, Any] = None):
        cls._errors.append({
            "error": str(err),
            "type": err.__class__.__name__,
            "trace": traceback.format_exc(),
            "context": context or {},
        })

    @classmethod
    def get_errors(cls) -> List[Dict[str, Any]]:
        return cls._errors

    @classmethod
    def clear(cls):
        cls._errors.clear()
