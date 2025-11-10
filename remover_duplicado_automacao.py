import os
import shutil
import filecmp
from datetime import datetime

duplicata = os.path.join("projetos-inovexa")
original = os.getcwd()
log_dir = os.path.join("scripts", "logs")
os.makedirs(log_dir, exist_ok=True)

log_path = os.path.join(
    log_dir, f"remocao_duplicata_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.txt"
)

def comparar_e_logar_diferencas(dir1, dir2, log_file):
    with open(log_file, "w", encoding="utf-8") as log:
        log.write(f"[{datetime.now()}] Comparando '{dir1}' com '{dir2}'...\n\n")

        cmp = filecmp.dircmp(dir1, dir2)

        if cmp.left_only:
            log.write("Arquivos/pastas só na duplicata:\n")
            for item in cmp.left_only:
                log.write(f"  - {item}\n")
            log.write("\n")

        if cmp.right_only:
            log.write("Arquivos/pastas só na original:\n")
            for item in cmp.right_only:
                log.write(f"  - {item}\n")
            log.write("\n")

        if cmp.diff_files:
            log.write("Arquivos com conteúdo diferente:\n")
            for item in cmp.diff_files:
                log.write(f"  - {item}\n")
            log.write("\n")

        log.write("Remoção automatizada autorizada.\n")

def remover_duplicata(caminho, log_file):
    if os.path.exists(caminho):
        shutil.rmtree(caminho)
        with open(log_file, "a", encoding="utf-8") as log:
            log.write(f"[✔] Pasta '{caminho}' removida com sucesso.\n")
        print(f"[✔] Pasta '{caminho}' foi removida.")
    else:
        print(f"[i] Pasta '{caminho}' não encontrada.")

# Executa
print(f"[●] Iniciando verificação e remoção automática da duplicata...")
comparar_e_logar_diferencas(duplicata, original, log_path)
remover_duplicata(duplicata, log_path)
print(f"[✓] Log salvo em: {log_path}")
