
import subprocess

def run_docker_compose():
    try:
        print("🔧 Iniciando build com Docker Compose...")
        subprocess.run(["docker-compose", "up", "--build"], check=True)
    except subprocess.CalledProcessError as e:
        print("❌ Erro ao executar Docker Compose:", e)

if __name__ == "__main__":
    run_docker_compose()
