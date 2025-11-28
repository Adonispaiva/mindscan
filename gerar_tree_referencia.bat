@echo off
setlocal

echo ================================================
echo       GERANDO TREE_REFERENCIA DO MINDSCAN
echo ================================================
echo.

set ROOT=%~dp0
python "%ROOT%tools\gerar_tree_referencia.py"

echo.
echo ================================================
echo       ARVORE DE REFERENCIA GERADA
echo ================================================
echo.

pause
exit /b
