from __future__ import annotations

import os
from datetime import datetime
from typing import Generator, Optional

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session

# Banco isolado do legado para evitar colisões e circular imports.
MINDSCAN_DB_URL = (
    os.getenv("MINDSCAN_DB_URL")
    or os.getenv("MINDSCAN_DATABASE_URL")
    or "sqlite:///./mindscan_ms.db"
)

_is_sqlite = MINDSCAN_DB_URL.startswith("sqlite:")

_engine_kwargs = {"pool_pre_ping": True, "future": True}
if _is_sqlite:
    _engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(MINDSCAN_DB_URL, **_engine_kwargs)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)

Base = declarative_base()

_initialized: bool = False


def init_db() -> None:
    global _initialized
    if _initialized:
        return
    Base.metadata.create_all(bind=engine)
    _initialized = True


def get_db() -> Generator[Session, None, None]:
    init_db()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class MindscanTest(Base):
    __tablename__ = "ms_tests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), default="MindScan Test", index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    answers = relationship("Answer", back_populates="test", cascade="all, delete-orphan")
    results = relationship("Result", back_populates="test", cascade="all, delete-orphan")


class Answer(Base):
    __tablename__ = "ms_answers"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("ms_tests.id", ondelete="CASCADE"), index=True)
    question_id = Column(Integer, index=True)
    answer = Column(Text)

    test = relationship("MindscanTest", back_populates="answers")


class Result(Base):
    __tablename__ = "ms_results"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("ms_tests.id", ondelete="CASCADE"), index=True)
    results_json = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    test = relationship("MindscanTest", back_populates="results")
