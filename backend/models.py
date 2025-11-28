# Caminho: backend/models.py
# MindScan — MODELOS ORM (SQLAlchemy 2.0+)
# Diretor Técnico: Leo Vinci — Inovexa Software

from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
    JSON,
)
from sqlalchemy.orm import relationship

from backend.database import Base

# =============================
# 1) USUÁRIOS / PROFISSIONAIS
# =============================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(200), nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    password_hash = Column(String(300), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    tests = relationship("MindscanTest", back_populates="user")

    def __repr__(self):
        return f"<User {self.email}>"


# =============================
# 2) PESSOA AVALIADA (CANDIDATO)
# =============================
class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(200), nullable=False)
    age = Column(Integer)
    email = Column(String(200))
    phone = Column(String(50))

    created_at = Column(DateTime, default=datetime.utcnow)

    tests = relationship("MindscanTest", back_populates="candidate")

    def __repr__(self):
        return f"<Candidate {self.full_name}>"


# =============================
# 3) TESTE MINDSCAN (SESSÃO)
# =============================
class MindscanTest(Base):
    __tablename__ = "mindscan_tests"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)

    status = Column(String(50), default="pending")
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

    final_score = Column(Float)
    dominant_profile = Column(String(200))

    user = relationship("User", back_populates="tests")
    candidate = relationship("Candidate", back_populates="tests")
    answers = relationship("MindscanAnswers", back_populates="test")
    results = relationship("MindscanResult", back_populates="test")
    report = relationship("MindscanReport", back_populates="test", uselist=False)

    def __repr__(self):
        return f"<MindscanTest ID={self.id}>"


# =============================
# 4) RESPOSTAS DO TESTE (BRUTAS)
# =============================
class MindscanAnswers(Base):
    __tablename__ = "mindscan_answers"

    id = Column(Integer, primary_key=True)
    test_id = Column(Integer, ForeignKey("mindscan_tests.id"), nullable=False)

    answers_json = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    test = relationship("MindscanTest", back_populates="answers")

    def __repr__(self):
        return f"<MindscanAnswers Test={self.test_id}>"


# =============================
# 5) RESULTADOS INTERMEDIÁRIOS
# =============================
class MindscanResult(Base):
    __tablename__ = "mindscan_results"

    id = Column(Integer, primary_key=True)
    test_id = Column(Integer, ForeignKey("mindscan_tests.id"), nullable=False)

    dimension = Column(String(200), nullable=False)
    score = Column(Float, nullable=False)
    descriptor = Column(Text)
    metadata = Column(JSON)

    created_at = Column(DateTime, default=datetime.utcnow)

    test = relationship("MindscanTest", back_populates="results")

    def __repr__(self):
        return f"<MindscanResult {self.dimension}={self.score}>"


# =============================
# 6) RELATÓRIO FINAL (PDF)
# =============================
class MindscanReport(Base):
    __tablename__ = "mindscan_reports"

    id = Column(Integer, primary_key=True)
    test_id = Column(Integer, ForeignKey("mindscan_tests.id"), nullable=False)

    pdf_path = Column(String(500), nullable=False)
    metadata = Column(JSON)

    created_at = Column(DateTime, default=datetime.utcnow)

    test = relationship("MindscanTest", back_populates="report")

    def __repr__(self):
        return f"<MindscanReport Test={self.test_id}>"


# =============================
# 7) AUDITORIA / LOGS
# =============================
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)
    action = Column(String(200), nullable=False)
    user_email = Column(String(200))
    test_id = Column(Integer)

    detail = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<AuditLog {self.action}>"