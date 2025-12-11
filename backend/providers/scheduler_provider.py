# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\providers\scheduler_provider.py
# Última atualização: 2025-12-11T09:59:21.073776

# scheduler_provider.py
# MindScan / SynMind 2025 – Agendador Definitivo, Estável, Completo

import threading
import time
import logging
from datetime import datetime, timedelta
from typing import Callable, Optional


class ScheduledTask:
    """
    Representa uma tarefa agendada:
        - função
        - intervalo
        - modo (repetição ou execução única)
    """
    def __init__(
        self,
        func: Callable,
        interval_seconds: int,
        repeat: bool = True,
        start_at: Optional[datetime] = None,
        name: Optional[str] = None
    ):
        self.func = func
        self.interval_seconds = interval_seconds
        self.repeat = repeat
        self.start_at = start_at or datetime.now()
        self.name = name or f"task_{int(time.time())}"
        self.next_run = self.start_at


class SchedulerProvider:
    """
    Agendador profissional SynMind:
        - múltiplas tarefas simultâneas
        - execução com threads separadas
        - start/stop seguro
        - controle interno
        - logs completos
        - tratamento de exceções
        - modo repetição ou execução única
    """

    def __init__(self, tick_interval=1.0):
        self.tick_interval = tick_interval
        self.tasks = []
        self.running = False

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [Scheduler] %(levelname)s: %(message)s"
        )

    # ------------------------------
    # API PUBLICA
    # ------------------------------

    def add_task(
        self,
        func: Callable,
        interval_seconds: int,
        repeat: bool = True,
        start_at: Optional[datetime] = None,
        name: Optional[str] = None
    ):
        """
        Adiciona uma tarefa ao scheduler.
        """
        task = ScheduledTask(
            func=func,
            interval_seconds=interval_seconds,
            repeat=repeat,
            start_at=start_at,
            name=name
        )
        self.tasks.append(task)

        logging.info(f"Tarefa '{task.name}' adicionada (intervalo: {interval_seconds}s).")

    def start(self):
        if self.running:
            return

        self.running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        logging.info("Scheduler iniciado.")

    def stop(self):
        if not self.running:
            return

        self.running = False
        self._thread.join()
        logging.info("Scheduler finalizado com segurança.")

    # ------------------------------
    # LOOP PRINCIPAL
    # ------------------------------

    def _run_loop(self):
        while self.running:
            now = datetime.now()

            for task in list(self.tasks):
                if now >= task.next_run:
                    self._execute_task(task)

                    if task.repeat:
                        task.next_run = now + timedelta(seconds=task.interval_seconds)
                    else:
                        self.tasks.remove(task)

            time.sleep(self.tick_interval)

    # ------------------------------
    # EXECUÇÃO INTERNA
    # ------------------------------

    def _execute_task(self, task: ScheduledTask):
        try:
            logging.info(f"Executando tarefa: {task.name}")
            threading.Thread(
                target=task.func,
                daemon=True
            ).start()

        except Exception as e:
            logging.error(f"Erro ao executar tarefa '{task.name}': {e}")
