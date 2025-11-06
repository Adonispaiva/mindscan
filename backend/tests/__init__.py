backend/tests/__init__.py

# Este arquivo permite que o diretório tests seja tratado como um pacote Python.


backend/tests/test_health.py

import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


backend/tests/test_main.py

import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert "MindScan" in response.text


backend/tests/test_user.py

import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_user_login():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {"username": "admin", "password": "admin"}
        response = await ac.post("/login", json=payload)
    assert response.status_code in [200, 401]  # Ajustável conforme lógica do projeto


# Observações:
# 1. Caminhos corrigidos: todos assumem que "main.py" está em "backend/main.py".
# 2. Para rodar corretamente:
#    - Execute os testes a partir do diretório `backend` com: `pytest tests/`
#    - Verifique se as dependências estão instaladas: `pip install -r requirements.txt`
#    - Assegure que o app esteja exportado como `app` em `main.py`.
# 3. Você pode adaptar endpoints e payloads conforme sua lógica real.
