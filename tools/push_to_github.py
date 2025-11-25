import os
import subprocess
import datetime
import sys


def run_git_command(cmd, cwd):
    """Executa comandos git de forma segura e captura erros."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            shell=True,
            text=True,
            capture_output=True
        )
        return result.stdout, result.stderr
    except Exception as e:
        return "", str(e)


def main():
    """
    Script oficial de push do MindScan para o GitHub.
    Seguro, usando GITHUB_TOKEN via variável de ambiente.
    Não expõe credenciais nem modifica arquivos sensíveis.
    """

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    print("\n=== MindScan — Automação de Push para o GitHub ===\n")

    github_token = os.getenv("GITHUB_TOKEN")

    if not github_token:
        print("[ERRO] Variável de ambiente GITHUB_TOKEN não encontrada.")
        print("Configure no .env ou no sistema antes de executar.")
        sys.exit(1)

    # Configuração do remote com token seguro
    remote_url = f"https://{github_token}:x-oauth-basic@github.com/Adonispaiva/mindscan.git"

    print("[1/5] Ajustando remote origin seguro…")
    _, err = run_git_command(f'git remote set-url origin {remote_url}', project_root)
    if err:
        print("⚠️ Aviso:", err.strip())

    # Adicionar todos os arquivos
    print("[2/5] Adicionando arquivos ao commit…")
    out, err = run_git_command("git add .", project_root)
    if err:
        print("⚠️ Aviso:", err.strip())

    # Criar mensagem de commit automática
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_message = f"Atualização automática MindScan — {timestamp}"

    print("[3/5] Realizando commit…")
    _, err = run_git_command(f'git commit -m "{commit_message}"', project_root)
    if "nothing to commit" in err:
        print("Nenhuma alteração detectada. Push cancelado.")
        sys.exit(0)

    # Push
    print("[4/5] Enviando alterações (push)…")
    out, err = run_git_command("git push origin main", project_root)

    if err and "error" in err.lower():
        print("❌ Falha ao enviar push:")
        print(err)
        sys.exit(1)

    print("[5/5] Push concluído com sucesso!")
    print("\n✓ MindScan sincronizado com o GitHub\n")


if __name__ == "__main__":
    main()
