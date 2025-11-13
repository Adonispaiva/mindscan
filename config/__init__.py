import os

# ---------------------------------------------------------------------
# URL do banco de dados
# ---------------------------------------------------------------------
# Em produção, defina a variável de ambiente DATABASE_URL.
# Em desenvolvimento, usamos SQLite local por padrão.
DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./mindscan.db")

# ---------------------------------------------------------------------
# CORS - origens permitidas
# ---------------------------------------------------------------------
_default_origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:4200",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:4200",
]

_env_origins = os.getenv("ALLOWED_ORIGINS")

if _env_origins:
    ALLOWED_ORIGINS = [
        origin.strip()
        for origin in _env_origins.split(",")
        if origin.strip()
    ]
else:
    ALLOWED_ORIGINS = _default_origins
