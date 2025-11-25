# audit_log.py
# MindScan Rebuild – Modelo Final de Auditoria
# Versão Definitiva • Estrutura Avançada Pydantic-Style
# Autor: Leo Vinci — IA Supervisora Inovexa
# -------------------------------------------------------------------------
# Este módulo define o modelo de Auditoria Interna do MindScan:
#   - Registra cada etapa do processamento
#   - Guarda eventos, erros, avisos e informações importantes
#   - É utilizado pelo Runtime Kernel e Diagnostic Engine
#   - É parte integrante do pacote final entregue ao MI Formatter
#   - Estrutura final congelada, sem necessidade de revisões futuras
# -------------------------------------------------------------------------

from dataclasses import dataclass, field
from typing import Any, Dict, List
import datetime


class ValidationError(Exception):
    pass


def require(condition: bool, message: str):
    if not condition:
        raise ValidationError(message)


@dataclass
class AuditEntry:
    """
    Uma entrada individual de auditoria.
    """

    timestamp: datetime.datetime
    event: str
    detail: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        require(isinstance(self.timestamp, datetime.datetime),
                "timestamp deve ser datetime válido.")

        require(isinstance(self.event, str) and len(self.event) > 0,
                "event deve ser string não vazia.")

        require(isinstance(self.detail, dict),
                "detail deve ser um dicionário.")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "event": self.event,
            "detail": self.detail
        }


@dataclass
class AuditLog:
    """
    Registro completo de auditoria do MindScan.
    Responsável por:
        - registrar eventos
        - registrar erros
        - registrar informações do Kernel
        - apresentar trilha completa para relatórios e MI
    """

    session_id: str
    entries: List[AuditEntry] = field(default_factory=list)
    started_at: datetime.datetime = field(default_factory=datetime.datetime.utcnow)
    finished_at: datetime.datetime = None

    def __post_init__(self):
        require(isinstance(self.session_id, str) and len(self.session_id) > 0,
                "session_id deve ser string não vazia.")

    # ---------------------------------------------------------------------
    # Registro de eventos
    # ---------------------------------------------------------------------

    def log_event(self, event: str, detail: Dict[str, Any] = None):
        entry = AuditEntry(
            timestamp=datetime.datetime.utcnow(),
            event=event,
            detail=detail or {}
        )
        self.entries.append(entry)

    def log_error(self, message: str, detail: Dict[str, Any] = None):
        entry = AuditEntry(
            timestamp=datetime.datetime.utcnow(),
            event=f"ERROR: {message}",
            detail=detail or {}
        )
        self.entries.append(entry)

    def close(self):
        self.finished_at = datetime.datetime.utcnow()

    # ---------------------------------------------------------------------
    # Conversões
    # ---------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "started_at": self.started_at.isoformat(),
            "finished_at": self.finished_at.isoformat() if self.finished_at else None,
            "entries": [e.to_dict() for e in self.entries]
        }

    def summary(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "event_count": len(self.entries),
            "started_at": self.started_at.isoformat(),
            "finished_at": self.finished_at.isoformat() if self.finished_at else None
        }
