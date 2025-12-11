# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\helpers\payload_integrator.py
# Última atualização: 2025-12-11T09:59:21.154630

# -*- coding: utf-8 -*-
"""
payload_integrator.py
---------------------

Integra o payload original do usuário com o payload gerado pelo Orchestrator.
"""

from typing import Dict, Any


class PayloadIntegrator:

    @staticmethod
    def merge(original: Dict[str, Any], generated: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge inteligente:
        - mantém valores originais
        - complementa com campos gerados
        - preserva compatibilidade com CorporateRenderer
        """
        merged = {}

        for key in set(original.keys()).union(generated.keys()):
            if key in original and key in generated:
                # valores do orchestrator prevalecem se estruturais
                if isinstance(generated[key], dict) or isinstance(generated[key], list):
                    merged[key] = generated[key]
                else:
                    merged[key] = original[key]
            elif key in original:
                merged[key] = original[key]
            else:
                merged[key] = generated[key]

        return merged
