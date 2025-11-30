#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
identidade.py — Seção de Identidade (MindScan PDF Premium)
----------------------------------------------------------

Responsável por apresentar:
- Dados essenciais do avaliado
- Informações contextuais
- Identidade profissional
- Estrutura compatível com o PDF Premium
"""

from datetime import datetime

class IdentidadeSection:
    def render(self, context: dict) -> str:
        usuario = context.get("usuario", {})

        nome = usuario.get("nome", "Nome não informado")
        idade = usuario.get("idade", "—")
        genero = usuario.get("genero", "—")
        cargo = usuario.get("cargo", "—")
        senioridade = usuario.get("senioridade", "—")
        empresa = usuario.get("empresa", "—")
        data_geracao = datetime.now().strftime("%d/%m/%Y")

        return f"""
<section class="identidade">
    <h2 class="secao-titulo">Identidade Profissional</h2>

    <div class="identidade-container">

        <div class="identidade-bloco">
            <h3>Informações do Avaliado</h3>
            <p><strong>Nome:</strong> {nome}</p>
            <p><strong>Idade:</strong> {idade}</p>
            <p><strong>Gênero:</strong> {genero}</p>
            <p><strong>Empresa:</strong> {empresa}</p>
        </div>

        <div class="identidade-bloco">
            <h3>Contexto Profissional</h3>
            <p><strong>Cargo Atual:</strong> {cargo}</p>
            <p><strong>Senioridade:</strong> {senioridade}</p>
            <p><strong>Data do Relatório:</strong> {data_geracao}</p>
        </div>

    </div>
</section>
"""
