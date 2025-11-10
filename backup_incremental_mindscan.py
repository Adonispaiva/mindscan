import os
import zipfile
from datetime import datetime
from pathlib import Path

# Configurações
pasta_origem = Path(__file__).resolve().parent.parent
pasta_destino = pasta_origem / "scripts" / "backup"
pasta_destino.mkdir(parents=True, exist_ok=True)

qtde_max_backups = 3  # Quantidade máxima de backups a manter
hora_atual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
nome_arquivo_zip = f"mindscan_backup_{hora_atual}.zip"
caminho_zip = pasta_destino / nome_arquivo_zip

log_path = pasta_origem / "scripts" / "logs"
log_path.mkdir(parents=True, exist_ok=True)
log_file = log_path / f"log_backup_{hora_atual}.txt"

# Lista de pastas e arquivos a ignorar no backup
ignorar = {"node_modules", "backup", ".git", "__pycache__", ".env"}

def zipar_pasta(origem, zipf):
    for pasta_atual, subpastas, arquivos in os.walk(origem):
        if any(ign in Path(pasta_atual).parts for ign in ignorar):
            continue
        for arquivo in arquivos:
            caminho_completo = Path(pasta_atual) / arquivo
            rel_path = caminho_completo.relative_to(origem)
            zipf.write(caminho_completo, rel_path)

def aplicar_politica_de_retencao():
    backups = sorted(pasta_destino.glob("mindscan_backup_*.zip"), key=os.path.getmtime, reverse=True)
    backups_a_excluir = backups[qtde_max_backups:]
    with open(log_file, "a", encoding="utf-8") as log:
        for arquivo in backups_a_excluir:
            try:
                os.remove(arquivo)
                log.write(f"[{datetime.now()}] Backup removido: {arquivo.name}\n")
            except Exception as e:
                log.write(f"[{datetime.now()}] Erro ao remover {arquivo.name}: {str(e)}\n")

# Criar o backup zipado
with zipfile.ZipFile(caminho_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
    zipar_pasta(pasta_origem, zipf)

# Registrar log de criação
with open(log_file, "w", encoding="utf-8") as log:
    log.write(f"[{datetime.now()}] Backup criado: {nome_arquivo_zip}\n")

# Aplicar retenção
aplicar_politica_de_retencao()
