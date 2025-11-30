#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
anexos.py — Seção de Anexos (MindScan PDF Premium)
--------------------------------------------------

Inclui:
- Tabelas adicionais
- Dados brutos
- Gráficos auxiliares
- Informações complementares do relatório
- Arquitetura preparada para anexos dinâmicos (como imagens base64)
"""

class AnexosSection:
    def render(self, context: dict) -> str:

        anexos = context.get("resultados", {}).get("anexos", [])
        mi = context.get("mi", {})
        anexos_mi = mi.get("anexos", {})

        texto_mi = anexos_mi.get(
            "texto",
            "Esta seção apresenta informações complementares que enriquecem a "
            "compreensão dos resultados obtidos pelo MindScan."
        )

        if not anexos:
            lista_html = "<p>Nenhum anexo adicional fornecido.</p>"
        else:
            itens = []
            for idx, item in enumerate(anexos, start=1):
                itens.append(f"<li><strong>Anexo {idx}:</strong> {item}</li>")
            lista_html = "<ul>" + "".join(itens) + "</ul>"

        return f"""
<section class="anexos">

    <h2 class="secao-titulo">Anexos</h2>

    <p class="mi-texto">{texto_mi}</p>

    {lista_html}

</section>
"""
