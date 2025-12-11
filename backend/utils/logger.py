# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\utils\logger.py
# Última atualização: 2025-12-11T09:59:21.308202

# D:\projetos-inovexa\mindscan\backend\utils\logger.py

import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs")

class MindScanLogger:
    """
    Logger global do MindScan.
    Produz logs estruturados, rotativos e prontos para auditoria.
    """

    def __init__(self, name: str = "MindScan"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        os.makedirs(LOG_DIR, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d")
        logfile = os.path.join(LOG_DIR, f"mindscan_{timestamp}.log")

        handler = RotatingFileHandler(
            logfile,
            maxBytes=5 * 1024 * 1024,  # 5 MB
            backupCount=10
        )
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        handler.setFormatter(formatter)

        if not self.logger.handlers:
            self.logger.addHandler(handler)

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def critical(self, message: str):
        self.logger.critical(message)


# Instância global usada pelo sistema inteiro
logger = MindScanLogger("MindScan").logger
