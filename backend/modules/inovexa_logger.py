# ===============================================================
#  MÓDULO: INOVEXA LOGGER
#  Projeto: MindScan — SynMind MI v2.0
#  Autor: Leo Vinci (GPT Inovexa)
#  Data: 07/11/2025
#  Função: Registrar logs criptografados da MI para auditoria
# ===============================================================

import os
import json
import datetime
from cryptography.fernet import Fernet

# ---------------------------------------------------------------
# Caminho padrão do arquivo de log
# ---------------------------------------------------------------
LOG_DIR = "backend/logs"
LOG_FILE = os.path.join(LOG_DIR, "mi_logs.enc")

# ---------------------------------------------------------------
# Garante diretório de logs
# ---------------------------------------------------------------
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR, exist_ok=True)

# ---------------------------------------------------------------
# Chave de criptografia (armazenada no .env)
# ---------------------------------------------------------------
def _get_fernet():
    key = os.getenv("INOVEXA_LOG_KEY")
    if not key:
        raise ValueError("Chave INOVEXA_LOG_KEY ausente do ambiente.")
    return Fernet(key.encode())

# ---------------------------------------------------------------
# Função principal de registro de log
# ---------------------------------------------------------------
def registrar_evento(usuario: str, tipo: str, conteudo: str, origem: str = "mi_engine"):
    """
    Registra um evento criptografado de atividade do MindScan.
    - usuario: nome ou ID do usuário que realizou o diagnóstico
    - tipo: tipo do evento ("diagnostico", "relatorio", "erro", etc.)
    - conteudo: texto ou resumo da ação
    - origem: módulo de origem (default = 'mi_engine')
    """
    try:
        fernet = _get_fernet()
        evento = {
            "usuario": usuario,
            "tipo": tipo,
            "origem": origem,
            "conteudo": conteudo[:5000],
            "timestamp": datetime.datetime.now().isoformat()
        }
        data = json.dumps(evento, ensure_ascii=False).encode()
        criptografado = fernet.encrypt(data)

        with open(LOG_FILE, "ab") as f:
            f.write(criptografado + b"\n")

        return True

    except Exception as e:
        print(f"[Inovexa Logger] Falha ao registrar evento: {e}")
        return False

# ---------------------------------------------------------------
# Função de leitura (uso interno da Inovexa)
# ---------------------------------------------------------------
def ler_logs(limit: int = 10):
    """
    Retorna os últimos N eventos descriptografados.
    Apenas para uso interno da Inovexa.
    """
    try:
        fernet = _get_fernet()
        if not os.path.exists(LOG_FILE):
            return []

        with open(LOG_FILE, "rb") as f:
            linhas = f.readlines()[-limit:]

        eventos = []
        for linha in linhas:
            try:
                evento = json.loads(fernet.decrypt(linha))
                eventos.append(evento)
            except Exception:
                continue

        return eventos

    except Exception as e:
        print(f"[Inovexa Logger] Erro na leitura: {e}")
        return []
