# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\pdf_sections\recomendacoes.py
# Última atualização: 2025-12-11T09:59:21.231327

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
recomendacoes.py — Seção de Recomendações Profissionais (MindScan PDF Premium)
Versão consolidada — Leo Vinci v2.0
---------------------------------------------------------------------------
Inclui:
- Recomendações de desenvolvimento
- Sugestões práticas baseadas nos resultados
- Direcionamento MI
"""

from typing import Dict, Any


def build_recomendacoes(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Retorna estrutura padronizada para o PDFEngine:
    {id, titulo, html}
    """

    resultados = context.get("resultados", {})
    mi = context.get("mi", {})

    rec_mi = mi.get("recomendacoes", {}) or {}

    texto_mi = rec_mi.get(
        "texto",
        "Com base nos padrões identificados, seguem recomendações estratégicas "
        "para fortalecimento do desempenho profissional e desenvolvimento contínuo."
    )

    lista_recs = rec_mi.get("lista", [
        "Aprimorar consistência comportamental em contextos de pressão.",
        "Desenvolver estratégias de regulação emocional.",
        "Expandir repertório de interação social em ambientes colaborativos.",
        "Fortalecer postura analítica em decisões complexas."
    ])

    itens = "".join(f"<li>{item}</li>" for item in lista_recs)

    html = f"""
<section class="recomendacoes page">

    <h2 class="secao-titulo">Recomendações Profissionais</h2>

    <p class="mi-texto">{texto_mi}</p>

    <ul class="lista-recomendacoes">
        {itens}
    </ul>

</section>
"""

    return {
        "id": "recomendacoes",
        "titulo": "Recomendações Profissionais",
        "html": html
    }
