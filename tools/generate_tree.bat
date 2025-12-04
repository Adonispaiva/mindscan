:: Caminho completo do arquivo
:: D:\projetos-inovexa\mindscan\tools\generate_tree.bat

@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

:: Diretório onde este .bat está
SET "SCRIPT_DIR=%~dp0"

:: Raiz do projeto = pasta acima de tools
FOR %%I IN ("%SCRIPT_DIR%..") DO SET "PROJECT_ROOT=%%~fI"

echo ==========================================
echo      GERANDO ARVORE DO PROJETO MINDSCAN
echo ==========================================
echo Root: %PROJECT_ROOT%
echo.

:: Ativa o venv se existir
IF EXIST "%PROJECT_ROOT%\venv\Scripts\activate.bat" (
    echo [OK] Ativando ambiente virtual...
    call "%PROJECT_ROOT%\venv\Scripts\activate.bat"
) ELSE (
    echo [AVISO] Nenhum ambiente virtual encontrado. Usando Python global.
)

echo.
echo [INFO] Executando generate_tree.py ...
python "%SCRIPT_DIR%generate_tree.py"

echo.
pause
ENDLOCAL
