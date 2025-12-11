# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\core\base_service.py
# Última atualização: 2025-12-11T09:59:21.120711

# D:\mindscan\backend\services\core\base_service.py
# --------------------------------------------------
# Classe-mãe de todos os serviços corporativos do MindScan
# Autor: Leo Vinci — Inovexa Software

from typing import Any, Dict
from datetime import datetime

from backend.core.runtime_kernel import RuntimeKernel


class BaseService:
    """
    Classe-base que padroniza o comportamento de todos os serviços
    corporativos do MindScan, garantindo:

    - logging unificado
    - trilha de execução para auditoria
    - metadados consistentes
    - acesso centralizado ao RuntimeKernel
    - validação estrutural de entrada/saída
    """

    def __init__(self, service_name: str):
        self.service_name = service_name
        self.kernel = RuntimeKernel()

    # ----------------------------------------------------------------------
    # LOGGING & AUDITORIA
    # ----------------------------------------------------------------------

    def _log(self, message: str) -> None:
        """
        Registra logs estruturados para auditoria interna do sistema.
        """
        timestamp = datetime.utcnow().isoformat()
        entry = f"[{timestamp}] [{self.service_name}] {message}"
        self.kernel.register_service_log(self.service_name, entry)

    # ----------------------------------------------------------------------
    # VALIDAÇÕES E METADADOS
    # ----------------------------------------------------------------------

    def _validate_input(self, data: Dict[str, Any]) -> None:
        """
        Validação defensiva para evitar inconsistências no pipeline.
        """
        if not isinstance(data, dict):
            raise TypeError(
                f"Entrada inválida para {self.service_name}: esperado dict, recebido {type(data)}"
            )

    def _package_metadata(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Acrescenta metadados padronizados a qualquer retorno.
        """
        return {
            "service": self.service_name,
            "timestamp": datetime.utcnow().isoformat(),
            "payload": payload,
            "runtime": self.kernel.get_runtime_metadata(),
        }

    # ----------------------------------------------------------------------
    # MÉTODO PADRÃO DE EXECUÇÃO
    # ----------------------------------------------------------------------

    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Método genérico sobrescrito por cada serviço especializado.
        """
        self._log("Iniciando execução.")
        self._validate_input(data)

        raise NotImplementedError(
            f"O serviço '{self.service_name}' deve implementar o método execute()."
        )
