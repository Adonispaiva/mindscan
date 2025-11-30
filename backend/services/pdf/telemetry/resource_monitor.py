#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
resource_monitor.py — Monitoramento de CPU e RAM do MindScan PDF Engine
-----------------------------------------------------------------------

Recursos:
- Coleta periódica de CPU %
- Coleta periódica de RAM (MB)
- Pico de memória por sessão
- Thread autônoma (não bloqueia o PDF)
- Registro JSONL contínuo
- Integração com Logger e Telemetria Avançada
- Compatível com Linux, Windows e Mac

Dependência:
    psutil (necessário instalar manualmente: pip install psutil)

Este módulo NÃO interfere na pipeline.
Apenas observa.
"""

import json
import threading
import time
from datetime import datetime
from pathlib import Path

try:
    import psutil
except ImportError:
    raise RuntimeError("psutil é necessário para o monitoramento (pip install psutil).")


class ResourceMonitor:

    def __init__(self, logs_dir: Path, logger=None, interval: float = 0.5):
        """
        logs_dir: pasta onde o log JSONL será salvo
        interval: intervalo de coleta em segundos
        """
        self.logs_dir = Path(logs_dir)
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        self.logger = logger
        self.interval = interval
        self._stop_flag = False
        self._thread = None
        self._session_id = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

        self.output_file = self.logs_dir / "mindscan_resource_monitor.jsonl"

        if self.logger:
            self.logger.info(
                f"ResourceMonitor iniciado. Intervalo: {self.interval}s."
            )

        # Armazenar pico de memória
        self.peak_memory_mb = 0.0

    # ============================================================
    # Thread principal (loop de coleta)
    # ============================================================
    def _loop(self):
        process = psutil.Process()

        while not self._stop_flag:
            try:
                cpu = psutil.cpu_percent(interval=None)
                mem_info = process.memory_info()
                mem_mb = mem_info.rss / (1024 * 1024)

                # Atualizar pico
                if mem_mb > self.peak_memory_mb:
                    self.peak_memory_mb = mem_mb

                entrada = {
                    "session_id": self._session_id,
                    "timestamp": datetime.utcnow().isoformat(),
                    "cpu_percent": cpu,
                    "memory_mb": mem_mb,
                    "peak_memory_mb": self.peak_memory_mb,
                }

                with self.output_file.open("a", encoding="utf-8") as f:
                    f.write(json.dumps(entrada) + "\n")

            except Exception as e:
                if self.logger:
                    self.logger.evento_erro("ResourceMonitor", e)

            time.sleep(self.interval)

    # ============================================================
    # Controle
    # ============================================================
    def start(self):
        if self._thread:
            return  # já iniciado

        self._stop_flag = False
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

        if self.logger:
            self.logger.info("ResourceMonitor: coleta iniciada.")

    def stop(self):
        self._stop_flag = True
        if self._thread:
            self._thread.join(timeout=2.0)

        if self.logger:
            self.logger.info(
                f"ResourceMonitor: coleta finalizada. Pico de memória: {self.peak_memory_mb:.2f} MB."
            )

    # ============================================================
    # Uso com contexto
    # ============================================================
    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
