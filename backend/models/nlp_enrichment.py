# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\nlp_enrichment.py
# Última atualização: 2025-12-11T09:59:20.964461

# nlp_enrichment.py
# MindScan Rebuild – Modelo de Enriquecimento NLP
# Versão Definitiva • Estrutura Avançada Pydantic-Style
# Autor: Leo Vinci — IA Supervisora Inovexa
# -------------------------------------------------------------------------
# Este módulo define a estrutura final do bloco de enriquecimento NLP,
# utilizado para:
#   - Expandir insights psicométricos em linguagem natural
#   - Adicionar marcadores descritivos ao relatório
#   - Suportar o MI Formatter e o Diagnostic Engine
#   - Padronizar outputs textuais de alta relevância
# -------------------------------------------------------------------------

from dataclasses import dataclass, field
from typing import List, Dict, Any
import datetime


class ValidationError(Exception):
    pass


def require(condition: bool, message: str):
    if not condition:
        raise ValidationError(message)


@dataclass
class NLPEnrichmentBlock:
    """
    Bloco de enriquecimento textual.
    Contém frases, análises breves e insights linguísticos
    derivados dos módulos principais.
    """

    statements: List[str]                 # frases finais enriquecidas
    tags: List[str] = field(default_factory=list)     # categorias semânticas
    metadata: Dict[str, Any] = field(default_factory=dict)
    generated_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())

    def __post_init__(self):
        require(isinstance(self.statements, list) and len(self.statements) > 0,
                "statements deve ser uma lista de frases não vazia.")

        for s in self.statements:
            require(isinstance(s, str) and len(s) > 0,
                    "Cada item em statements deve ser uma string não vazia.")

        require(isinstance(self.tags, list),
                "tags deve ser uma lista.")

        for t in self.tags:
            require(isinstance(t, str),
                    "Cada tag deve ser string.")

        require(isinstance(self.metadata, dict),
                "metadata deve ser um dicionário.")

        require(isinstance(self.generated_at, str) and len(self.generated_at) > 0,
                "generated_at inválido.")

    # ---------------------------------------------------------
    # Conversões finais
    # ---------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        return {
            "statements": self.statements,
            "tags": self.tags,
            "metadata": self.metadata,
            "generated_at": self.generated_at
        }

    def summary(self) -> Dict[str, Any]:
        return {
            "count": len(self.statements),
            "first": self.statements[0] if self.statements else None
        }
