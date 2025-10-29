import os
import subprocess

PASTA_SCRIPTS = r'D:\projetos-inovexa\mindscan\scripts'
SCRIPT_FINAL = 'automacao_mindscan_completa_CORRIGIDO_FINAL.py'
SCRIPT_ANTIGO = 'automacao_mindscan_completa_CORRIGIDO.py'
BAT_FILE = 'executar_mindscan.bat'

# Caminhos completos
caminho_antigo = os.path.join(PASTA_SCRIPTS, SCRIPT_ANTIGO)
caminho_final = os.path.join(PASTA_SCRIPTS, SCRIPT_FINAL)
caminho_bat = os.path.join(PASTA_SCRIPTS, BAT_FILE)

print("🔄 Iniciando automação de ambiente MindScan...")

# 1. Remover script antigo, se existir
if os.path.exists(caminho_antigo):
    os.remove(caminho_antigo)
    print(f"🗑️ Removido: {SCRIPT_ANTIGO}")
else:
    print("✅ Nenhum script antigo para remover.")

# 2. Verificar se o script final está presente
if not os.path.exists(caminho_final):
    print(f"❌ Script final '{SCRIPT_FINAL}' não encontrado! Abortando.")
    exit(1)
else:
    print(f"✅ Script final localizado: {SCRIPT_FINAL}")

# 3. Criar ou atualizar .bat com terminal visível
linha_bat = f'start cmd /k "python {caminho_final}"\n'

try:
    with open(caminho_bat, 'w', encoding='utf-8') as bat:
        bat.write(linha_bat)
    print(f"✅ Arquivo BAT criado/atualizado: {BAT_FILE}")
except Exception as e:
    print(f"❌ Erro ao criar BAT: {e}")
    exit(1)

# 4. Opcional: Executar o script final automaticamente
# subprocess.run(["python", caminho_final])

print("🎉 Ambiente pronto para execução do MindScan.")
