# auto_clean_logs.ps1 — Inovexa Maintenance Script
# Projeto: MindScan v3.0-stable
# Objetivo: Limpeza e rotação automática de logs e caches

$ErrorActionPreference = 'Stop'
$basePath = "D:\\MindScan"
$logDir = "$basePath\\logs"
$auditDir = "$basePath\\data\\auditoria_mindscan"
$cacheDir = "$basePath\\data\\synmind_cache"
$daysToKeep = 7
$logFile = "$basePath\\data\\auditoria_mindscan\\clean_logs_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"

function Write-Log {
    param([string]$message)
    $timestamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
    $entry = "[$timestamp] $message"
    Add-Content -Path $logFile -Value $entry
    Write-Host $entry
}

Write-Log "🚀 Iniciando rotina de limpeza de logs e caches..."

try {
    $targets = @($logDir, $auditDir, $cacheDir)

    foreach ($dir in $targets) {
        if (Test-Path $dir) {
            Write-Log "Verificando: $dir"
            $oldFiles = Get-ChildItem -Path $dir -Recurse -File | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-$daysToKeep) }
            $count = ($oldFiles | Measure-Object).Count

            if ($count -gt 0) {
                Write-Log "🧹 Encontrados $count arquivos antigos — compactando..."
                $archive = "$dir\\archive_$(Get-Date -Format 'yyyyMMdd_HHmmss').zip"
                Compress-Archive -Path $oldFiles.FullName -DestinationPath $archive -Force
                Write-Log "📦 Arquivos compactados em: $archive"

                Write-Log "Removendo arquivos originais..."
                $oldFiles | Remove-Item -Force -ErrorAction SilentlyContinue
                Write-Log "✅ Limpeza concluída para: $dir"
            }
            else {
                Write-Log "Nenhum arquivo antigo encontrado em: $dir"
            }
        }
        else {
            Write-Log "⚠️ Diretório não encontrado: $dir"
        }
    }

    Write-Log "Rotina concluída com sucesso."
    exit 0
}
catch {
    Write-Log "❌ Erro durante a limpeza: $($_.Exception.Message)"
    exit 2
}