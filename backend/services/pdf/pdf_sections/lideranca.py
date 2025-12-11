# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\pdf_sections\lideranca.py
# Última atualização: 2025-12-11T09:59:21.215694

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lideranca.py — Seção de Estilo de Liderança (MindScan PDF Premium)
Versão consolidada — Leo Vinci v2.0
------------------------------------------------------------------
Apresenta:
- Indicadores de liderança
- Interpretação MI
- Padrões comportamentais de influência, direção e gestão
"""

from typing import Dict, Any


def build_lideranca(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Padrão oficial: {id, titulo, html}
    Compatível com PDFEngine v2.0 e templates premium.
    """

    resultados = context.get("resultados", {})
    mi = context.get("mi", {})

    estilo = resultados.get("lideranca", {}) or {}
    lideranca_mi = mi.get("lideranca", {}) or {}

    texto_mi = lideranca_mi.get(
        "texto",
        "O estilo de liderança demonstra padrões de influência, coordenação e "
        "gestão coerentes com os traços de personalidade predominantes."
    )

    # Construção das linhas da tabela (fallback incluído)
    def linha(nome: str, chave: str) -> str:
        return f"<tr><td>{nome}</td><td>{estilo.get(chave, '—')}</td></tr>"

    tabela = "".join([
        linha("Tomada de decisão", "decisao"),
        linha("Influência social", "influencia"),
        linha("Gestão emocional", "gestao_emocional"),
        linha("Direção e clareza", "direcao"),
        linha("Relacionamento interpessoal", "relacional"),
    ])

    html = f"""
<section class="lideranca page">

    <h2 class="secao-titulo">Estilo de Liderança</h2>

    <p class="mi-texto">
        {texto_mi}
    </p>

    <table class="tabela-padrao">
        <thead>
            <tr>
                <th>Indicador</th>
                <th>Nível</th>
            </tr>
        </thead>
        <tbody>
            {tabela}
        </tbody>
    </table>

</section>
"""

    return {
        "id": "lideranca",
        "titulo": "Estilo de Liderança",
        "html": html
    }
