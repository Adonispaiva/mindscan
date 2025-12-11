# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\telemetry\logger.py
# Última atualização: 2025-12-11T09:59:21.275871

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
logger.py — Sistema Oficial de Logs e Telemetria do MindScan PDF Engine
-----------------------------------------------------------------------

Funcionalidades:
- Criação automática do diretório de logs
- Log rotacionado por data
- Funções de alto nível para registrar eventos
- Modo silencioso opcional
- API corporativa para instrumentação do PDF Engine
"""

import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from datetime import datetime


class MindScanLogger:

    def __init__(self, logs_dir: Path = None, silent: bool = False):
        """
        logs_dir: caminho da pasta onde os logs serão armazenados
        silent: se True, não exibe logs no console
        """
        if logs_dir is None:
            ROOT = Path(__file__).resolve().parent.parent.parent.parent
            logs_dir = ROOT / "logs"

        self.logs_dir = Path(logs_dir)
        self.logs_dir.mkdir(exist_ok=True, parents=True)

        self.silent = silent

        self.logger = logging.getLogger("MindScanPDF")
        self.logger.setLevel(logging.INFO)
        self.logger.handlers.clear()  # evita duplicação

        # ------------------------------------------------------------
        # 1) Handler de arquivo (rotacionado diariamente)
        # ------------------------------------------------------------
        file_handler = TimedRotatingFileHandler(
            filename=str(self.logs_dir / "mindscan_pdf.log"),
            when="midnight",
            interval=1,
            backupCount=30,
            encoding="utf-8"
        )
        file_handler.setFormatter(logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        ))
        self.logger.addHandler(file_handler)

        # ------------------------------------------------------------
        # 2) Handler de console (caso não esteja no modo silencioso)
        # ------------------------------------------------------------
        if not silent:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter(
                "%(asctime)s | %(levelname)s | %(message)s"
            ))
            self.logger.addHandler(console_handler)

    # ===============================================================
    # API de Logging Corporativo
    # ===============================================================

    def info(self, mensagem: str):
        self.logger.info(mensagem)

    def warn(self, mensagem: str):
        self.logger.warning(mensagem)

    def error(self, mensagem: str):
        self.logger.error(mensagem)

    def evento_pdf_iniciado(self, usuario: str):
        self.info(f"Iniciando geração de PDF para: {usuario}")

    def evento_pdf_finalizado(self, path: Path):
        self.info(f"PDF gerado com sucesso: {path}")

    def evento_erro(self, contexto: str, erro: Exception):
        self.error(f"Erro em '{contexto}': {erro}")

    def evento_validacao_ok(self):
        self.info("Validação dos dados concluída com sucesso.")

    def evento_validacao_falhou(self, erro: Exception):
        self.error(f"FALHA na validação dos dados: {erro}")

    def evento_renderer(self, nome_renderer: str):
        self.info(f"Renderer utilizado: {nome_renderer}")

    def evento_json_carregado(self, nome: str):
        self.info(f"JSON carregado: {nome}")

    # ===============================================================
    # Telemetria simples (extensível)
    # ===============================================================

    def registrar_telemetria(self, tipo: str, dados: dict):
        """
        Registra um evento de telemetria no arquivo mindscan_telemetry.log.
        """
        path = self.logs_dir / "mindscan_telemetry.log"
        timestamp = datetime.utcnow().isoformat()

        entrada = {
            "timestamp": timestamp,
            "tipo": tipo,
            "dados": dados
        }

        with path.open("a", encoding="utf-8") as f:
            f.write(str(entrada) + "\n")
