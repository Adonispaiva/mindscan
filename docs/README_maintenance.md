# Política de Manutenção Automática — MindScan

## Scripts Principais
| Script | Função |
|---------|---------|
| `backup_manager.py` | Controla retenção, arquivamento e purga conforme `backup_policy.json`. |
| `backup_purger_progressive.py` | Purga com barra de progresso (manual). |
| `backup_purger.py` | Purga simples (fallback). |
| `auto_orchestrator_v2.py` | Inclui manutenção automática no pipeline geral. |

## Política JSON
- `keep_last`: backups mantidos.
- `retention_days`: tempo mínimo.
- `max_backup_dir_gb`: tamanho máximo.
- `purge_archive_after_days`: purga automática.
- `force_purge_when_single_file_over_gb`: purga se muito grande.
- `dry_run`: simulação.
- `progressive_hash`: exibe barra de progresso.

## Execução manual
```powershell
cd D:\projetos-inovexa\mindscan\scripts
python backup_manager.py --dry-run
python backup_manager.py
