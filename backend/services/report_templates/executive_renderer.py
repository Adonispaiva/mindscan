import os
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import Spacer, Table, TableStyle, Paragraph, Image
from reportlab.graphics.shapes import Drawing, Rect
from .base_renderer import BaseRenderer

class ExecutiveRenderer(BaseRenderer):
    """
    Renderizador do Relatório Executivo MindScan.
    Design Minimalista, focado em ROI, Liderança e Decisão Estratégica.
    """

    def build(self):
        # Caminho relativo para os logos
        base_path = os.path.dirname(os.path.abspath(__file__))
        logo_synmind = os.path.join(base_path, "assets", "logos", "synmind_logo.png")
        logo_mindscan = os.path.join(base_path, "assets", "logos", "mindscan_logo.png")

        # 1. Branding de Topo (Logo SynMind)
        if os.path.exists(logo_synmind):
            img = Image(logo_synmind, width=4*cm, height=1.5*cm)
            img.hAlign = 'RIGHT'
            self.story.append(img)
            self.story.append(Spacer(1, 0.5*cm))
        
        self.title("Executive Insight Report")
        self.paragraph(f"<b>Executivo:</b> {self.candidate_name}")
        self.story.append(Spacer(1, 1*cm))

        # 2. Sumário de Impacto (Veredito)
        bussula = self.results.get("bussula", {})
        perf_score = self.results.get('scores_consolidated', {}).get('performance', 0)
        
        summary_data = [
            [f"Quadrante Estratégico: {bussula.get('quadrante', 'N/A')}"],
            [f"Score de Performance: {perf_score}%"]
        ]
        
        t = Table(summary_data, colWidths=[16*cm])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F0F4F8")),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#1A3A5A")),
            ('PADDING', (0, 0), (-1, -1), 12),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 14),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor("#1A3A5A")),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))
        self.story.append(t)
        self.story.append(Spacer(1, 1.5*cm))

        # 3. Gráfico de Competências Críticas
        self.heading("Análise de Competências Críticas")
        self.paragraph("Mapeamento de Soft Skills baseado no cruzamento de BIG5 e Performance.")
        self.story.append(Spacer(1, 0.5*cm))
        
        # Dados simulados ou reais do BIG5
        big5 = self.results.get("big5", {})
        competencias = {
            "Liderança Inspiradora": big5.get("extroversao", 50),
            "Foco em Processos": big5.get("conscienciosidade", 50),
            "Resiliência Emocional": 100 - big5.get("neuroticismo", 50), # Invertido (baixo neuro = alta resiliência)
            "Adaptabilidade": big5.get("abertura", 50)
        }
        
        for comp, score in competencias.items():
            self._draw_skill_bar(comp, score)

        # 4. Recomendações Estratégicas (PDI)
        self.story.append(Spacer(1, 1*cm))
        self.heading("Plano de Desenvolvimento Estratégico (PDI)")
        self.paragraph("• <b>Ponto Forte:</b> Capacidade analítica e rigor operacional.")
        self.paragraph("• <b>Oportunidade:</b> Desenvolver habilidades de mentoria para elevar a base.")
        self.paragraph("• <b>Ação Imediata:</b> Ativar o protocolo de comunicação assertiva (30 dias).")

        # 5. Branding de Rodapé (Logo MindScan)
        self.story.append(Spacer(1, 2*cm))
        if os.path.exists(logo_mindscan):
            img_footer = Image(logo_mindscan, width=3*cm, height=1*cm)
            img_footer.hAlign = 'CENTER'
            self.story.append(img_footer)

        return self.story

    def _draw_skill_bar(self, name, percentage):
        """
        Desenha uma barra de progresso usando Primitivas Gráficas (Drawing/Rect).
        Isso garante precisão exata da porcentagem.
        """
        try:
            pct = float(percentage)
            # Limita entre 0 e 100 para evitar erros visuais
            pct = max(0, min(100, pct))
        except:
            pct = 0.0

        # Configuração das dimensões
        max_width = 8 * cm
        height = 0.6 * cm
        fill_width = (pct / 100.0) * max_width
        
        # Cria o Container do desenho
        d = Drawing(max_width, height)
        
        # 1. Fundo da barra (Cinza Claro)
        bg = Rect(0, 0, max_width, height)
        bg.fillColor = colors.HexColor("#E0E0E0")
        bg.strokeColor = None # Sem borda
        d.add(bg)
        
        # 2. Barra de Progresso (Azul SynMind)
        # O Rect desenha de baixo para cima (x, y, w, h)
        bar = Rect(0, 0, fill_width, height)
        bar.fillColor = colors.HexColor("#1A3A5A")
        bar.strokeColor = None
        d.add(bar)

        # Tabela para alinhar: Texto da Skill | Barra Gráfica | Valor Numérico
        data = [[name, d, f"{int(pct)}%"]]
        
        t = Table(data, colWidths=[6*cm, max_width + 0.5*cm, 1.5*cm])
        t.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'), # Nome da skill em negrito
            ('FONTNAME', (-1, 0), (-1, 0), 'Helvetica'),    # Porcentagem normal
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor("#1A3A5A")),
            ('ALIGN', (1, 0), (1, 0), 'LEFT'),   # Alinha o desenho à esquerda
            ('ALIGN', (-1, 0), (-1, 0), 'RIGHT'), # Alinha a porcentagem à direita
        ]))
        
        self.story.append(t)
        self.story.append(Spacer(1, 0.2*cm))