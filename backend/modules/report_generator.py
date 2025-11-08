# ===============================================================
#  MÓDULO: REPORT GENERATOR
#  Projeto: MindScan — SynMind MI v2.0
#  Autor: Leo Vinci (GPT Inovexa)
#  Data: 07/11/2025
#  Função: Geração de relatório PDF com gráficos e narrativa MI
# ===============================================================

from datetime import datetime
from typing import Dict
import matplotlib.pyplot as plt
from fpdf import FPDF
import io
import base64

class MindScanPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, "🧠 Relatório MindScan — SynMind MI v2.0", ln=True, align="C")
        self.ln(4)
        self.set_font("Helvetica", "", 10)
        self.cell(0, 8, f"Emitido em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align="R")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 8, f"MindScan SynMind — Inovexa Software © {datetime.now().year}", align="C")

def gerar_grafico_barras(scores: Dict[str, int]) -> bytes:
    """Gera gráfico de barras simples para DASS-21 e retorna bytes PNG."""
    labels = list(scores.keys())
    values = list(scores.values())

    plt.figure(figsize=(5, 3))
    plt.bar(labels, values)
    plt.title("Pontuação DASS-21")
    plt.ylabel("Nível")
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    return buffer.read()

def gerar_relatorio_pdf(dados: Dict) -> bytes:
    """
    Gera o relatório PDF MindScan consolidado.
    Parâmetros:
        dados = {
            "nome": str,
            "scores": {"DEPRESSAO": int, "ANSIEDADE": int, "ESTRESSE": int},
            "quadrante": str,
            "score_performance": float,
            "relatorio_mi": str
        }
    Retorna: bytes do arquivo PDF
    """
    nome = dados.get("nome", "Usuário")
    scores = dados.get("scores", {})
    quadrante = dados.get("quadrante", "Indefinido")
    score_perf = dados.get("score_performance", 0)
    texto_mi = dados.get("relatorio_mi", "")

    # Gera gráfico e codifica temporariamente
    grafico_bytes = gerar_grafico_barras(scores)
    grafico_b64 = base64.b64encode(grafico_bytes).decode("utf-8")

    pdf = MindScanPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Cabeçalho do relatório
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, f"Relatório Individual — {nome}", ln=True)
    pdf.ln(6)

    # Seção de resultados numéricos
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, "Resultados Psicométricos (DASS-21):", ln=True)
    for eixo, valor in scores.items():
        pdf.cell(0, 8, f"- {eixo.capitalize()}: {valor}", ln=True)
    pdf.ln(4)

    pdf.cell(0, 8, f"Quadrante Bússola: {quadrante}", ln=True)
    pdf.cell(0, 8, f"Score de Performance Global: {score_perf}%", ln=True)
    pdf.ln(6)

    # Insere o gráfico
    img_stream = io.BytesIO(base64.b64decode(grafico_b64))
    pdf.image(img_stream, x=40, w=120)
    pdf.ln(8)

    # Seção interpretativa
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "Interpretação MI:", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 7, texto_mi)
    pdf.ln(6)

    # Finalização
    pdf.set_font("Helvetica", "I", 9)
    pdf.multi_cell(0, 6, "Este relatório foi gerado automaticamente pelo sistema SynMind MI v2.0, desenvolvido pela Inovexa Software, com base em dados psicométricos e analíticos do MindScan.")
    pdf.ln(4)

    # Gera bytes
    return pdf.output(dest="S").encode("latin1")
