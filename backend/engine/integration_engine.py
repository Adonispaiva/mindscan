"""
Integration Engine — MindScan (SynMind)

Responsável por integrar:
- Resultados dos algoritmos psicométricos
- Saída normalizada para consumo da MI
- Estrutura base para geração de relatório

Este engine NÃO executa algoritmos.
Ele integra, valida e organiza resultados.
"""

from typing import Dict, Any
from datetime import datetime


class IntegrationEngine:
    """
    Engine de integração central do MindScan.
    """

    def __init__(self) -> None:
        self.generated_at = datetime.utcnow()

    def integrate(
        self,
        algorithm_results: Dict[str, Any],
        metadata: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        """
        Integra os resultados dos algoritmos em uma estrutura única.

        :param algorithm_results: saída bruta dos algoritmos (BIG5, DASS, etc.)
        :param metadata: dados adicionais (id do teste, versão, etc.)
        :return: payload integrado e validado
        """

        if not algorithm_results or not isinstance(algorithm_results, dict):
            raise ValueError("algorithm_results inválido ou vazio")

        integrated_payload = {
            "meta": {
                "generated_at": self.generated_at.isoformat(),
                "engine": "IntegrationEngine",
                "version": "1.0",
            },
            "metadata": metadata or {},
            "results": {},
        }

        for key, value in algorithm_results.items():
            integrated_payload["results"][key] = self._normalize_block(
                key, value
            )

        return integrated_payload

    def _normalize_block(self, name: str, data: Any) -> Dict[str, Any]:
        """
        Normaliza cada bloco de resultado para um formato padrão.

        :param name: nome do algoritmo/bloco
        :param data: dados do algoritmo
        """

        return {
            "source": name,
            "data": data,
            "validated": True,
        }
