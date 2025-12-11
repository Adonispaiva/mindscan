# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\run_e2e.py
# Última atualização: 2025-12-11T09:59:20.558303

import json
import os
from datetime import datetime

# Importações do projeto real
from services.report_service import ReportService

# Caminhos oficiais
BASE_DIR = r"D:\projetos-inovexa\mindscan\backend"
RESULTS_PATH = os.path.join(BASE_DIR, "services", "export", "mindscan_results.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "reports")

# Test ID padrão
TEST_ID = "MS-E2E-2025-11-28-01"

def load_results():
    if not os.path.exists(RESULTS_PATH):
        raise FileNotFoundError(f"Arquivo de resultados não encontrado em: {RESULTS_PATH}")

    with open(RESULTS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("O arquivo JSON deve conter uma lista de blocos psicométricos.")

    print(f"[OK] {len(data)} blocos carregados do JSON.")
    return data


def generate_reports(results):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    report_types = [
        "technical",
        "executive",
        "psychodynamic",
        "premium"
    ]

    summary = {}

    for rtype in report_types:
        print(f"\n➡ Gerando relatório: {rtype.upper()}")

        filepath, metadata = ReportService.generate_pdf(
            test_id=TEST_ID,
            results=results,
            report_type=rtype
        )

        print(f"[OK] Arquivo gerado: {filepath}")
        summary[rtype] = metadata

    return summary


def main():
    print("============================================")
    print("   INOVEXA — MindScan v2.0 — Execução E2E   ")
    print("============================================\n")

    print(f"Test ID: {TEST_ID}")
    print("Carregando resultados psicométricos...")
    
    results = load_results()

    print("\nIniciando geração dos relatórios oficiais...\n")
    summary = generate_reports(results)

    print("\n============================================")
    print("        E2E FINALIZADO COM SUCESSO          ")
    print("============================================\n")

    for rtype, meta in summary.items():
        print(f"{rtype.upper()} → {meta['path']}")

    print("\nRelatórios completos disponíveis em:")
    print(f"{OUTPUT_DIR}\n")


if __name__ == "__main__":
    main()
