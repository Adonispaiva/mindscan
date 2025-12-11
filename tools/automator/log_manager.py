# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\tools\automator\log_manager.py
# Última atualização: 2025-12-11T09:59:27.808460

"""
log_manager.py
Gerenciador central de logs do MindScan Automator - Versão Profissional Completa

Funções oferecidas:
    • Logs coloridos no console
    • Logs com timestamps
    • Logs hierárquicos
    • Registro em arquivo (automator_log.txt)
    • Registro por sessão
    • Cabeçalhos e separadores estilizados
"""

import os
import datetime
import sys
import traceback


class LogManager:

    # ================================
    #         CONFIGURAÇÕES
    # ================================
    LOG_DIR = "tools/automator/logs"
    LOG_FILE = "automator_log.txt"

    COLOR_RESET = "\033[0m"
    COLOR_INFO = "\033[94m"       # azul
    COLOR_WARN = "\033[93m"       # amarelo
    COLOR_ERROR = "\033[91m"      # vermelho
    COLOR_SUCCESS = "\033[92m"    # verde
    COLOR_HEADER = "\033[95m"     # magenta

    def __init__(self):

        # Garante que o diretório de logs existe
        if not os.path.exists(self.LOG_DIR):
            os.makedirs(self.LOG_DIR)

        # Caminho final do arquivo de log
        self.log_path = os.path.join(self.LOG_DIR, self.LOG_FILE)

        # Cria uma sessão única
        self.session_id = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Session header
        self._write_file("\n============================================")
        self._write_file(f"Nova sessão iniciada: {self.session_id}")
        self._write_file("============================================\n")

    # ================================
    #        MÉTODOS INTERNOS
    # ================================

    def _timestamp(self):
        return datetime.datetime.now().strftime("%H:%M:%S")

    def _write_file(self, text):
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(text + "\n")

    def _log(self, prefix, color, msg):
        timestamp = self._timestamp()
        formatted = f"{color}[{prefix}] {timestamp}: {msg}{self.COLOR_RESET}"

        # Exibe no console
        print(formatted)

        # Salva no arquivo sem códigos ANSI
        clean_text = f"[{prefix}] {timestamp}: {msg}"
        self._write_file(clean_text)

    # ================================
    #           MÉTODOS PÚBLICOS
    # ================================

    def info(self, msg):
        self._log("INFO", self.COLOR_INFO, msg)

    def warn(self, msg):
        self._log("WARNING", self.COLOR_WARN, msg)

    def error(self, msg):
        self._log("ERROR", self.COLOR_ERROR, msg)

    def success(self, msg):
        self._log("SUCCESS", self.COLOR_SUCCESS, msg)

    def separator(self):
        sep = "-" * 60
        print(self.COLOR_HEADER + sep + self.COLOR_RESET)
        self._write_file(sep)

    def header(self, title):
        block = f"========== {title} =========="
        print(self.COLOR_HEADER + block + self.COLOR_RESET)
        self._write_file(block)

    def exception(self, e: Exception):
        """
        Registra falha com stacktrace completo.
        """
        self.error(str(e))
        trace = traceback.format_exc()
        self._write_file(trace)
        print(self.COLOR_ERROR + trace + self.COLOR_RESET)
