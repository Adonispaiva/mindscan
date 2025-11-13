@echo off
title MindScan - Validador Final
cd /d D:\projetos-inovexa\mindscan\scripts

python recovery_manager.py
python post_purge_validator.py
python system_health_monitor.py
python integrity_scanner.py
python maintenance_reporter.py
python alert_watcher.py

echo.
echo ====== CICLO COMPLETO FINALIZADO ======
pause
