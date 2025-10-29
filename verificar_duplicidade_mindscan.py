import os
import filecmp

def listar_arquivos_recursivamente(diretorio):
    arquivos = []
    for raiz, _, nomes in os.walk(diretorio):
        for nome in nomes:
            caminho_completo = os.path.relpath(os.path.join(raiz, nome), diretorio)
            arquivos.append(caminho_completo)
    return sorted(arquivos)

def comparar_diretorios(dir1, dir2):
    print("🟡 Comparando diretórios...\n")
    arquivos_dir1 = listar_arquivos_recursivamente(dir1)
    arquivos_dir2 = listar_arquivos_recursivamente(dir2)

    total = len(arquivos_dir1)
    duplicados = []
    diferentes = []

    for i, arquivo in enumerate(arquivos_dir1, 1):
        print(f"[{i}/{total}] Verificando: {arquivo}")

        caminho1 = os.path.join(dir1, arquivo)
        caminho2 = os.path.join(dir2, arquivo)

        if arquivo in arquivos_dir2:
            try:
                if filecmp.cmp(caminho1, caminho2, shallow=False):
                    duplicados.append(arquivo)
                else:
                    diferentes.append(arquivo)
            except Exception as e:
                print(f"Erro ao comparar '{arquivo}': {e}")

    print("\n✅ Verificação concluída.\n")
    print(f"Arquivos idênticos encontrados: {len(duplicados)}")
    print(f"Arquivos com diferenças: {len(diferentes)}\n")

    if diferentes:
        print("📌 Arquivos diferentes:")
        for dif in diferentes:
            print(f"  - {dif}")
    else:
        print("🎉 Nenhuma diferença detectada entre os diretórios.")

if __name__ == "__main__":
    raiz = os.getcwd()
    dir1 = os.path.join(raiz, "projetos-inovexa", "mindscan")
    dir2 = raiz

    comparar_diretorios(dir1, dir2)
