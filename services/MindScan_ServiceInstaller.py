"""
🧩 MindScan Service Installer — Template v5.8
Autor: Inovexa Software
Função: Registra e instala o MindScan SentinelDaemon como serviço do sistema.
"""

import os, sys, subprocess, platform

SERVICE_NAME = "MindScanSentinel"
SCRIPT_PATH = r"D:\MindScan\core\MindScan_SentinelDaemon.py"

def install_service():
    if platform.system() == "Windows":
        cmd = [
            "sc", "create", SERVICE_NAME,
            "binPath=", f"python \"{SCRIPT_PATH}\"",
            "start=", "auto"
        ]
        subprocess.run(cmd, shell=True)
        print("Serviço instalado com sucesso.")
    elif platform.system() == "Linux":
        service_file = f"""/etc/systemd/system/{SERVICE_NAME}.service"""
        content = f"""[Unit]
Description=MindScan Sentinel Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 {SCRIPT_PATH}
Restart=always
User=root

[Install]
WantedBy=multi-user.target
"""
        with open(service_file, "w") as f: f.write(content)
        subprocess.run(["systemctl", "enable", SERVICE_NAME])
        subprocess.run(["systemctl", "start", SERVICE_NAME])
        print("Serviço registrado com sucesso.")
    else:
        print("Sistema operacional não suportado.")

if __name__ == "__main__":
    install_service()
