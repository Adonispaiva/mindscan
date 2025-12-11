# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\renderers\matplotlib_ready.py
# Última atualização: 2025-12-11T09:59:21.246951

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
matplotlib_ready.py — Gerador de gráficos Base64 para o MindScan PDF
--------------------------------------------------------------------

Este módulo gera imagens base64 dos gráficos usados no relatório Premium.

Compatível com:
- PDFEngine
- PDFBuilder
- html <img src="data:image/png;base64,...">

Requisitos:
    pip install matplotlib
"""

import base64
import io
import matplotlib.pyplot as plt


class GraphGenerator:
    """
    Cria gráficos PNG em memória e converte para base64.
    Todos os gráficos são compatíveis com WeasyPrint.
    """

    # -------------------------------------------------------------
    #  GRÁFICO RADAR (Big Five, Bússola, etc.)
    # -------------------------------------------------------------
    def radar_chart(self, labels: list, values: list, title: str = "") -> str:
        """
        Gera um gráfico radar completo em base64.
        """

        num_vars = len(labels)

        angles = [n / float(num_vars) * 2 * 3.141592 for n in range(num_vars)]
        values = values + values[:1]
        angles = angles + angles[:1]

        fig = plt.figure(figsize=(4, 4))
        ax = plt.subplot(111, polar=True)

        ax.plot(angles, values)
        ax.fill(angles, values, alpha=0.25)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels)

        if title:
            ax.set_title(title, y=1.1)

        return self._fig_to_base64(fig)

    # -------------------------------------------------------------
    #  GRÁFICO DE BARRAS (TEIQue, Performance, DASS, etc.)
    # -------------------------------------------------------------
    def bar_chart(self, labels: list, values: list, title: str = "") -> str:
        """
        Gera gráfico de barras simples em base64.
        """

        fig, ax = plt.subplots(figsize=(5, 3))
        ax.bar(labels, values)

        if title:
            ax.set_title(title)

        return self._fig_to_base64(fig)

    # -------------------------------------------------------------
    #  GRÁFICO DE LINHA (Evolução da performance)
    # -------------------------------------------------------------
    def line_chart(self, labels: list, values: list, title: str = "") -> str:
        """
        Gráfico de linha — evolução temporal da performance.
        """

        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot(labels, values, marker="o")

        if title:
            ax.set_title(title)

        return self._fig_to_base64(fig)

    # -------------------------------------------------------------
    #  GRÁFICO DE PIZZA (Distribuições gerais)
    # -------------------------------------------------------------
    def pie_chart(self, labels: list, values: list, title: str = "") -> str:
        """
        Gráfico de pizza — distribuições percentuais.
        """

        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)

        if title:
            ax.set_title(title)

        return self._fig_to_base64(fig)

    # -------------------------------------------------------------
    #  CONVERSOR FINAL → FIG → BASE64
    # -------------------------------------------------------------
    def _fig_to_base64(self, fig) -> str:
        """
        Converte uma figura Matplotlib para base64 PNG.
        """

        buffer = io.BytesIO()
        fig.savefig(buffer, format="png", bbox_inches="tight")
        plt.close(fig)

        buffer.seek(0)
        img_bytes = buffer.read()
        base64_str = base64.b64encode(img_bytes).decode("utf-8")

        return f"data:image/png;base64,{base64_str}"
