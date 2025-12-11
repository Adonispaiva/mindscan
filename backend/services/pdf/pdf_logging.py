# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\pdf_logging.py
# Última atualização: 2025-12-11T09:59:21.184463

# pdf_logging.py — Logging estruturado MindScan PDF Engine
# Autor: Leo Vinci — Inovexa Software

import datetime


class PDFLogger:
    """
    Logger simples e auditável para o PDF Engine.
    Permite rastrear eventos, erros e fases do pipeline.
    """

    def __init__(self):
        self.entries = []

    def _timestamp(self):
        return datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    def info(self, message: str):
        entry = f"[INFO] {self._timestamp()} — {message}"
        self.entries.append(entry)
        print(entry)

    def warn(self, message: str):
        entry = f"[WARN] {self._timestamp()} — {message}"
        self.entries.append(entry)
        print(entry)

    def error(self, message: str):
        entry = f"[ERROR] {self._timestamp()} — {message}"
        self.entries.append(entry)
        print(entry)

    def get_log(self):
        return "\n".join(self.entries)
