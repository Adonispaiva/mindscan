from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True)
    criado_at = Column(DateTime, default=datetime.utcnow)
    diagnosticos = relationship("Diagnostico", back_populates="usuario")

class Diagnostico(Base):
    __tablename__ = "diagnosticos"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    ansiedade_score = Column(Float, default=0.0)
    depressao_score = Column(Float, default=0.0)
    stress_score = Column(Float, default=0.0)
    conclusao = Column(Text, nullable=True)
    criado_at = Column(DateTime, default=datetime.utcnow)
    
    usuario = relationship("Usuario", back_populates="diagnosticos")
    metricas = relationship("MetricaPsicometrica", back_populates="diagnostico")

class MetricaPsicometrica(Base):
    __tablename__ = "metricas_psicometricas"
    id = Column(Integer, primary_key=True, index=True)
    diagnostico_id = Column(Integer, ForeignKey("diagnosticos.id"))
    chave = Column(String(100))
    valor = Column(Float)
    interpretacao = Column(Text, nullable=True)
    
    diagnostico = relationship("Diagnostico", back_populates="metricas")