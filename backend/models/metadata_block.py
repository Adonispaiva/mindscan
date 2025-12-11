# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\metadata_block.py
# Última atualização: 2025-12-11T09:59:20.964461

# metadata_block.py
# MindScan Rebuild – Bloco Global de Metadados
# Versão Definitiva • Estrutura Avançada Pydantic-Style
# Autor: Leo Vinci — IA Supervisora Inovexa
# -------------------------------------------------------------------------
# Este arquivo define o bloco de metadados finais do MindScan.
# Inclui:
#   - versão do build
#   - arquitetura
#   - carimbo de integridade
#   - registro de origem dos dados
#   - trilha de compatibilidade
#   - informações de compliance
#
# Estrutura final e congelada.
# -------------------------------------------------------------------------

from dataclasses import dataclass, field
from typing import Dict, Any
import datetime


class ValidationError(Exception):
    pass


def require(condition: bool, msg: str):
    if not condition:
        raise ValidationError(msg)


@dataclass
class MetadataBlock:
    """
    Bloco definitivo de metadados globais usados em:
        - mindscan_result.py
        - mi_document_package.py
        - reporting
        - diagnostic engine
    """

    version: str                               # versão do MindScan Build
    architecture: str                           # arquitetura ativa
    integrity_hash: str                         # hash de integridade do pacote
    source: Dict[str, Any]                      # origem dos dados da sessão
    compliance: Dict[str, Any]                  # bloco de compliance e segurança
    generated_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())

    def __post_init__(self):

        require(isinstance(self.version, str) and len(self.version) > 0,
                "version deve ser string não vazia.")

        require(isinstance(self.architecture, str) and len(self.architecture) > 0,
                "architecture deve ser string válida.")

        require(isinstance(self.integrity_hash, str) and len(self.integrity_hash) > 0,
                "integrity_hash deve ser string não vazia.")

        require(isinstance(self.source, dict),
                "source deve ser dicionário.")

        require("system" in self.source and "origin" in self.source,
                "source deve conter os campos {system, origin}.")

        require(isinstance(self.compliance, dict),
                "compliance deve ser dicionário.")
        require("privacy" in self.compliance and "security" in self.compliance,
                "compliance deve conter os campos {privacy, security}.")

        require(isinstance(self.generated_at, str),
                "generated_at deve ser string válida.")

    # ---------------------------------------------------------------------
    # Conversão final
    # ---------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "architecture": self.architecture,
            "integrity_hash": self.integrity_hash,
            "source": self.source,
            "compliance": self.compliance,
            "generated_at": self.generated_at
        }

    def summary(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "architecture": self.architecture,
            "origin": self.source.get("origin", None)
        }
