# ============================================================
# MindScan — Runtime Kernel (CORE)
# ============================================================
# O Runtime Kernel é a camada responsável por gerenciar o
# estado de execução, permitir controle transacional,
# registrar falhas internas e manter o "Context Object"
# utilizado pelo Engine.
#
# Versão completa, maximizada e definitiva.
# ============================================================

from typing import Optional, Dict, Any
from datetime import datetime


class KernelContext:
    """
    Objeto de contexto utilizado por todos os módulos CORE.
    Guarda:
    - ID do teste
    - Fase atual
    - Timestamp de início e fim
    - Erros capturados
    - Metadados do pipeline
    """

    def __init__(self, test_id: int, stage: str = "initializing"):
        self.test_id: int = test_id
        self.stage: str = stage
        self.error: Optional[str] = None
        self.started_at: datetime = datetime.utcnow()
        self.finished_at: Optional[datetime] = None
        self.metadata: Dict[str, Any] = {
            "kernel_version": "2.3",
            "engine_protocol": "SynMind-Kernel",
            "initialized_from": "runtime_kernel"
        }

    # ------------------------------------------------------------
    # Atualização de estágio
    # ------------------------------------------------------------
    def update_stage(self, new_stage: str):
        self.stage = new_stage
        self.metadata["last_stage_update"] = datetime.utcnow().isoformat()

    # ------------------------------------------------------------
    # Registrar erro
    # ------------------------------------------------------------
    def register_error(self, message: str):
        self.error = message
        self.metadata["last_error"] = message
        self.finished_at = datetime.utcnow()

    # ------------------------------------------------------------
    # Marcar conclusão
    # ------------------------------------------------------------
    def complete(self):
        self.finished_at = datetime.utcnow()
        self.metadata["completed"] = True

    # ------------------------------------------------------------
    # Representação
    # ------------------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        return {
            "test_id": self.test_id,
            "stage": self.stage,
            "error": self.error,
            "started_at": self.started_at.isoformat(),
            "finished_at": self.finished_at.isoformat() if self.finished_at else None,
            "metadata": self.metadata,
        }


class RuntimeKernel:
    """
    Runtime Kernel do MindScan.
    Controla:
    - Abertura e fechamento de execução
    - Registro de estado
    - Tratamento de erros de alto nível
    - Integração com o Engine
    """

    def __init__(self):
        pass

    # ------------------------------------------------------------
    # EXECUTAR UMA FUNÇÃO COM CONTEXTO
    # ------------------------------------------------------------
    async def execute_with_context(self, test_id: int, func, *args, **kwargs):
        """
        Executa uma função dentro de um KernelContext de segurança.
        """

        ctx = KernelContext(test_id=test_id)

        try:
            ctx.update_stage("running")
            result = await func(ctx, *args, **kwargs)
            ctx.update_stage("finishing")
            ctx.complete()
            return {
                "result": result,
                "context": ctx.to_dict()
            }

        except Exception as e:
            ctx.register_error(str(e))
            return {
                "error": str(e),
                "context": ctx.to_dict()
            }
