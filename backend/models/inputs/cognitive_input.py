# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\inputs\cognitive_input.py
# Última atualização: 2025-12-11T09:59:20.980027

from __future__ import annotations

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class CognitiveTaskScore(BaseModel):
    """
    Resultado de uma tarefa cognitiva específica (memória, atenção, raciocínio, etc.).
    """

    task_id: str = Field(
        ...,
        description="Identificador da tarefa ou subteste cognitivo.",
    )
    raw_score: float = Field(
        ...,
        description="Score bruto obtido na tarefa.",
    )
    normalized_score: Optional[float] = Field(
        default=None,
        description="Score normalizado em relação às normas internas do MindScan/SynMind.",
    )
    unit: Optional[str] = Field(
        default=None,
        description="Unidade do score (tempo, acertos, índice composto, etc.).",
    )


class CognitiveInput(BaseModel):
    """
    Payload de entrada para dados cognitivos no MindScan.

    Pode englobar:
    - resultados de baterias cognitivas externas;
    - tarefas proprietárias digitais da SynMind;
    - índices compostos calculados por motores externos.
    """

    candidate_id: str = Field(
        ...,
        description="Identificador único do candidato no ecossistema SynMind.",
    )
    session_id: Optional[str] = Field(
        default=None,
        description="Sessão/rodada de coleta dos dados cognitivos.",
    )
    tasks: List[CognitiveTaskScore] = Field(
        default_factory=list,
        description="Lista de tarefas cognitivas avaliadas.",
    )
    global_index: Optional[float] = Field(
        default=None,
        description="Índice global cognitivo (quando calculado externamente).",
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Metadados auxiliares (protocolo, instrumento, versão, dispositivo, etc.).",
    )

    def to_algorithm_payload(self) -> Dict[str, Any]:
        """
        Converte o input em um dicionário pronto para uso por:

        - módulos de performance e perfil cognitivo;
        - pipelines de cruzamento (ex.: Big5 x cognição);
        - geradores de insights no relatório final.
        """
        return self.dict()
