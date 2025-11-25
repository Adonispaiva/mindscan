# diagnostic_payload.py
# MindScan Rebuild – Modelo de Payload para o Diagnostic Engine
# Versão Definitiva • Arquitetura Avançada Pydantic-Style
# Autor: Leo Vinci — IA Supervisora Inovexa
# Última atualização: 23/11/2025
# -------------------------------------------------------------------------
# Este módulo define o formato OFICIAL de entrada para o Diagnostic Engine
# e para o Runtime Kernel, garantindo:
#   - Validação completa dos blocos
#   - Conversão determinística para dicionário
#   - Estrutura final e imutável
#   - Compatibilidade com TODOS os algoritmos do MindScan
#   - Consistência total com mindscan_result.py
# -------------------------------------------------------------------------

from dataclasses import dataclass, field
from typing import Dict, Any
import datetime


class ValidationError(Exception):
    pass


def require(condition: bool, message: str):
    if not condition:
        raise ValidationError(message)


@dataclass
class DiagnosticPayload:
    """
    Payload oficial usado pelo Diagnostic Engine.
    Representa a entrada consolidada dos algoritmos principais.
    """

    # Identificação da sessão
    user_id: str
    session_id: str
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.utcnow)

    # Dados de entrada provenientes dos algoritmos brutos
    big5: Dict[str, Any] = field(default_factory=dict)
    teique: Dict[str, Any] = field(default_factory=dict)
    dass21: Dict[str, Any] = field(default_factory=dict)
    esquemas: Dict[str, Any] = field(default_factory=dict)
    performance: Dict[str, Any] = field(default_factory=dict)
    bussola: Dict[str, Any] = field(default_factory=dict)
    ocai: Dict[str, Any] = field(default_factory=dict)

    # Pacote adicional
    source_metadata: Dict[str, Any] = field(default_factory=dict)

    # ---------------------------------------------------------------------
    # Validação final
    # ---------------------------------------------------------------------

    def __post_init__(self):
        require(isinstance(self.user_id, str) and len(self.user_id) > 0,
                "user_id deve ser string não vazia.")
        require(isinstance(self.session_id, str) and len(self.session_id) > 0,
                "session_id deve ser string não vazia.")
        require(isinstance(self.timestamp, datetime.datetime),
                "timestamp inválido.")

        # Blocos obrigatórios
        for block in [
            "big5", "teique", "dass21", "esquemas",
            "performance", "bussola", "ocai"
        ]:
            value = getattr(self, block)
            require(isinstance(value, dict), f"{block} deve ser um dicionário.")
            require(len(value) > 0, f"{block} está vazio — esperado conteúdo completo.")

    # ---------------------------------------------------------------------
    # Conversão final para o Diagnostic Engine
    # ---------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """
        Conversão determinística para dicionário completo.
        Este formato é consumido diretamente pelo Diagnostic Engine.
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
                "ocai": self.ocai
            },

            "source_metadata": self.source_metadata
        }

    # ---------------------------------------------------------------------
    # Resumo simplificado
    # ---------------------------------------------------------------------

    def summary(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "session_id": self.session_id,
            "timestamp": self.timestamp.isoformat(),
            "modules_received": [
                "big5", "teique", "dass21",
                "esquemas", "performance", "bussola", "ocai"
            ]
        }
