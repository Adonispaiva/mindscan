# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\mindscan_pdf\cli.py
# Última atualização: 2025-12-11T09:59:27.745995

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mindscan_pdf/cli.py — EntryPoint oficial com Logger integrado
-------------------------------------------------------------

Este módulo é executado quando a CLI instalada é chamada:

    mindscan-pdf gerar --usuario usuario.json --resultados resultados.json --mi mi.json

Funções adicionadas nesta versão:
- Logger corporativo integrado
- Registro de carregamento de JSON
- Registro de validação
- Registro do processo de geração do PDF
- Tratamento avançado de erros com telemetria
"""

import argparse
import json
import sys
from pathlib import Path

from pdf_builder import PDFBuilder
from backend.services.pdf.validators.data_validator import MindScanDataValidator
from backend.services.pdf.telemetry.logger import MindScanLogger
from backend.services.pdf.renderers.weasy_renderer import WeasyRenderer


# ================================================================
# Utilidade para carregar JSON (com logs)
# ================================================================
def carregar_json(path: str, logger: MindScanLogger):
    p = Path(path)

    if not p.exists():
        logger.error(f"Arquivo JSON não encontrado: {path}")
        print(f"[ERRO] Arquivo JSON não encontrado: {path}")
        sys.exit(1)

    try:
        logger.evento_json_carregado(path)
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        logger.evento_erro("carregar_json", e)
        print(f"[ERRO] Falha ao carregar JSON '{path}': {e}")
        sys.exit(1)


# ================================================================
# Comando: gerar relatório
# ================================================================
def cmd_gerar(args):
    logger = MindScanLogger()  # logger ativado

    print("\n=== MindScan PDF Engine — CLI Oficial ===\n")

    # Carregar arquivos
    usuario = carregar_json(args.usuario_json, logger)
    resultados = carregar_json(args.resultados_json, logger)
    mi = carregar_json(args.mi_json, logger)

    # Validar dados
    validator = MindScanDataValidator()

    try:
        validator.validar(usuario, resultados, mi)
        logger.evento_validacao_ok()
    except Exception as e:
        logger.evento_validacao_falhou(e)
        print(f"[ERRO] Falha na validação dos dados: {e}")
        sys.exit(1)

    # Caminhos internos
    ROOT = Path(__file__).resolve().parent.parent
    PDF_DIR = ROOT / "backend" / "services" / "pdf"
    TEMPLATES_DIR = PDF_DIR / "templates"

    # Instanciar renderer
    logger.evento_renderer("WeasyRenderer")
    renderer = WeasyRenderer(TEMPLATES_DIR)

    # Gerar relatório
    try:
        builder = PDFBuilder(logger=logger)
        logger.info("Iniciando pipeline de geração do PDF...")

        pdf_path = builder.gerar_relatorio(
            usuario,
            resultados,
            mi,
            renderer
        )

        logger.info(f"Relatório finalizado: {pdf_path}")

    except Exception as e:
        logger.evento_erro("cmd_gerar", e)
        print(f"[ERRO] Falha ao gerar relatório: {e}")
        sys.exit(1)

    print("\n✔ Relatório gerado com sucesso!")
    print(f"📄 Caminho: {pdf_path}\n")


# ================================================================
# Parser principal
# ================================================================
def main():
    parser = argparse.ArgumentParser(
        description="MindScan PDF Engine — CLI Oficial"
    )

    subparsers = parser.add_subparsers(dest="comando")

    # ------------------------------------------------------------
    # Subcomando: gerar
    # ------------------------------------------------------------
    gerar = subparsers.add_parser("gerar", help="Gerar relatório PDF completo")

    gerar.add_argument(
        "--usuario",
        dest="usuario_json",
        required=True,
        help="Arquivo JSON contendo dados do usuário"
    )

    gerar.add_argument(
        "--resultados",
        dest="resultados_json",
        required=True,
        help="Arquivo JSON contendo resultados dos algoritmos"
    )

    gerar.add_argument(
        "--mi",
        dest="mi_json",
        required=True,
        help="Arquivo JSON contendo dados de MI"
    )

    gerar.set_defaults(func=cmd_gerar)

    # Executa
    args = parser.parse_args()

    if not args.comando:
        parser.print_help()
        sys.exit(0)

    args.func(args)


# ================================================================
# Execução direta
# ================================================================
if __name__ == "__main__":
    main()
