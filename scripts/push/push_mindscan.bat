@echo off
:: ===============================================
:: Inovexa Fábrica - Push Automático MindScan v4.1
:: ===============================================
title Inovexa MindScan – Push Automático v4.1
color 0A
setlocal EnableDelayedExpansion

cd /d D:\projetos-inovexa\mindscan

:: 1) (Opcional) habilitar UTF-8 no console; seguro manter mesmo usando ASCII no console do Python
chcp 65001 >nul

:: 2) Não redirecionar stdout/err do Python para o mesmo log do script
::    O logger interno já grava backup\push_runtime.log com retry anti-lock.
echo [INICIO - %date% %time%] Execucao v4.1

:: 3) Verificação do arquivo antes de executar
if not exist "tools\push_sync_mindscan_v4_1.py" (
  echo [ERRO] Arquivo tools\push_sync_mindscan_v4_1.py nao encontrado.
  pause & exit /b 1
)

:: 4) Execucao do script final
python tools\push_sync_mindscan_v4_1.py
set CODE=%ERRORLEVEL%

echo.
if "%CODE%"=="0" (
  echo ✅ Push executado com sucesso.
  for /f %%f in ('dir /b /od backup\manifest_push_*.html') do set LASTREPORT=%%f
  if exist "backup\!LASTREPORT!" start "" "backup\!LASTREPORT!"
) else (
  echo ❌ Erro durante a execucao. Verifique "backup\push_runtime.log".
)

echo.
echo --------------------------------------------------------
echo Processo concluido. Pressione qualquer tecla para sair.
echo --------------------------------------------------------
pause >nul
endlocal
exit /b %CODE%
