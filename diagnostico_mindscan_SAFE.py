import subprocess

def run(cmd, shell=True):
    print(f"Executando: {cmd}")
    try:
        output = subprocess.check_output(cmd, shell=shell, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
        print(output.strip())
    except subprocess.CalledProcessError as e:
        print("Erro:")
        print(e.output.strip())

print("Iniciando diagnóstico do container 'mindscan-api'...\n")

# Verifica se o container está rodando
print("Verificando status do container...")
run("docker inspect -f '{{.State.Status}}' mindscan-api")

# Exibe logs recentes
print("\nLogs recentes:")
run("docker logs --tail 20 mindscan-api")

# Verifica shell e escuta na porta 8000
print("\nVerificando escuta na porta 8000 dentro do container...")
shell = None
for s in ["bash", "sh"]:
    result = subprocess.run(f"docker exec mindscan-api which {s}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    if result.returncode == 0:
        shell = s
        break

if shell:
    run(f'docker exec mindscan-api {shell} -c "netstat -tuln | grep 8000 || echo Nenhum processo escutando na porta 8000."')
else:
    print("Nenhum shell disponível detectado no container.")

# Verifica dependências externas
print("\nVerificando dependências externas (mindscan-db, mindscan-redis)...")
for dep in ["mindscan-db", "mindscan-redis"]:
    result = subprocess.run(f"docker inspect -f '{{{{.State.Status}}}}' {dep}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    if result.stdout.strip() != "running":
        print(f"Iniciando dependência: {dep}")
        run(f"docker start {dep}")
    else:
        print(f"{dep} já está em execução.")

# Reinicia o backend
print("\nReiniciando o container 'mindscan-api'...")
run("docker restart mindscan-api")

print("\nDiagnóstico concluído. Tente acessar: http://localhost:8000")
