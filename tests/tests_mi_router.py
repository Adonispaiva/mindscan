import asyncio
import httpx
import pytest
import json
import os
from typing import Dict, Any

# =============================
# CONFIGURAÇÃO DO TESTE
# =============================
DOCKER_API_HOST = os.getenv("MINDSCAN_API_HOST", "http://mindscan_backend:8000")
ENDPOINTS = {
    "analyze": "/api/v3/matcher/analyze",
    "insights": "/api/v3/matcher/insights",
    "patterns": "/api/v3/matcher/patterns"
}

COGNITIVE_PROFILES = [
    {"user_id": f"U{i:03}", "profile": p}
    for i, p in enumerate(["Analitico", "Criativo", "Emocional", "Estrategico"], start=1)
]

EXPECTED_KEYS = {
    "analyze": ["score", "dimension", "confidence"],
    "insights": ["summary", "dominant_trait", "recommendations"],
    "patterns": ["pattern_id", "correlation", "category"]
}

TIMEOUT = 8.0

# =============================
# FUNÇÕES AUXILIARES
# =============================
async def post_json(client: httpx.AsyncClient, endpoint: str, payload: Dict[str, Any]):
    response = await client.post(endpoint, json=payload, timeout=TIMEOUT)
    return response


def validate_schema(endpoint: str, data: Dict[str, Any]):
    keys = EXPECTED_KEYS.get(endpoint.strip("/api/v3/matcher/"), [])
    missing = [k for k in keys if k not in data]
    assert not missing, f"Schema incorreto em {endpoint}: faltam campos {missing}"


# =============================
# TESTES DE INTEGRAÇÃO
# =============================
@pytest.mark.asyncio
@pytest.mark.integration
async def test_matcher_endpoints_integrity():
    async with httpx.AsyncClient(base_url=DOCKER_API_HOST) as client:
        for name, endpoint in ENDPOINTS.items():
            for profile in COGNITIVE_PROFILES:
                resp = await post_json(client, endpoint, profile)
                assert resp.status_code == 200, f"Falha HTTP em {endpoint} ({resp.status_code})"
                data = resp.json()
                validate_schema(endpoint, data)
                assert data.get("confidence", 0) >= 0, "Confiança inválida"
                assert isinstance(data, dict), "Resposta não é JSON válido"


@pytest.mark.asyncio
@pytest.mark.stress
async def test_concurrent_requests_stability():
    async with httpx.AsyncClient(base_url=DOCKER_API_HOST) as client:
        tasks = []
        for i in range(10):
            profile = {"user_id": f"stress_{i}", "profile": "Analitico"}
            tasks.append(post_json(client, ENDPOINTS["analyze"], profile))
        results = await asyncio.gather(*tasks)
        statuses = [r.status_code for r in results]
        assert all(s == 200 for s in statuses), f"Erros HTTP detectados: {statuses}"


@pytest.mark.asyncio
@pytest.mark.functional
async def test_cross_endpoint_consistency():
    async with httpx.AsyncClient(base_url=DOCKER_API_HOST) as client:
        profile = {"user_id": "cross001", "profile": "Estrategico"}
        analyze_resp = await post_json(client, ENDPOINTS["analyze"], profile)
        insights_resp = await post_json(client, ENDPOINTS["insights"], profile)
        patterns_resp = await post_json(client, ENDPOINTS["patterns"], profile)

        analyze_data = analyze_resp.json()
        insights_data = insights_resp.json()
        patterns_data = patterns_resp.json()

        # Consistência cruzada: os traços dominantes devem estar correlacionados
        assert insights_data.get("dominant_trait") in [patterns_data.get("category"), analyze_data.get("dimension")], (
            "Inconsistência entre análise, padrões e insights"
        )


@pytest.mark.asyncio
@pytest.mark.validation
async def test_invalid_payload_rejection():
    async with httpx.AsyncClient(base_url=DOCKER_API_HOST) as client:
        bad_payload = {"invalid": "data"}
        response = await client.post(ENDPOINTS["analyze"], json=bad_payload)
        assert response.status_code in [400, 422], f"Falha esperada, mas obtido {response.status_code}"