from sqlalchemy.orm import declarative_base

Base = declarative_base()

# ============================================================
# IMPORTAÇÃO EXPLÍCITA DE TODOS OS MODELS
# (necessário para Base.metadata refletir o ORM completo)
# ============================================================

from backend.models.user import User
from backend.models.candidate import Candidate
from backend.models.mindscan_test import MindscanTest

__all__ = [
    "Base",
    "User",
    "Candidate",
    "MindscanTest",
]
