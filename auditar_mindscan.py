#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AUDITORIA MAX DO MINDSCAN
----------------------------------
Versão mais completa já criada.
"""

import os
import json
import hashlib
import datetime
import ast
import subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
TREE_REF = os.path.join(ROOT, "tree_referencia.json")
TREE_ATUAL = os.path.join(ROOT, "tree_atual.json")
RELATORIO = os.path.join(ROOT, "relatorio_auditoria.json")


# ============================================================
# UTILIDADES
# ============================================================

def sha256_arquivo(path):
    """Retorna o hash SHA256 de um arquivo."""
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for bloco in iter(lambda: f.read(4096), b""):
                h.update(bloco)
    except Exception:
        return None
    return h.hexdigest()


def gerar_estrutura(path):
    """Gera árvore completa com hash, tamanho e timestamps."""
    estrutura = {}
    for raiz, dirs, files in os.walk(path):
        for f in files:
            arq = os.path.join(raiz, f)
            rel = os.path.relpath(arq, ROOT)
            try:
                stat = os.stat(arq)
                estrutura[rel.replace("\\", "/")] = {
                    "tamanho": stat.st_size,
                    "hash": sha256_arquivo(arq),
                    "modificado": stat.st_mtime
                }
            except:
                pass
    return estrutura


def salvar_json(caminho, dados):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4)


# ============================================================
# AUDITORIA DE CÓDIGO (AST)
# ============================================================

def auditar_codigo(estrutura):
    relatorio = {
        "erros_sintaticos": [],
        "ciclos_import": [],
        "imports_ausentes": [],
        "funcoes_vazias": [],
        "classes_vazias": [],
        "dead_code": []
    }

    for arquivo in estrutura:
        if not arquivo.endswith(".py"):
            continue

        full = os.path.join(ROOT, arquivo)

        try:
            with open(full, "r", encoding="utf-8") as f:
                codigo = f.read()

            tree = ast.parse(codigo)

        except SyntaxError as e:
            relatorio["erros_sintaticos"].append({
                "arquivo": arquivo,
                "erro": str(e)
            })
            continue

        # detectar imports e funções
        for node in ast.walk(tree):

            # função vazia
            if isinstance(node, ast.FunctionDef):
                if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                    relatorio["funcoes_vazias"].append(f"{arquivo}:{node.name}")

            # classe vazia
            if isinstance(node, ast.ClassDef):
                if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                    relatorio["classes_vazias"].append(f"{arquivo}:{node.name}")

            # imports com nomes inexistentes
            if isinstance(node, ast.Import):
                for n in node.names:
                    try:
                        __import__(n.name)
                    except:
                        relatorio["imports_ausentes"].append(f"{arquivo}: {n.name}")

            if isinstance(node, ast.ImportFrom):
                try:
                    __import__(node.module)
                except:
                    relatorio["imports_ausentes"].append(
                        f"{arquivo}: from {node.module} import ..."
                    )

    return relatorio


# ============================================================
# AUDITORIA DO GITHUB
# ============================================================

def auditar_github():
    """Obtém diferenças via git diff --name-status."""
    out = subprocess.Popen(
        "git fetch origin",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        errors="ignore"
    ).communicate()

    diff = subprocess.Popen(
        "git diff --name-status origin/main",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        errors="ignore"
    ).communicate()[0]

    diferencas = [x for x in diff.split("\n") if x.strip()]

    return {
        "arquivos_divergentes": diferencas,
        "total": len(diferencas)
    }


# ============================================================
# AUDITORIA PRINCIPAL
# ============================================================

def auditar():
    print("\n🔍 INICIANDO AUDITORIA MAX DO MINDSCAN...")
    inicio = datetime.datetime.now().isoformat()

    # gerar estrutura atual
    atual = gerar_estrutura(ROOT)
    salvar_json(TREE_ATUAL, atual)

    # carregar ref
    if os.path.exists(TREE_REF):
        with open(TREE_REF, "r", encoding="utf-8") as f:
            referencia = json.load(f)
        ref_nova = False
    else:
        print("Primeira execução → criando árvore de referência.")
        referencia = atual
        salvar_json(TREE_REF, referencia)
        ref_nova = True

    # DIFERENCIAL
    adicionados = sorted(set(atual) - set(referencia))
    removidos = sorted(set(referencia) - set(atual))
    alterados = sorted([
        f for f in atual if f in referencia and atual[f]["hash"] != referencia[f]["hash"]
    ])

    # INTEGRIDADE
    integridade = {
        "arquivos_corrompidos": [
            f for f, meta in atual.items()
            if meta["hash"] is None
        ]
    }

    # CÓDIGO
    codigo = auditar_codigo(atual)

    # GITHUB
    github = auditar_github()

    # DECISÃO FINAL
    conclusao = "APROVADO"

    if codigo["erros_sintaticos"]:
        conclusao = "REPROVADO (erros de sintaxe)"

    if integridade["arquivos_corrompidos"]:
        conclusao = "REPROVADO (arquivos corrompidos)"

    if github["total"] > 50:
        conclusao = "REPROVADO (muitas divergências com GitHub)"

    # RELATÓRIO FINAL
    relatorio = {
        "inicio": inicio,
        "estrutura_atual": TREE_ATUAL,
        "estrutura_referencia": TREE_REF,
        "diferencial": {
            "adicionados": adicionados,
            "removidos": removidos,
            "alterados": alterados
        },
        "integridade": integridade,
        "codigo": codigo,
        "github": github,
        "conclusao": conclusao
    }

    salvar_json(RELATORIO, relatorio)

    print("\n✔ Auditoria MAX concluída.")
    print(f"📄 Relatório salvo em: {RELATORIO}")
    print(f"🏁 Resultado final: {conclusao}\n")


if __name__ == "__main__":
    auditar()
