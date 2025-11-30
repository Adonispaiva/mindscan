#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mindscan_pdf_cli.py — CLI Oficial do MindScan PDF Engine
---------------------------------------------------------

Permite gerar relatórios via terminal:

Exemplo:
    python mindscan_pdf_cli.py gerar --usuario usuario.json --resultados resultados.json --mi mi.json

Este CLI é profissional, robusto, com validações, logs e integração total
com PDFBuilder + WeasyRenderer.
"""

import argparse
import json
from pathlib import Path
import sys

# Importações internas
from pdf_builder import PDFBuilder
from backend.services.pdf.renderers.weasy_renderer import WeasyRenderer


# ================================================================
# Utilidades
# ================================================================
def carregar_json(path: str):
    p = Path(path)
    if not p.exists():
        print(f"[ERRO] Arquivo JSON não encontrado: {path}")
        sys.exit(1)

    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[ERRO] Falha ao carregar JSON {path}: {e}")
        sys.exit(1)


# ================================================================
# Comando: gerar relatório
# ================================================================
def cmd_gerar(args):
    print("\n=== MindScan PDF Engine — Geração de Relatório ===")

    # Carregar arquivos
    dados_usuario = carregar_json(args.usuario_json)
    resultados = carregar_json(args.resultados_json)
    mi = carregar_json(args.mi_json)

    # Caminhos internos
    ROOT = Path(__file__).resolve().parent.parent
    PDF_DIR = ROOT / "backend" / "services" / "pdf"
    TEMPLATES_DIR = PDF_DIR / "templates"

    # Instanciar renderer
    print("• Inicializando renderer (WeasyPrint)...")
    renderer = WeasyRenderer(TEMPLATES_DIR)

    # Gerar relatório
    print("• Gerando PDF...")
    builder = PDFBuilder()
    pdf_path = builder.gerar_relatorio(dados_usuario, resultados, mi, renderer)

    print(f"\n✔ Relatório gerado com sucesso!")
    print(f"📄 Caminho: {pdf_path}\n")


# ================================================================
# Função principal (parser)
# ================================================================
def main():
    parser = argparse.ArgumentParser(
        description="CLI Oficial MindScan — PDF Engine Premium"
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
        help="Arquivo JSON contendo os resultados dos algoritmos"
    )

    gerar.add_argument(
        "--mi",
        dest="mi_json",
        required=True,
        help="Arquivo JSON contendo textos MI"
    )

    gerar.set_defaults(func=cmd_gerar)

    # ------------------------------------------------------------
    # Executar
    # ------------------------------------------------------------
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
