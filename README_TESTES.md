# 🧪 Testes Automatizados — MindScan

## Requisitos
- Python 3.10+
- Postgres configurado (local ou Docker)
- Variáveis de ambiente presentes em `.env` ou `.env.example`
- Dependências instaladas: `pip install -r requirements.txt`

---

## 🚀 Executar localmente

```bash
pytest
```

### Com cobertura:
```bash
pytest --cov=backend --cov-report=term-missing
```

---

## 🐳 Usar com Docker

```bash
docker-compose up -d
docker-compose exec backend pytest
```

---

## 🧬 Estrutura esperada

```
mindscan/
├── backend/
│   └── routers/
├── tests/
│   ├── routers/
│   ├── conftest.py
├── .env.example
├── docker-compose.yml
├── pytest.ini
```

---

## 💡 CI/CD GitHub Actions

O workflow `backend.yml` já está pronto para rodar testes a cada `push` ou `pull_request`.

---

**Mantra de Qualidade:**
> “Cobertura de testes não é custo. É seguro de inovação.”
