from reportlab.lib.units import cm
from reportlab.platypus import Spacer  # Adicionado para corrigir o NameError
from .base_renderer import BaseRenderer

class TechnicalRenderer(BaseRenderer):
    """
    Renderizador do Relatório Técnico MindScan.
    Focado em precisão de dados, métricas de performance e scores psicométricos.
    """

    def build(self):
        """
        Constrói a estrutura do PDF seguindo o fluxo:
        Capa -> Bússola -> BIG5 (Gráfico) -> DASS-21 (Tabela) -> Metadados.
        """
        # 1. Cabeçalho e Título
        self.add_logo()
        self.title("Relatório Técnico de Diagnóstico")
        self.paragraph(f"Candidato: {self.candidate_name}")
        self.paragraph(f"ID do Teste: {self.test_id}")
        self.story.append(Spacer(1, 1*cm))

        # 2. Bússola de Talentos (Destaque Principal)
        bussula = self.results.get("bussula", {})
        self.heading("1. Posicionamento na Bússola de Talentos")
        self.paragraph(f"<b>Quadrante:</b> {bussula.get('quadrante', 'Analisando...')}")
        self.paragraph(f"<i>{bussula.get('mensagem', '')}</i>")
        self.story.append(Spacer(1, 0.5*cm))

        # 3. Personalidade (BIG5) com Gráfico de Radar
        big5 = self.results.get("big5", {})
        if big5:
            self.heading("2. Perfil de Personalidade (BIG5)")
            self.draw_radar_chart(big5, title="Distribuição dos 5 Grandes Fatores")
            self.paragraph("Este gráfico representa a inclinação comportamental natural do indivíduo sob condições normais.")

        # 4. Saúde Emocional (DASS-21) com Tabela
        dass = self.results.get("dass21", {})
        if "scores" in dass:
            self.heading("3. Inventário de Estados Emocionais (DASS-21)")
            
            # Prepara dados para a tabela
            dass_data = [
                ["Dimensão", "Score Real", "Classificação"],
                ["Depressão", dass['scores']['depression'], dass['classification']['depression']],
                ["Ansiedade", dass['scores']['anxiety'], dass['classification']['anxiety']],
                ["Estresse", dass['scores']['stress'], dass['classification']['stress']]
            ]
            self.add_score_table(dass_data, title="Tabela de Gravidade (Lovibond)")

        # 5. Metadados e Auditoria
        self.page_break()
        self.heading("4. Informações de Auditoria")
        metadata = self.results.get("metadata", {})
        if metadata:
            for k, v in metadata.items():
                self.paragraph(f"<b>{k}:</b> {v}")

        return self.story