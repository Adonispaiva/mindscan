# Define caminhos
$verificacao = "ts-verificacao.txt"
$backup = "backup_restore/mindscan_backup_2025-10-14_08-43-46.zip"
$remote = "https://github.com/seu-usuario/seu-repo.git"

# Etapa 1 - Executa git-filter-repo
python git-filter-repo.py `
    --path $verificacao `
    --path $backup `
    --force

# Etapa 2 - Confirma limpeza
git count-objects -vH

# Etapa 3 - Redefine origem remota
git remote remove origin
git remote add origin $remote

# Etapa 4 - Push forçado
git push -u origin main --force
