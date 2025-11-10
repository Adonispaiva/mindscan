<#
╔══════════════════════════════════════════════════════╗
║     VERIFICAÇÃO PÓS-AUDITORIA — MINDSCAN v2.0        ║
║     Padrão Disciplinar Inovexa Software              ║
╚══════════════════════════════════════════════════════╝
#>

Write-Host "`n🔍 Iniciando verificação da auditoria técnica..." -ForegroundColor Cyan

# Caminho base do repositório
$repoPath = "D:\projetos-inovexa\mindscan"
Set-Location $repoPath

# 1️⃣ Verifica se o arquivo de auditoria existe
$auditFile = "docs\relatorios\auditoria_git_mindscan_v2.0.md"
if (Test-Path $auditFile) {
    Write-Host "✅ Arquivo de auditoria localizado: $auditFile" -ForegroundColor Green
} else {
    Write-Host "❌ Arquivo de auditoria NÃO encontrado em $auditFile" -ForegroundColor Red
    exit 1
}

# 2️⃣ Atualiza informações do repositório
git fetch --tags > $null 2>&1

# 3️⃣ Verifica existência da tag v2.0-auditoria
$tagExists = git tag | Select-String "v2.0-auditoria"
if ($tagExists) {
    Write-Host "🏷️ Tag 'v2.0-auditoria' detectada localmente." -ForegroundColor Green
} else {
    Write-Host "❌ Tag 'v2.0-auditoria' não encontrada." -ForegroundColor Red
    exit 1
}

# 4️⃣ Verifica se a tag está sincronizada com o remoto
$remoteTag = git ls-remote --tags origin | Select-String "v2.0-auditoria"
if ($remoteTag) {
    Write-Host "🌐 Tag 'v2.0-auditoria' confirmada no repositório remoto." -ForegroundColor Green
} else {
    Write-Host "⚠️ Tag ainda não sincronizada no GitHub. Execute: git push origin v2.0-auditoria" -ForegroundColor Yellow
}

# 5️⃣ Confere commit de auditoria no histórico recente
$auditCommit = git log -n 10 --pretty=oneline | Select-String "Auditoria Técnica Inovexa v2.0"
if ($auditCommit) {
    Write-Host "🧠 Commit de auditoria encontrado no histórico recente." -ForegroundColor Green
} else {
    Write-Host "❌ Commit de auditoria não localizado nos últimos 10 commits." -ForegroundColor Red
    exit 1
}

Write-Host "`n✅ VERIFICAÇÃO CONCLUÍDA — Auditoria MindScan v2.0 está íntegra e rastreável." -ForegroundColor Cyan
