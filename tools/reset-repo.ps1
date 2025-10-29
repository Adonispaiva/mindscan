# tools/reset-repo.ps1
$ErrorActionPreference = "Stop"

Write-Host "🚨 Atenção: Este script deve ser usado com responsabilidade. Prosseguindo..."
Set-Location "$PSScriptRoot/../frontend"

# Lista de arquivos grandes a remover
$arquivosGrandes = @(
  "scripts/backup/*.zip",
  "ts-verificacao.txt"
)

# Cria uma string para o filtro
$filtro = $arquivosGrandes -join " --path "

# Executa a limpeza com git-filter-repo
Write-Host "🧹 Removendo arquivos grandes do histórico Git..."
git filter-repo --path $filtro --invert-paths

# Remove backups temporários do git-filter-repo
Remove-Item .git\refs\original -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item .git\logs\refs\original -Recurse -Force -ErrorAction SilentlyContinue

# Recria a branch remota com push forçado
$branch = "docs/compliance-final"

Write-Host "🌱 Criando nova branch $branch..."
git checkout -b $branch

Write-Host "🚀 Enviando nova branch limpa para o GitHub (force push)..."
git push origin $branch --force

Write-Host "✅ Concluído com sucesso!"
