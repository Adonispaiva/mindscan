<#
.SYNOPSIS
  Script oficial de build e deploy do MindScan v3.0 (Inovexa Software)
.DESCRIPTION
  Permite alternar entre modo de desenvolvimento e produção.
  Executa validações, logs e commits automáticos no branch ativo.
#>

param(
    [ValidateSet("dev", "prod")]
    [string]$mode = "dev"
)

Write-Host "🧠 Iniciando build do MindScan (modo: $mode)..." -ForegroundColor Cyan

# Caminho base do projeto
$root = "D:\projetos-inovexa\mindscan"
Set-Location $root

# Verifica Docker
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker não encontrado. Instale o Docker Desktop e tente novamente." -ForegroundColor Red
    exit 1
}

# Interrompe containers ativos
Write-Host "🧹 Parando containers existentes..." -ForegroundColor Yellow
docker compose down

# Seleciona compose conforme modo
if ($mode -eq "prod") {
    $compose = "infra\docker-compose.prod.yml"
    $tag = "mindscan:3.0-stable"
    Write-Host "🏗️  Build completo de produção..." -ForegroundColor Cyan
    docker compose -f $compose build
    docker compose -f $compose up -d
}
else {
    $compose = "infra\docker-compose.yml"
    $tag = "mindscan:dev"
    Write-Host "🔧 Ambiente de desenvolvimento ativado..." -ForegroundColor Blue
    docker compose -f $compose up -d
}

# Log final
Write-Host "`n✅ Containers em execução:" -ForegroundColor Green
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Validação do serviço principal
Start-Sleep -Seconds 5
$response = curl http://localhost:8000/health -UseBasicParsing -ErrorAction SilentlyContinue

if ($response.StatusCode -eq 200) {
    Write-Host "✅ MindScan operacional em http://localhost:8000" -ForegroundColor Green
}
else {
    Write-Host "⚠️  MindScan não respondeu no healthcheck inicial." -ForegroundColor Yellow
}

# Commit automatizado
Write-Host "`n💾 Registrando build no Git..." -ForegroundColor Cyan
git add .
git commit -m "🚀 Build $mode executado via build_mindscan.ps1 em $(Get-Date -Format 'dd/MM/yyyy HH:mm:ss')"
git push origin HEAD

# Tag opcional para builds de produção
if ($mode -eq "prod") {
    $tagName = "v3.0-stable"
    git tag -a $tagName -m "MindScan v3.0 build estável"
    git push origin $tagName
    Write-Host "🏁 Build de produção registrado e tag $tagName publicada." -ForegroundColor Green
}

Write-Host "`n🎯 Processo concluído com sucesso." -ForegroundColor Green
