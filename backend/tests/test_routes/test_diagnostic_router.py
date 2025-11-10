import pytest
from httpx import AsyncClient
from main import app

# --------------------------------------------------
# 🔗 TESTE INTEGRADO: POST /diagnostic
# --------------------------------------------------
@pytest.mark.asyncio
async def test_post_diagnostic():
    """
    Testa a rota /diagnostic garantindo:
    - Resposta HTTP 200
    - Estrutura JSON com nome e resultado interpretado
    - Inclusão do relatório MindScan MI no retorno
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {
            "nome": "Emília",
            "scores": {
                "DEPRESSAO": 6,
                "ANSIEDADE": 4,
                "ESTRESSE": 8
            }
        }
        response = await ac.post("/diagnostic", json=payload)
        assert response.status_code == 200

        data = response.json()
        assert data["nome"] == "Emília"
        assert data["resultado"]["DEPRESSAO"]["nivel"] == "NORMAL"
        assert "Relatório MindScan MI" in data["relatorio"]
