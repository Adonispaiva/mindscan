# Script: clean‑repo.ps1
# Finalidade: remover arquivos grandes do histórico Git, atualizar ignore, e fazer push do branch compliance-final.

Write-Host "⚠️ ATENÇÃO: Este script reescreve o histórico Git. Continue apenas se estiver pronto e for único desenvolvedor."

# 1. Ir para o diretório do repositório
Set-Location 'D:\projetos-inovexa\mindscan\frontend'

# 2. Atualizar .gitignore para impedir futuros commits de arquivos grandes
Add-Content -Path .gitignore -Value "`n# Ignorar backups grandes`n/scripts/backup/*.zip`nts-verificacao.txt"

git add .gitignore
git commit -m "[cleanup] Atualiza .gitignore para ignorar arquivos grandes"

# 3. Remover os arquivos grandes do histórico
# Usando git filter-branch para remoção
git filter-branch --force --index-filter "git rm --cached --ignore-unmatch scripts/backup/*.zip ts-verificacao.txt" --prune-empty --tag-name-filter cat -- --all

# 4. Expirar e limpar o reflog e objetos
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# 5. Criar branch de compliance-final (se ainda não existir)
if (-not (git branch --list docs/compliance-final)) {
    git checkout -b docs/compliance-final
} else {
    git checkout docs/compliance-final
}

# 6. Push forçado do branch reformulado
git push --set-upstream origin docs/compliance-final --force

# 7. Criar PR automaticamente (se estiver utilizando GitHub CLI)
if (Get-Command gh -ErrorAction SilentlyContinue) {
    gh pr create --base main --head docs/compliance-final --title "[Compliance] v1.6 Supercola + Testes completos" --body "Entrega automatizada do ambiente de testes + limpeza de histórico + compliance."
} else {
    Write-Host "GitHub CLI (gh) não encontrado. Por favor crie o PR manualmente usando GitHub."
}

Write-Host "✅ Script concluído. Verifique no GitHub e instruções de clonagem limpa para colaboradores."
