# Arquivo: D:\projetos-inovexa\mindscan\revisor_encoding_global.py
# Status: Novo / Operacional
# Objetivo: Blindar o projeto contra erros de codificação no terminal Windows.

import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def sanear_conteudo(conteudo):
    """Remove emojis e caracteres não-ASCII de strings de log e print."""
    # Procura por padrões de print ou log com caracteres especiais
    def clean_match(match):
        return match.group(0).encode('ascii', 'ignore').decode('ascii')
    
    # Limpa apenas o que está dentro de prints e logs para não afetar lógica de dados
    conteudo = re.sub(r'print\(.*?\)', clean_match, conteudo)
    conteudo = re.sub(r'log_event\(.*?\)', clean_match, conteudo)
    return conteudo

def executar_saneamento():
    print("🧹 Iniciando Saneamento Global de Encoding (MindScan)...")
    formatos_alvo = ['.py', '.md', '.bat']
    contagem = 0

    for root, dirs, files in os.walk(ROOT):
        # Ignora pastas de sistema
        if any(x in root for x in [".git", "__pycache__", ".venv", "node_modules"]):
            continue
            
        for file in files:
            if any(file.endswith(fmt) for fmt in formatos_alvo):
                if file == "revisor_encoding_global.py": continue
                
                path = Path(root) / file
                try:
                    conteudo_original = path.read_text(encoding='utf-8')
                    conteudo_saneado = sanear_conteudo(conteudo_original)
                    
                    if conteudo_original != conteudo_saneado:
                        path.write_text(conteudo_saneado, encoding='utf-8')
                        print(f"✅ Saneado: {path.relative_to(ROOT)}")
                        contagem += 1
                except Exception as e:
                    print(f"⚠️ Erro ao processar {file}: {e}")

    print(f"\n✨ Saneamento concluído. {contagem} ficheiros foram corrigidos.")

if __name__ == "__main__":
    executar_saneamento()