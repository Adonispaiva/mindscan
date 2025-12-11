# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\telemetry\telemetry_advanced.py
# Última atualização: 2025-12-11T09:59:21.276887

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
telemetry_advanced.py — Telemetria Avançada do MindScan PDF Engine
-------------------------------------------------------------------

Este módulo registra métricas detalhadas:
- tempo total de geração do PDF
- tempo por seção
- tamanho final do PDF
- renderer utilizado e performance
- velocidade de geração de HTML
- indicadores para dashboards futuros

Compatível com:
- PDFBuilder
- CLI
- Renderers
- Logger padrão (logger.py)
"""

from pathlib import Path
from datetime import datetime
import time
import json


class TelemetryAdvanced:

    def __init__(self, logs_dir: Path, logger=None):
        self.logs_dir = Path(logs_dir)
        self.logs_dir.mkdir(exist_ok=True, parents=True)

        self.logger = logger
        self._start_times = {}
        self._sections_timings = {}
        self._session_id = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

        self.telemetry_file = self.logs_dir / "mindscan_telemetry_advanced.jsonl"

        if self.logger:
            self.logger.info("TelemetryAdvanced inicializada.")

    # ============================================================
    # Controle de tempo
    # ============================================================
    def iniciar(self, nome: str):
        """Inicia medição de tempo de um bloco."""
        self._start_times[nome] = time.perf_counter()
        if self.logger:
            self.logger.info(f"Telemetria: início '{nome}'")

    def finalizar(self, nome: str):
        """Finaliza medição de tempo e registra duração."""
        if nome not in self._start_times:
            return 0.0

        duracao = time.perf_counter() - self._start_times[nome]
        self._sections_timings[nome] = duracao

        if self.logger:
            self.logger.info(f"Telemetria: fim '{nome}' – {duracao:.4f}s")

        return duracao

    # ============================================================
    # Tamanho final do PDF
    # ============================================================
    def registrar_tamanho_pdf(self, output_path: Path):
        try:
            tamanho = output_path.stat().st_size
        except FileNotFoundError:
            tamanho = 0

        if self.logger:
            self.logger.info(f"Tamanho final do PDF: {tamanho} bytes")

        self._sections_timings["tamanho_pdf_bytes"] = tamanho

    # ============================================================
    # Renderer utilizado
    # ============================================================
    def registrar_renderer(self, nome: str):
        self._sections_timings["renderer"] = nome
        if self.logger:
            self.logger.info(f"Telemetria: renderer '{nome}' registrado.")

    # ============================================================
    # Exportar telemetria (JSONL)
    # ============================================================
    def exportar(self):
        entrada = {
            "session_id": self._session_id,
            "timestamp": datetime.utcnow().isoformat(),
            "metrics": self._sections_timings,
        }

        with self.telemetry_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entrada, ensure_ascii=False) + "\n")

        if self.logger:
            self.logger.info("Telemetria avançada exportada com sucesso.")

    # ============================================================
    # Utilitário para uso em blocos
    # ============================================================
    def bloco(self, nome):
        """Context manager para medir automaticamente o tempo."""
        class _Bloco:
            def __init__(self, parent, nome):
                self.parent = parent
                self.nome = nome
            def __enter__(self):
                self.parent.iniciar(self.nome)
            def __exit__(self, exc_type, exc_val, exc_tb):
                self.parent.finalizar(self.nome)

        return _Bloco(self, nome)
