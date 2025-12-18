from pathlib import Path

ROOT = Path(".")
OUTPUT = Path("relatorio_logging_conflicts.txt")

patterns = [
    "from logging import",
    "import logging",
    "mindscan_logging",
    "mindscan_logging",
]

lines_out = []

for file in ROOT.rglob("*.py"):
    try:
        content = file.read_text(encoding="utf-8", errors="ignore")
        for i, line in enumerate(content.splitlines(), 1):
            for p in patterns:
                if p in line:
                    lines_out.append(f"{file}:{i}: {line.strip()}")
    except Exception:
        pass

OUTPUT.write_text("\n".join(lines_out), encoding="utf-8")

print(f"Relatório salvo em: {OUTPUT.resolve()}")
