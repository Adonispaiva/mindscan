import os
import shutil
import filecmp

# Caminhos
pasta_raiz = os.path.abspath('.')
pasta_duplicada = os.path.join(pasta_raiz, 'projetos-inovexa', 'mindscan')

# Arquivos que o script anterior encontrou com mesmo nome mas conteúdo diferente
arquivos_conflitantes = [
    'docker-compose.yml',
    os.path.join('backend', 'main.py'),
    os.path.join('backend', 'requirements.txt'),
]

def comparar_arquivos():
    for caminho in arquivos_conflitantes:
        origem = os.path.join(pasta_raiz, caminho)
        duplicado = os.path.join(pasta_duplicada, caminho)
        if not (os.path.exists(origem) and os.path.exists(duplicado)):
            print(f"[!] Arquivo ausente para comparação: {caminho}")
            return False
        if not filecmp.cmp(origem, duplicado, shallow=False):
            print(f"[⚠️] Arquivo diferente detectado: {caminho}")
            return False
    return True

def remover_pasta_duplicada():
    if os.path.exists(pasta_duplicada):
        print(f"[🗑️] Removendo pasta duplicada: {pasta_duplicada}")
        shutil.rmtree(os.path.join(pasta_raiz, 'projetos-inovexa'))
        print("[✅] Pasta duplicada removida com sucesso.")
    else:
        print("[ℹ️] Pasta duplicada já não existe.")

# --- Execução ---
print("[🔍] Verificando se é seguro apagar a duplicata...")

if comparar_arquivos():
    remover_pasta_duplicada()
else:
    print("[⛔] Remoção cancelada. Existem arquivos divergentes.")
    print("[💡] Revise os arquivos listados acima antes de continuar.")
