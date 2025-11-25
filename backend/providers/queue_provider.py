# queue_provider.py
# MindScan / SynMind 2025 – Final, Definitivo, Completo

import threading
import queue
import time
import logging
from typing import Any, Callable, Optional

class QueueJob:
    """
    Representa um job na fila com prioridade,
    função, argumentos e tentativas de execução.
    """
    def __init__(
        self,
        func: Callable,
        args: Optional[tuple] = None,
        kwargs: Optional[dict] = None,
        priority: int = 10,
        retries: int = 3
    ):
        self.func = func
        self.args = args or ()
        self.kwargs = kwargs or {}
        self.priority = priority
        self.retries = retries


class QueueProvider:
    """
    Provedor de fila totalmente funcional, definitivo, thread-safe,
    com prioridade, retries, shutdown controlado e métricas internas.
    """

    def __init__(self):
        self.queue = queue.PriorityQueue()
        self.running = True
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)

        # Métricas internas
        self.total_processed = 0
        self.total_failed = 0
        self.total_enqueued = 0

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [QueueProvider] %(levelname)s: %(message)s"
        )

        self.worker_thread.start()
        logging.info("QueueProvider inicializado com sucesso.")

    # -------------------------------
    # API PÚBLICA
    # -------------------------------

    def enqueue(
        self,
        func: Callable,
        args: Optional[tuple] = None,
        kwargs: Optional[dict] = None,
        priority: int = 10,
        retries: int = 3
    ):
        job = QueueJob(func, args, kwargs, priority, retries)
        self.queue.put((priority, time.time(), job))
        self.total_enqueued += 1
        logging.info(f"Job adicionado à fila (prioridade: {priority}).")

    def stop(self):
        """
        Finaliza o worker de maneira segura.
        """
        logging.info("Solicitado desligamento seguro da fila...")
        self.running = False
        self.worker_thread.join()
        logging.info("QueueProvider finalizado.")

    # -------------------------------
    # WORKER INTERNO
    # -------------------------------

    def _worker(self):
        while self.running:
            try:
                priority, _, job = self.queue.get(timeout=0.5)

                success = self._execute_job(job)

                if success:
                    self.total_processed += 1
                else:
                    self.total_failed += 1

                self.queue.task_done()

            except queue.Empty:
                continue
            except Exception as e:
                logging.error(f"Erro inesperado no worker: {e}")

    def _execute_job(self, job: QueueJob) -> bool:
        """
        Executa um job com tratamento completo de falhas e retries.
        """
        attempt = 0

        while attempt < job.retries:
            try:
                job.func(*job.args, **job.kwargs)
                logging.info("Job executado com sucesso.")
                return True

            except Exception as e:
                attempt += 1
                logging.warning(
                    f"Falha ao executar job (tentativa {attempt}/{job.retries}): {e}"
                )
                time.sleep(0.5)

        logging.error("Job falhou após todas as tentativas.")
        return False
