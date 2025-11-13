from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import Base  # <- seu Base está aqui


class Quiz(Base):
    """
    Modelo de domínio para um Quiz do MindScan.
    """

    __tablename__ = "quizzes"

    # Identificador primário
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Metadados principais
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Estado / flags
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Auditoria
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # Exemplo de relacionamento futuro com tabela de perguntas:
    # questions: Mapped[List["Question"]] = relationship(
    #     "Question",
    #     back_populates="quiz",
    #     cascade="all, delete-orphan",
    # )

    def __repr__(self) -> str:
        return f"<Quiz id={self.id} title={self.title!r} active={self.is_active}>"


# -------------------------------------------------------------------------
# Modelos Pydantic (DTOs) para uso nas rotas FastAPI
# -------------------------------------------------------------------------

from pydantic import BaseModel, Field


class QuizBase(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    category: Optional[str] = Field(default=None, max_length=100)
    is_active: bool = True
    is_public: bool = False


class QuizCreate(QuizBase):
    """Payload para criação de novos quizzes."""
    pass


class QuizUpdate(BaseModel):
    """Payload para atualização parcial/total de quizzes."""
    title: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = Field(default=None, max_length=100)
    is_active: Optional[bool] = None
    is_public: Optional[bool] = None


class QuizRead(QuizBase):
    """Modelo de resposta (saída) padrão."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# Aliases para compatibilidade com routers que usem esses nomes
QuizIn = QuizCreate
QuizOut = QuizRead
