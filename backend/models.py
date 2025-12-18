# Arquivo: backend/models.py
# MindScan Backend — SQLAlchemy Models
# Diretor Técnico: Leo Vinci — Inovexa Software
# Versão: 2.0.1 (compatibilidade + robustez)

from __future__ import annotations

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from backend.database import Base


class MindscanTest(Base):
    __tablename__ = "mindscan_tests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    answers = relationship(
        "Answer",
        back_populates="test",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    results = relationship(
        "Result",
        back_populates="test",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return f"<MindscanTest id={self.id} name={self.name!r}>"


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("mindscan_tests.id", ondelete="CASCADE"))
    question_id = Column(Integer)
    answer = Column(String)

    test = relationship("MindscanTest", back_populates="answers")

    def __repr__(self) -> str:
        return f"<Answer id={self.id} test_id={self.test_id} q={self.question_id}>"


class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("mindscan_tests.id", ondelete="CASCADE"))
    results = Column(String)  # JSON string (lista normalizada)

    test = relationship("MindscanTest", back_populates="results")

    def __repr__(self) -> str:
        return f"<Result id={self.id} test_id={self.test_id}>"
