# MindScan Backend Package
# ========================
# Este arquivo inicializa o pacote backend e expõe componentes centrais.

from .config import settings
from .database import Base, get_session, engine
