"""
generate_tree.py
Gera a árvore de diretórios e arquivos do MindScan.

Versão blindada:
- Não modifica nada (somente leitura).
- Ignora venv, backups, .git, __pycache__, node_modules etc.
- Tolera erros de permissão e caminhos muito longos (WinError 206).
"""

import os
import datetime

# Diretórios a serem ignorados na geração da árvore
IGNORED_DIRS = {
    ".git",
    "venv",
    "__pycache__",
    "node_modules",
    ".idea",
    ".vscode",
    "logs",              # logs em geral
}

# Prefixos de diretórios de backup a ignorar
IGNORED_PREFIXES = {
    "_backup_mindscan",
}


def should_ignore_dir(name: str) -> bool:
    """Retorna True se o diretório deve ser ignorado."""
    if name in IGNORED_DIRS:
        return True
    for prefix in IGNORED_PREFIXES:
        if name.startswith(prefix):
            return True
    return False


def generate_tree(root_path: str, prefix: str = ""):
    """
    Gera recursivamente a estrutura de diretórios e arquivos.
    Não modifica NENHUM arquivo — apenas leitura segura.
    """
    entries = []

    try:
        entries = sorted(os.listdir(root_path))
    except PermissionError:
        return [prefix + "[PERMISSION DENIED]\n"]
    except OSError:
        # Caminho muito longo ou outro erro de SO
        return [prefix + "[OS ERROR / PATH TOO LONG]\n"]

    result_lines = []

    for index, entry in enumerate(entries):
        path = os.path.join(root_path, entry)
        is_last = index == len(entries) - 1
        connector = "└── " if is_last else "├── "

        if os.path.isdir(path):
            # Ignora diretórios problemáticos
            if should_ignore_dir(entry):
                result_lines.append(f"{prefix}{connector}{entry}/ [IGNORED]\n")
                continue

            result_lines.append(f"{prefix}{connector}{entry}/\n")
            child_prefix = prefix + ("    " if is_last else "│   ")
            result_lines.extend(generate_tree(path, child_prefix))
        else:
            result_lines.append(f"{prefix}{connector}{entry}\n")

    return result_lines


def save_tree_file(base_path: str) -> str:
    """
    Salva o arquivo .txt dentro de logs/estrutura/
    Criando pastas caso não existam.
    """

    logs_dir = os.path.join(base_path, "logs", "estrutura")
    os.makedirs(logs_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%Hh%Mmin%Ss")
    output_file = os.path.join(logs_dir, f"tree_{timestamp}.txt")

    lines = []
    lines.append("MindScan — Estrutura do Projeto\n")
    lines.append(f"Gerado em: {datetime.datetime.now()}\n")
    lines.append("=" * 60 + "\n\n")

    lines.extend(generate_tree(base_path))

    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(lines)

    return output_file


def main():
    """
    Ponto de entrada oficial.
    Detecta automaticamente a raiz do projeto
    com base na localização deste próprio script.
    """

    script_dir = os.path.dirname(os.path.abspath(__file__))
    # tools -> raiz do projeto
    project_root = os.path.abspath(os.path.join(script_dir, ".."))

    output_file = save_tree_file(project_root)

    print("[OK] Estrutura gerada com sucesso:")
    print(f"     {output_file}")


if __name__ == "__main__":
    main()
