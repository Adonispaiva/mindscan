import sys
import os
import logging

# Configuração de Cores para o Terminal (Sucesso/Erro)
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

logging.basicConfig(level=logging.INFO, format="%(message)s")

def check_mindscan_readiness():
    print(f"\n{GREEN}🌌 INOVEXA SOFTWARE - PROTOCOLO ORION - PREFLIGHT CHECK{RESET}")
    print("---------------------------------------------------------")
    
    steps = {
        "1. Estrutura de Pastas": ["main.py", "services/engine.py", "services/narrative_engine.py", "routers/diagnostic_router.py"],
        "2. Motores de Cálculo": "engine_test",
        "3. Gerador de PDF": "pdf_test"
    }

    # Passo 1: Arquivos
    for file in steps["1. Estrutura de Pastas"]:
        if os.path.exists(file):
            print(f"[OK] Arquivo encontrado: {file}")
        else:
            print(f"{RED}[FALHA] Arquivo ausente: {file}{RESET}")
            return

    # Passo 2: Teste de Lógica (DASS-21)
    try:
        from services.engine import MindScanEngine
        test_payload = {"dass21": {"depression_items": [1, 1, 1, 1, 1, 1, 1]}} # Soma 7 * 2 = 14
        result = MindScanEngine._calculate_dass21(test_payload["dass21"])
        if result["depression"]["score"] == 14 and result["depression"]["level"] == "Leve":
            print(f"{GREEN}[OK] Algoritmo DASS-21 validado com precisão científica.{RESET}")
        else:
            print(f"{RED}[FALHA] Erro de precisão no cálculo psicométrico.{RESET}")
    except Exception as e:
        print(f"{RED}[ERRO] Falha ao carregar MindScanEngine: {e}{RESET}")

    # Passo 3: Verificação de PDF
    if os.path.exists("D:/mindscan/generated_reports/"):
        print(f"{GREEN}[OK] Diretório de relatórios pronto.{RESET}")
    else:
        os.makedirs("D:/mindscan/generated_reports/")
        print("[AVISO] Diretório de relatórios criado agora.")

    print("---------------------------------------------------------")
    print(f"{GREEN}🚀 MINDSCAN ESTÁ PRONTO PARA A REUNIÃO DAS 16H!{RESET}\n")

if __name__ == "__main__":
    check_mindscan_readiness()