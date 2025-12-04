#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
performance_governor.py — Adaptive Performance Governor (SynMind v2.0)
Autor: Leo Vinci (Inovexa)
-------------------------------------------------------------------------------
Função:
    - Ajustar dinamicamente o modo TURBO de acordo com CPU/RAM
    - Integrado com ResourceMonitor v2.0
    - Telemetria avançada para registrar eventos de carga
    - Operação segura (sem eval, sem riscos)
"""

import json
import time
from typing import Optional


class PerformanceGovernor:

    def __init__(
        self,
        logger=None,
        monitor=None,         # ResourceMonitor v2.0
        telemetry=None,       # TelemetryAdvanced v2.0
        cpu_limit_high: float = 85.0,   # acima disso → desligar turbo
        cpu_limit_low: float = 45.0,    # abaixo disso → ativar turbo
        ram_limit_mb: float = 1500.0,   # limite de carga máxima
        cool_down: float = 1.5          # intervalo entre avaliações
    ):
        self.logger = logger
        self.monitor = monitor
        self.telemetry = telemetry

        self.cpu_limit_high = cpu_limit_high
        self.cpu_limit_low = cpu_limit_low
        self.ram_limit_mb = ram_limit_mb
        self.cool_down = cool_down

        # Estado
        self.turbo_enabled = False
        self.last_eval = 0.0

        if self.logger:
            self.logger.info(
                f"PerformanceGovernor v2.0 iniciado | "
                f"CPU_HIGH={cpu_limit_high}% CPU_LOW={cpu_limit_low}% "
                f"RAM_LIMIT={ram_limit_mb}MB"
            )

    # ----------------------------------------------------------------------
    # LER CPU de maneira segura (sem eval)
    # ----------------------------------------------------------------------
    def _ler_cpu(self) -> float:
        """
        Tenta ler a última linha JSONL gravada pelo ResourceMonitor v2.0.
        Sem eval, sem riscos.
        """
        try:
            with open(self.monitor.output_file, "r", encoding="utf-8") as f:
                for line in reversed(f.readlines()):
                    try:
                        data = json.loads(line.strip())
                        return float(data.get("cpu_percent", 0.0))
                    except json.JSONDecodeError:
                        continue
        except Exception:
            pass

        return 0.0

    # ----------------------------------------------------------------------
    # AVALIAÇÃO DE CARGA
    # ----------------------------------------------------------------------
    def avaliar(self) -> bool:
        agora = time.time()
        if agora - self.last_eval < self.cool_down:
            return self.turbo_enabled

        self.last_eval = agora

        if not self.monitor:
            return self.turbo_enabled

        cpu = self._ler_cpu()
        ram = getattr(self.monitor, "peak_memory_mb", 0.0)

        if self.logger:
            self.logger.info(f"[Governor] CPU={cpu:.2f}% RAM={ram:.1f}MB")

        # Registrar evento de carga
        if self.telemetry:
            self.telemetry.registrar_carga(cpu, ram)

        # Regra 1 — carga alta
        if cpu > self.cpu_limit_high or ram > self.ram_limit_mb:
            if self.turbo_enabled:
                self.turbo_enabled = False
                if self.logger:
                    self.logger.warn("[Governor] TURBO desativado (carga alta).")
                if self.telemetry:
                    self.telemetry.registrar_evento("turbo_desativado_carga_alta")
            return False

        # Regra 2 — carga baixa
        if cpu < self.cpu_limit_low:
            if not self.turbo_enabled:
                self.turbo_enabled = True
                if self.logger:
                    self.logger.info("[Governor] TURBO ativado (carga baixa).")
                if self.telemetry:
                    self.telemetry.registrar_evento("turbo_ativado_carga_baixa")
            return True

        # Regra 3 — manter estado
        if self.logger:
            self.logger.info("[Governor] Mantendo estado atual de TURBO.")

        return self.turbo_enabled

    # ----------------------------------------------------------------------
    # INTERFACE PÚBLICA
    # ----------------------------------------------------------------------
    def turbo_ativado(self) -> bool:
        return self.turbo_enabled
