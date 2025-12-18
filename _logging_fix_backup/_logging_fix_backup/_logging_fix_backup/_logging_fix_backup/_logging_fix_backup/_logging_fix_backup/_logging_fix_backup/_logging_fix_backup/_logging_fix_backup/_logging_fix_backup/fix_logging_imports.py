from pathlib import Path
import shutil

# === CONFIGURAÇÃO ===
ROOT = Path(".")
BACKUP_DIR = Path("_logging_fix_backup")
REPORT_FILE = Path("relatorio_logging_fix_aplicado.txt")

# Padrões PROBLEMÁTICOS (código do projeto)
REPLACEMENTS = {
    "backend.logging": "mindscan_logging",
    "mindscan.logging": "mindscan_logging",
}

# Pastas que NÃO devem ser tocadas
IGNORE_DIRS = {
    ".git",
    "__pycache__",
    "venv",
    ".venv",
    "site-packages",
}

BACKUP_DIR.mkdir(exist_ok=True)

report_lines = []
files_modified = 0

for py_file in ROOT.rglob("*.py"):
    # Ignorar pastas proibidas
    if any(part in IGNORE_DIRS for part in py_file.parts):
        continue

    try:
        original = py_file.read_text(encoding="utf-8", errors="ignore")
        modified = original

        for old, new in REPLACEMENTS.items():
            modified = modified.replace(old, new)

        if modified != original:
            # Backup do arquivo original
            backup_path = BACKUP_DIR / py_file.relative_to(ROOT)
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(py_file, backup_path)

            # Escreve versão corrigida
            py_file.write_text(modified, encoding="utf-8")

            files_modified += 1
            report_lines.append(f"MODIFICADO: {py_file}")

    except Exception as e:
        report_lines.append(f"ERRO: {py_file} -> {e}")

# Salva relatório final
REPORT_FILE.write_text(
    "\n".join(report_lines) +
    f"\n\nTotal de arquivos modificados: {files_modified}",
    encoding="utf-8"
)

print("✔ Correção concluída")
print(f"✔ Arquivos modificados: {files_modified}")
print(f"✔ Backup em: {BACKUP_DIR.resolve()}")
print(f"✔ Relatório: {REPORT_FILE.resolve()}")
