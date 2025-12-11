# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\utils\id_generator.py
# Última atualização: 2025-12-11T09:59:21.308202

# ============================================================
# MindScan — ID Generator (UTILS)
# ============================================================
# Gerador de IDs unificados seguindo o padrão SynMind:
# - UUID4
# - Encoded NanoID
# - SynID baseado em timestamp
# - Hash curto para logs e auditoria
#
# Versão completa e maximizada.
# ============================================================

import uuid
import base64
import hashlib
from datetime import datetime
from typing import Optional


class IDGenerator:
    """
    Gerador de IDs multi-formato utilizado em:
    - testes MindScan
    - relatórios PDF
    - MI packages
    - auditorias
    - logs internos
    """

    # ------------------------------------------------------------
    # UUID4 PADRÃO
    # ------------------------------------------------------------
    @staticmethod
    def uuid() -> str:
        return str(uuid.uuid4())

    # ------------------------------------------------------------
    # NANO-ID BASEADO EM UUID
    # ------------------------------------------------------------
    @staticmethod
    def nanoid(length: int = 12) -> str:
        raw = uuid.uuid4().bytes
        encoded = base64.urlsafe_b64encode(raw).decode("utf-8")
        clean = encoded.replace("=", "")
        return clean[:length]

    # ------------------------------------------------------------
    # SYNMIND ID (timestamp + hash curto)
    # ------------------------------------------------------------
    @staticmethod
    def synid(prefix: str = "MS") -> str:
        """
        Padrão:
        MS-2025-01-28-14H32M56-8F4A
        """
        now = datetime.utcnow().strftime("%Y-%m-%d-%H%M%S")
        hash_short = IDGenerator.hash_short(now)
        return f"{prefix}-{now}-{hash_short}"

    # ------------------------------------------------------------
    # HASH CURTO
    # ------------------------------------------------------------
    @staticmethod
    def hash_short(text: str) -> str:
        h = hashlib.sha256(text.encode()).hexdigest()
        return h[:6].upper()

    # ------------------------------------------------------------
    # GERA ID PARA TESTES MINDSCAN
    # ------------------------------------------------------------
    @staticmethod
    def test_id() -> str:
        return IDGenerator.synid(prefix="TEST")

    # ------------------------------------------------------------
    # GERA ID PARA PDF/RELATÓRIOS
    # ------------------------------------------------------------
    @staticmethod
    def report_id() -> str:
        return IDGenerator.synid(prefix="RPT")

    # ------------------------------------------------------------
    # GERA ID PARA LOGS E AUDITORIA
    # ------------------------------------------------------------
    @staticmethod
    def log_id() -> str:
        return IDGenerator.nanoid(10)
