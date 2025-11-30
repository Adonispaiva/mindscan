#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
performance_governor.py — Adaptive Performance Governor · Inovexa
------------------------------------------------------------------

Objetivo:
- Controlar dinamicamente o modo TURBO (paralelização).
- Monitorar CPU/RAM via ResourceMonitor.
- Ajustar agressividade do pipeline conforme a carga do sistema.
- Evitar degradação e sobrecarga em servidores.
- Otimizar performance automaticamente.

Funciona com:
- PDFBuilder v36 (otimizado)
- SectionEngine v39 (paralelo inteligente)
- AsyncPipeline v40
- ResourceMonitor v38
- Telemetria Avançada
- Logger corporativo

Estratégia:
- Coleta de CPU/RAM em tempo real.
- Ajustes de política conforme thresholds.
- Força Modo Seguro quando necessário.
- Habilita TURBO+ quando seguro.
"""

import time


class PerformanceGovernor:

    def __init__(
        self,
        logger=None,
        monitor=None,         # ResourceMonitor
        cpu_limit_high=85.0,  # acima disso, desligar TURBO
        cpu_limit_low=45.0,   # abaixo disso, ativar TURBO
        ram_limit_mb=1500.0,  # limite recomendado
        cool_down=2.0          # segundos antes de reavaliar
    ):
        self.logger = logger
        self.monitor = monitor
        self.cpu_limit_high = cpu_limit_high
        self.cpu_limit_low = cpu_limit_low
        self.ram_limit_mb = ram_limit_mb
        self.cool_down = cool_down

        # Estado interno
        self.turbo_enabled = False
        self.last_eval = 0.0

        if self.logger:
            self.logger.info(
                f"PerformanceGovernor iniciado. CPU_HIGH={cpu_limit_high} "
                f"CPU_LOW={cpu_limit_low} RAM_LIMIT={ram_limit_mb}MB"
            )

    # ============================================================
    # Avaliar estado atual do sistema
    # ============================================================
    def avaliar(self):
        """
        Coleta CPU/RAM do monitor e ajusta estado interno.
        Chamado em intervalos seguros pelo PDFBuilder/AsyncPipeline.
        """

        agora = time.time()
        if agora - self.last_eval < self.cool_down:
            return self.turbo_enabled

        self.last_eval = agora

        if not self.monitor:
            # Sem monitor, assume modo normal
            return self.turbo_enabled

        # Última leitura do ResourceMonitor
        # O monitor salva JSONL, mas também mantém pico de RAM.
        cpu = self._ler_cpu()
        ram = self.monitor.peak_memory_mb

        if self.logger:
            self.logger.info(
                f"[Governor] Avaliação: CPU={cpu:.2f}% RAM={ram:.1f}MB"
            )

        # Regra 1 — Carga muito alta = desliga TURBO imediatamente
        if cpu > self.cpu_limit_high or ram > self.ram_limit_mb:
            if self.turbo_enabled:
                self.turbo_enabled = False
                if self.logger:
                    self.logger.warn("[Governor] TURBO desativado por carga alta.")
            return False

        # Regra 2 — Carga baixa = ativa TURBO automaticamente
        if cpu < self.cpu_limit_low:
            if not self.turbo_enabled:
                self.turbo_enabled = True
                if self.logger:
                    self.logger.info("[Governor] TURBO ativado (carga baixa).")
            return True

        # Regra 3 — Região neutra = mantém estado atual
        if self.logger:
            self.logger.info("[Governor] Mantendo estado atual de TURBO.")

        return self.turbo_enabled

    # ============================================================
    # Leitura segura da última CPU registrada pelo monitor
    # ============================================================
    def _ler_cpu(self):
        """
        Usa o JSONL mais recente gerado pelo ResourceMonitor para
        descobrir a CPU atual. Caso não seja possível, retorna 0%.
        """
        try:
            with open(self.monitor.output_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
            if not lines:
                return 0.0
            last = lines[-1]
            data = eval(last) if last.startswith("{") else {}
            return data.get("cpu_percent", 0.0)
        except Exception:
            return 0.0

    # ============================================================
    # Interface pública
    # ============================================================
    def turbo_ativado(self) -> bool:
        """Retorna o estado atual do TURBO."""
        return self.turbo_enabled
42
