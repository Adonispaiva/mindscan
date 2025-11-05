@echo off
echo === Removendo arquivo grande do Git e recriando o histórico ===

REM Substitua o caminho do arquivo a remover abaixo
set ARQUIVO_ALVO=scripts/backup/mindscan_backup_20251014_082639.zip

REM Filtra o repositório e remove o arquivo
git filter-branch --force --index-filter "git rm --cached --ignore-unmatch %ARQUIVO_ALVO%" --prune-empty --tag-name-filter cat -- --all

REM Remove referências antigas
git for-each-ref --format="%%(refname)" refs/original/ | for /f "delims=" %%r in ('more') do git update-ref -d %%r

REM Limpa e comprime o repositório
git reflog expire --expire=now --all
git gc --prune=now --aggressive

REM Faz o push forçado para o repositório remoto
git push origin --force --all
git push origin --force --tags

echo === Concluído com sucesso ===
pause
