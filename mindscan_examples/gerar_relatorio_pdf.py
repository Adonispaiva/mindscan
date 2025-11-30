#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gerar_relatorio_pdf.py — Exemplo Oficial MindScan
-------------------------------------------------

Este script demonstra como gerar um relatório PDF REAL
usando o PDFEngine Premium + PDFBuilder + WeasyRenderer.

Requisitos:
    pip install weasyprint
"""

from pathlib import Path
from pdf_builder import PDFBuilder
from pdf.renderers.weasy_renderer import WeasyRenderer


# ============================================================
# 1) Caminhos
# ============================================================
ROOT = Path(__file__).resolve().parent.parent
PDF_DIR = ROOT / "backend" / "services" / "pdf"
TEMPLATES_DIR = PDF_DIR / "templates"


# ============================================================
# 2) Dados simulados (exemplo)
# ============================================================
dados_usuario = {
    "nome": "João Carvalho",
    "idade": 32,
    "genero": "Masculino",
    "cargo": "Analista de Sistemas",
    "senioridade": "Pleno",
    "empresa": "Inovexa Software"
}

resultados = {
    "big_five": {
        "abertura": 72,
        "conscienciosidade": 66,
        "extroversao": 41,
        "agradabilidade": 58,
        "neuroticismo": 37
    },
    "lideranca": {
        "decisao": "Moderado",
        "influencia": "Alto",
        "gestao_emocional": "Adequado",
        "direcao": "Bom",
        "relacional": "Consistente"
    },
    "ocai": {
        "cla": 58,
        "adhocracia": 65,
        "mercado": 52,
        "hierarquia": 47
    },
    "esquemas": {
        "Autoexigência": "Moderado",
        "Aprovação": "Baixo",
        "Abandono": "Muito baixo"
    },
    "dass": {
        "depressao": "Normal",
        "ansiedade": "Leve",
        "estresse": "Moderado"
    },
    "performance": {
        "2023-S1": 72,
        "2023-S2": 79,
        "2024-S1": 83,
        "2024-S2": 81
    },
    "bussola": {
        "Analítico": "Alto",
        "Criativo": "Moderado",
        "Relacional": "Adequado",
        "Executor": "Forte"
    },
    "anexos": [
        "Pontuação detalhada Big Five",
        "Tabela de Facetas TEIQue"
    ]
}

mi = {
    "resumo_executivo": {
        "texto": "O avaliado demonstra solidez comportamental e potencial para funções estratégicas.",
        "destaques": [
            "Boa capacidade de análise.",
            "Estabilidade emocional acima da média."
        ],
        "alertas": [
            "Melhorar consistência em interações de alta pressão."
        ]
    }
}


# ============================================================
# 3) Instância do Renderer
# ============================================================
renderer = WeasyRenderer(TEMPLATES_DIR)


# ============================================================
# 4) Gerar relatório final
# ============================================================
builder = PDFBuilder()
pdf_path = builder.gerar_relatorio(dados_usuario, resultados, mi, renderer)

print("\n===============================================")
print(" RELATÓRIO PDF GERADO COM SUCESSO!")
print(f" Caminho: {pdf_path}")
print("===============================================\n")
