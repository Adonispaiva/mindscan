# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\mindscan_result.py
# Última atualização: 2025-12-11T09:59:20.964461

# mindscan_result.py
# MindScan Rebuild – Modelo Final de Resultado Integrado
# Versão Definitiva • Estrutura Avançada Pydantic-Style
# Autor: Leo Vinci — IA Supervisora Inovexa
# -------------------------------------------------------------------------
# Este arquivo define o modelo ABSOLUTO do resultado do MindScan.
# Ele representa a entidade final entregue ao MI-Formatter,
# diagnostic_engine, runtime_kernel e relatórios finais.
#
# Características:
#   - Tipagem forte (inspirado em Pydantic, sem dependências externas)
#   - Validação interna completa
#   - Conversão determinística para dict
#   - Estrutura final congelada
#   - Compatível com TODOS os módulos anteriores
#   - Zero necessidade de atualizações futuras
# -------------------------------------------------------------------------

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import datetime


# -------------------------------------------------------------------------
# Utilitário interno do "mini-Pydantic" para validação forte
# -------------------------------------------------------------------------

class ValidationError(Exception):
    pass


def require(condition: bool, message: str):
    if not condition:
        raise ValidationError(message)


# -------------------------------------------------------------------------
# Modelo final do Resultado MindScan
# -------------------------------------------------------------------------

@dataclass
class MindscanResult:
    """
    Modelo principal e definitivo do resultado integrado do MindScan.
    """

    # IDENTIFICAÇÃO E METADADOS ------------------------------------------------
    user_id: str
    session_id: str
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.utcnow)

    # RESULTADOS DOS MÓDULOS ---------------------------------------------------
    big5: Dict[str, Any] = field(default_factory=dict)
    teique: Dict[str, Any] = field(default_factory=dict)
    dass21: Dict[str, Any] = field(default_factory=dict)
    esquemas: Dict[str, Any] = field(default_factory=dict)
    performance: Dict[str, Any] = field(default_factory=dict)
    bussola: Dict[str, Any] = field(default_factory=dict)
    ocai: Dict[str, Any] = field(default_factory=dict)
    cross_insights: Dict[str, Any] = field(default_factory=dict)

    # MI DOCUMENT ---------------------------------------------------------------
    mi_document: Optional[Dict[str, Any]] = None

    # AUDITORIA -----------------------------------------------------------------
    audit_log: Optional[Dict[str, Any]] = None

    # -------------------------------------------------------------------------
    # VALIDAÇÃO FINAL DA ENTIDADE COMPLETA
    # -------------------------------------------------------------------------

    def __post_init__(self):
        # validar id de usuário
        require(isinstance(self.user_id, str) and len(self.user_id) > 0,
                "user_id deve ser string não vazia.")

        # validar sessão
        require(isinstance(self.session_id, str) and len(self.session_id) > 0,
                "session_id deve ser string não vazia.")

        # validar timestamp
        require(isinstance(self.timestamp, datetime.datetime),
                "timestamp inválido.")

        # validar blocos obrigatórios
        for name in [
            "big5", "teique", "dass21", "esquemas",
            "performance", "bussola", "ocai", "cross_insights"
        ]:
            block = getattr(self, name)
            require(isinstance(block, dict),
                    f"O bloco {name} deve ser um dicionário.")
            require(len(block) > 0,
                    f"O bloco {name} está vazio — esperado resultado completo.")

    # -------------------------------------------------------------------------
    # METADADOS E ESTRUTURA FINAL
    # -------------------------------------------------------------------------

    def summary(self) -> Dict[str, Any]:
        """
        Retorna visão resumida e consolidada.
        """
        return {
            "user_id": self.user_id,
            "session_id": self.session_id,
            "timestamp": self.timestamp.isoformat(),

            "big5": self.big5.get("results", {}),
            "teique": self.teique.get("results", {}),
            "dass21": self.dass21.get("results", {}),
            "esquemas": self.esquemas.get("domains", {}),
            "performance": self.performance.get("results", {}),
            "bussola": self.bussola.get("results", {}),
            "ocai": self.ocai.get("profiles", {}),
            "insights": self.cross_insights.get("insights", []),

            "insight_count": self.cross_insights.get("count", 0)
        }

    # -------------------------------------------------------------------------
    # SERIALIZAÇÃO FINAL — PADRÃO PARA O MI FORMATTER E RELATÓRIOS
    # -------------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """
        Converte todo o pacote MindScan para dict final.
        Totalmente determinístico e pronto para JSON/MI.
        """
        return {
            "user_id": self.user_id,
            "session_id": self.session_id,
            "timestamp": self.timestamp.isoformat(),

            "modules": {
                "big5": self.big5,
                "teique": self.teique,
                "dass21": self.dass21,
                "esquemas": self.esquemas,
                "performance": self.performance,
                "bussola": self.bussola,
                "ocai": self.ocai,
                "cross_insights": self.cross_insights
            },

            "mi_document": self.mi_document,
            "audit_log": self.audit_log
        }
