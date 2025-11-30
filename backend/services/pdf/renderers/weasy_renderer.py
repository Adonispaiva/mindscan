#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
weasy_renderer.py — Renderer Premium do MindScan usando WeasyPrint
------------------------------------------------------------------

Versão integrada ao Logger:
- Registra início da renderização
- Arquivo sendo gerado
- Erros detalhados
"""

from pathlib import Path
from weasyprint import HTML, CSS


class WeasyRenderer:
    def __init__(self, templates_dir: Path, logger=None):
        """
        templates_dir: pasta com base.html e estilo.css
        logger: instância de MindScanLogger (opcional)
        """
        self.templates_dir = Path(templates_dir)
        self.logger = logger

        self.base_html = self.templates_dir / "base.html"
        self.css_file = self.templates_dir / "estilo.css"

        # Logs
        if self.logger:
            self.logger.info(f"WeasyRenderer inicializado. Templates em: {self.templates_dir}")

        # Valida existência
        if not self.base_html.exists():
            msg = f"Template base não encontrado: {self.base_html}"
            if self.logger: self.logger.error(msg)
            raise FileNotFoundError(msg)

        if not self.css_file.exists():
            msg = f"Arquivo de estilo não encontrado: {self.css_file}"
            if self.logger: self.logger.error(msg)
            raise FileNotFoundError(msg)

    # --------------------------------------------------------------
    # RENDERIZAÇÃO FINAL PARA PDF
    # --------------------------------------------------------------
    def render_html_to_pdf(self, conteudo_html: str, output_path: Path):
        """
        Converte HTML final em PDF real usando WeasyPrint.
        """

        if self.logger:
            self.logger.info("Iniciando renderização com WeasyPrint...")
            self.logger.info(f"Arquivo de saída: {output_path}")

        try:
            # Carregar template base
            base = self.base_html.read_text(encoding="utf-8")

            # Substituir o placeholder
            final_html = base.replace("{{conteudo}}", conteudo_html)

            # Gerar PDF
            HTML(string=final_html, base_url=str(self.templates_dir)).write_pdf(
                str(output_path),
                stylesheets=[CSS(filename=str(self.css_file))]
            )

            if self.logger:
                self.logger.info("Renderização concluída com sucesso (WeasyPrint).")

            return output_path

        except Exception as e:
            if self.logger:
                self.logger.evento_erro("WeasyRenderer.render_html_to_pdf", e)
            raise e
