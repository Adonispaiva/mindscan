import os
import datetime

def generate_tree(root_path, prefix=""):
    """
    Gera recursivamente a estrutura de diretórios e arquivos.
    Não modifica NENHUM arquivo — apenas leitura segura.
    """

    entries = []

    try:
        entries = sorted(os.listdir(root_path))
    except PermissionError:
        return [prefix + "[PERMISSION DENIED]\n"]

    result_lines = []

    for entry in entries:
        path = os.path.join(root_path, entry)
        connector = "├── "

        if entry == entries[-1]:
            connector = "└── "

        if os.path.isdir(path):
            result_lines.append(f"{prefix}{connector}{entry}/\n")
            result_lines.extend(
                generate_tree(path, prefix + ("    " if connector == "└── " else "│   "))
            )
        else:
            result_lines.append(f"{prefix}{connector}{entry}\n")

    return result_lines


def save_tree_file(base_path):
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
    project_root = os.path.abspath(os.path.join(script_dir, ".."))

    output_file = save_tree_file(project_root)

    print(f"[OK] Estrutura gerada com sucesso:")
    print(f"     {output_file}")


if __name__ == "__main__":
    main()
