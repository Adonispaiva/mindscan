import os
import subprocess
import datetime
from generate_tree import main as generate_tree_main

def run_git(cmd, cwd):
    result = subprocess.run(cmd, cwd=cwd, shell=True, text=True, capture_output=True)
    return result.stdout, result.stderr

def sync_all():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))

    print("\n=== MindScan — Sync All (Tree + Commit + Push) ===\n")

    # 1) Generate tree
    print("[1/4] Gerando árvore...")
    generate_tree_main()

    # 2) Git add
    print("[2/4] Adicionando arquivos...")
    run_git("git add .", project_root)

    # 3) Git commit
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"Sync All MindScan — {ts}"
    print("[3/4] Commitando...")
    out, err = run_git(f"git commit -m '{msg}'", project_root)
    if "nothing to commit" in err:
        print("Nenhuma alteração detectada. Encerrando.")
        return

    # 4) Git push
    print("[4/4] Enviando push...")
    out, err = run_git("git push origin main", project_root)
    if err and "error" in err.lower():
        print("Erro ao enviar push:\n", err)
    else:
        print("Sync All concluído com sucesso!")

if __name__ == "__main__":
    sync_all()
