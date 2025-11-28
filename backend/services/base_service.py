"""
MindScan Backend — Base Service
Diretor Técnico: Leo Vinci

Este arquivo define a classe-base para todos os serviços
internos do backend MindScan. Serviços futuros devem
herdar desta classe para garantir padronização total.
"""

from datetime import datetime
from pathlib import Path


# Diretórios e logs isolados
ROOT = Path(__file__).resolve().parent
RUNTIME = ROOT / "runtime"
RUNTIME.mkdir(parents=True, exist_ok=True)

LOGFILE = RUNTIME / "base_service.log"


def slog(msg: str):
    """Log interno do BaseService."""
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[BaseService {ts}] {msg}"
    print(line)

    with LOGFILE.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


class BaseService:
    """
    Classe base para qualquer serviço do MindScan.
    Serviços devem herdar e sobrescrever:
        - setup()
        - run()
        - shutdown()
    """

    name = "BaseService"

    def __init__(self):
        slog(f"Instanciando serviço: {self.name}")

    # ------------------------------------------------------------------
    # MÉTODOS DO CICLO DE VIDA
    # ------------------------------------------------------------------
    def setup(self):
        """Inicialização opcional antes de run()."""
        slog(f"{self.name}.setup() chamado.")

    def run(self):
        """
        Método principal do serviço.
        DEVE ser sobrescrito pelas subclasses.
        """
        raise NotImplementedError(
            f"{self.name}.run() precisa ser implementado pela subclasse."
        )

    def shutdown(self):
        """Procedimentos de finalização."""
        slog(f"{self.name}.shutdown() chamado.")

    # ------------------------------------------------------------------
    # EXECUTOR PADRÃO
    # ------------------------------------------------------------------
    def execute(self):
        """
        Executa o ciclo completo padrão do serviço:
        setup() → run() → shutdown()
        """
        slog(f"Executando serviço: {self.name}")
        self.setup()

        try:
            self.run()
        except Exception as e:
            slog(f"ERRO em {self.name}.run(): {e}")
            raise

        self.shutdown()
        slog(f"Serviço {self.name} concluído com sucesso.")
