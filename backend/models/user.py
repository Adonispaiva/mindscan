from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

# Importação direta do módulo database no mesmo pacote
try:
    from backend.database import Base
except ImportError:
    import sys
    import os
    # Fallback para execução de scripts de teste isolados
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    from backend.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relação com sessões MindScan
    mindscan_tests = relationship(
        "MindscanTest",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<User id={self.id} email={self.email}>"