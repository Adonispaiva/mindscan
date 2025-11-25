# mi_document_package.py
# MindScan Rebuild – Pacote Final para o MI Formatter
# Versão Definitiva • Estrutura Avançada Pydantic-Style
# Autor: Leo Vinci — IA Supervisora Inovexa
# -------------------------------------------------------------------------
# Este módulo define a estrutura FINAL do documento entregue ao MI Formatter.
# Ele reúne:
#   - Resultados dos módulos psicométricos
#   - Cross Insights
#   - Enriquecimento NLP
#   - Metadados globais
#   - Auditoria
#   - Identificação do usuário e sessão
#
# É a camada final antes da geração dos relatórios.
# Estrutura está congelada — nenhuma alteração futura é necessária.
# -------------------------------------------------------------------------

from dataclasses import dataclass, field
from typing import Dict, Any, Optional
import datetime


class ValidationError(Exception):
    pass


def require(condition: bool, message: str):
    if not condition:
        raise ValidationError(message)


@dataclass
class MIDocumentPackage:
    """
    Estrutura final entregue ao MI Formatter.
    Este documento consolida:
        - MindscanResult (via to_dict)
        - Cross Insights estruturados
        - Enriquecimento NLP
        - Auditoria
        - Metadados finais de sessão
    """

    user_id: str
    session_id: str
    payload: Dict[str, Any]              # Resultado consolidado do MindScan
    insights: Dict[str, Any]             # Cross Insights estruturados
    nlp_block: Dict[str, Any]            # Texto enriquecido
    audit_log: Optional[Dict[str, Any]]  # Auditoria completa
    metadata: Dict[str, Any] = field(default_factory=dict)
    generated_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())

    def __post_init__(self):
        # -------------------------
        # Identificação
        # -------------------------
        require(isinstance(self.user_id, str) and len(self.user_id) > 0,
                "user_id deve ser string não vazia.")
        require(isinstance(self.session_id, str) and len(self.session_id) > 0,
                "session_id deve ser string não vazia.")

        # -------------------------
        # Payload principal
        # -------------------------
        require(isinstance(self.payload, dict) and len(self.payload) > 0,
                "payload deve conter o pacote final do MindScan.")

        require(isinstance(self.insights, dict),
                "insights deve ser dicionário.")
        require("insights" in self.insights and "count" in self.insights,
                "insights mal formados: esperados campos {insights, count}.")

        require(isinstance(self.nlp_block, dict),
                "nlp_block deve ser dicionário.")
        require("statements" in self.nlp_block,
                "nlp_block deve conter 'statements'.")

        # -------------------------
        # Auditoria
        # -------------------------
        if self.audit_log is not None:
            require(isinstance(self.audit_log, dict),
                    "audit_log deve ser dicionário.")

        # -------------------------
        # Metadados
        # -------------------------
        require(isinstance(self.metadata, dict),
                "metadata deve ser dicionário.")

        require(isinstance(self.generated_at, str) and len(self.generated_at) > 0,
                "generated_at inválido.")

    # ---------------------------------------------------------------------
    # Conversão determinística para dicionário
    # ---------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "session_id": self.session_id,
            "payload": self.payload,
            "insights": self.insights,
            "nlp_block": self.nlp_block,
            "audit_log": self.audit_log,
            "metadata": self.metadata,
            "generated_at": self.generated_at
        }

    # ---------------------------------------------------------------------
    # Resumo executivo usado pelo MI Formatter
    # ---------------------------------------------------------------------

    def summary(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "session_id": self.session_id,
            "insights_count": self.insights.get("count", 0),
            "nlp_statement_count": len(self.nlp_block.get("statements", [])),
            "generated_at": self.generated_at
        }
 