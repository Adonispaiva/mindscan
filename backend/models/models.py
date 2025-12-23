from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from db.session import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    data = Column(DateTime, default=datetime.utcnow) # Nomeado como 'data' para bater com o dashboard