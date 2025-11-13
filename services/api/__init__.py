"""
Camada de serviços de API do MindScan (SynMind).

Este pacote concentra clientes, adaptadores e integrações de alto nível
para consumir o backend MindScan a partir de outros componentes:

- Jobs em segundo plano
- Ferramentas de linha de comando
- Integrações SynMind / terceiros
- Painéis internos

A ideia é manter aqui apenas código de ORQUESTRAÇÃO DE CHAMADAS,
não regras de negócio nem modelos de banco de dados.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional
import os

import requests


# ---------------------------------------------------------------------------
# Configuração de base
# ---------------------------------------------------------------------------

def get_backend_base_url(default: str = "http://localhost:8000") -> str:
    """
    Retorna a URL base do backend MindScan.

    A ordem de resolução é:
    1. Variável de ambiente MINDSCAN_BACKEND_URL
    2. Valor padrão informado (default="http://localhost:8000")
    """
    return os.getenv("MINDSCAN_BACKEND_URL", default).rstrip("/")


# ---------------------------------------------------------------------------
# Cliente HTTP simples (para scripts/serviços)
# ---------------------------------------------------------------------------

@dataclass
class MindScanAPIClient:
    """
    Cliente HTTP simples para o backend MindScan.

    Uso típico em scripts:

        from services.api import api_client

        health = api_client.get("/health")
        stats = api_client.get("/admin/stats")

    Esta classe é intencionalmente enxuta para evitar dependências pesadas.
    Frontends em TS/React devem usar seus próprios clients (ex.: axios).
    """

    base_url: str

    def _build_url(self, path: str) -> str:
        path = path.lstrip("/")
        return f"{self.base_url}/{path}"

    def get(self, path: str, **kwargs: Any) -> requests.Response:
        url = self._build_url(path)
        return requests.get(url, timeout=kwargs.pop("timeout", 10), **kwargs)

    def post(self, path: str, json_body: Optional[Dict[str, Any]] = None, **kwargs: Any) -> requests.Response:
        url = self._build_url(path)
        return requests.post(
            url,
            json=json_body,
            timeout=kwargs.pop("timeout", 10),
            **kwargs,
        )


# Instância padrão pronta para uso em scripts
api_client = MindScanAPIClient(base_url=get_backend_base_url())


__all__ = [
    "MindScanAPIClient",
    "api_client",
    "get_backend_base_url",
]
