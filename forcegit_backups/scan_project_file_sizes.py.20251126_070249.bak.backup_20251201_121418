import os


def scan_project_sizes(root_path: str, report_path: str):
    entries = []
    for dirpath, _, filenames in os.walk(root_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                size = os.path.getsize(fp)
                entries.append((fp, size))
            except Exception:
                continue

    entries.sort(key=lambda x: x[0])

    with open(report_path, "w", encoding="utf-8") as rpt:
        rpt.write("RELATÓRIO DE TAMANHO DE ARQUIVOS DO MINDSCAN\n")
        rpt.write("=" * 60 + "\n\n")
        for path, size in entries:
            rpt.write(f"{path} -> {size} bytes\n")


if __name__ == "__main__":
    # Ajuste o caminho raiz do MindScan conforme sua estrutura local
    ROOT = r"D:\MindScan"
    REPORT = r"D:\\projetos-inovexa\\mindscan_rebuild\\logs\\estrutura\\relatorio_tamanho_arquivos.txt"