from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base 

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    criado_at = Column(DateTime, default=datetime.utcnow)
    diagnosticos = relationship("Diagnostico", back_populates="usuario")
    respostas = relationship("RespostasBrutas", back_populates="usuario")

class RespostasBrutas(Base):
    __tablename__ = "respostas_brutas"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    dados_respostas = Column(JSONB, nullable=False) 
    versao_algoritmo = Column(String(20), default="V4")
    criado_at = Column(DateTime, default=datetime.utcnow)
    usuario = relationship("Usuario", back_populates="respostas")

class Diagnostico(Base):
    __tablename__ = "diagnosticos"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    score_big5 = Column(JSONB, nullable=True)     
    score_clinico = Column(JSONB, nullable=True)  
    score_esquemas = Column(JSONB, nullable=True) 
    conclusao_mi = Column(Text, nullable=True)    
    status = Column(String(50), default="Aguardando Revisão")
    pdf_path = Column(String(512), nullable=True)
    criado_at = Column(DateTime, default=datetime.utcnow)
    usuario = relationship("Usuario", back_populates="diagnosticos")