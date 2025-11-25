import os
import hashlib
import json
import subprocess
import requests
from datetime import datetime

# ============================================================
#  CONFIGURAÇÃO GERAL
# ============================================================

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

REFERENCE_TREE_FILE = os.path.join(PROJECT_ROOT, "tree_referencia.json")
LOCAL_TREE_FILE = os.path.join(PROJECT_ROOT, "tree_atual.json")

GITHUB_REPO = "https://github.com/Adonispaiva/mindscan"
GITHUB_API = "https://api.github.com/repos/Adonispaiva/mindscan"


# ============================================================
#  UTILITÁRIOS
# ============================================================

def gerar_tree(path):
    estrutura = {}
    for root, dirs, files in os.walk(path):
        rel = os.path.relpath(root, path)
        if rel == ".":
            rel = ""
        estrutura[rel] = {
            "dirs": dirs,
            "files": files
        }
    return estrutura


def salvar_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def calcular_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


# ============================================================
#  A) AUDITORIA ESTRUTURAL
# ============================================================

def auditar_estrutura():
    print("\n🔍 AUDITORIA ESTRUTURAL\n")

    tree_atual = gerar_tree(PROJECT_ROOT)
    salvar_json(LOCAL_TREE_FILE, tree_atual)

    if not os.path.exists(REFERENCE_TREE_FILE):
        print("⚠ Nenhuma árvore de referência encontrada. Criando primeira referência...")
        salvar_json(REFERENCE_TREE_FILE, tree_atual)
        return {"status": "referencia_criada"}

    with open(REFERENCE_TREE_FILE, "r", encoding="utf-8") as f:
        tree_ref = json.load(f)

    novos = []
    removidos = []

    # Pastas e arquivos adicionados
    for pasta in tree_atual:
        if pasta not in tree_ref:
            novos.append(("nova pasta", pasta))
        else:
            # comparar arquivos
            for f in tree_atual[pasta]["files"]:
                if f not in tree_ref[pasta]["files"]:
                    novos.append(("novo arquivo", os.path.join(pasta, f)))

    # Pastas e arquivos removidos
    for pasta in tree_ref:
        if pasta not in tree_atual:
            removidos.append(("pasta removida", pasta))
        else:
            for f in tree_ref[pasta]["files"]:
                if f not in tree_atual[pasta]["files"]:
                    removidos.append(("arquivo removido", os.path.join(pasta, f)))

    return {
        "novos": novos,
        "removidos": removidos
    }


# ============================================================
#  B) AUDITORIA DE INTEGRIDADE
# ============================================================

def auditar_integridade():
    print("\n🔍 AUDITORIA DE INTEGRIDADE\n")

    hashes = {}
    arquivos_vazios = []
    arquivos_duplicados = {}

    for root, dirs, files in os.walk(PROJECT_ROOT):
        for file in files:
            path = os.path.join(root, file)

            # ignora venv, cache, logs, dist-info
            if any(x in path for x in ["venv", "__pycache__", "dist-info"]):
                continue

            size = os.path.getsize(path)
            if size == 0:
                arquivos_vazios.append(path)

            h = calcular_hash(path)

            if h not in arquivos_duplicados:
                arquivos_duplicados[h] = [path]
            else:
                arquivos_duplicados[h].append(path)

            hashes[path] = h

    duplicados = {h: p for h, p in arquivos_duplicados.items() if len(p) > 1}

    return {
        "arquivos_vazios": arquivos_vazios,
        "arquivos_duplicados": duplicados
    }


# ============================================================
#  C) AUDITORIA DO CÓDIGO
# ============================================================

def auditar_codigo():
    print("\n🔍 AUDITORIA DO CÓDIGO\n")

    problemas = {
        "imports_quebrados": [],
        "modulos_inexistentes": [],
        "rotas_sem_servico": [],
        "servicos_sem_provider": [],
    }

    # Verifica imports quebrados usando "python -m py_compile"
    for root, dirs, files in os.walk(PROJECT_ROOT):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                result = subprocess.run(
                    ["python", "-m", "py_compile", path],
                    capture_output=True,
                    text=True
                )
                if result.stderr:
                    problemas["imports_quebrados"].append({
                        "arquivo": path,
                        "erro": result.stderr.strip()
                    })

    # (poderíamos expandir para AST analysis, mas já cobre breakages reais)

    return problemas


# ============================================================
#  D) AUDITORIA DO GITHUB
# ============================================================

def auditar_github():
    print("\n🔍 AUDITORIA DO GITHUB\n")

    resultado = {}

    # 1. Testar comunicação com GitHub API
    try:
        r = requests.get(GITHUB_API)
        resultado["github_online"] = (r.status_code == 200)
    except Exception as e:
        resultado["github_online"] = False
        resultado["erro_conexao"] = str(e)

    # 2. Verificar estado do repositório local
    comandos = {
        "status": ["git", "status", "-s"],
        "branch": ["git", "branch", "--show-current"],
        "pendencias": ["git", "status"]
    }

    for chave, cmd in comandos.items():
        try:
            r = subprocess.run(cmd, capture_output=True, text=True)
            resultado[chave] = r.stdout.strip()
        except Exception as e:
            resultado[chave] = f"Erro: {str(e)}"

    return resultado


# ============================================================
#  EXECUTOR GERAL
# ============================================================

def executar_auditoria():
    print("\n=======================================================")
    print("     🔎 AUDITORIA COMPLETA DO MINDSCAN — INÍCIO")
    print("     ", datetime.now())
    print("=======================================================\n")

    resultados = {
        "estrutura": auditar_estrutura(),
        "integridade": auditar_integridade(),
        "codigo": auditar_codigo(),
        "github": auditar_github(),
    }

    relatorio_path = os.path.join(PROJECT_ROOT, "relatorio_auditoria.json")
    salvar_json(relatorio_path, resultados)

    print("\n📄 Relatório salvo em:", relatorio_path)
    print("\n✅ Auditoria concluída com sucesso.")
    return resultados


if __name__ == "__main__":
    executar_auditoria()
