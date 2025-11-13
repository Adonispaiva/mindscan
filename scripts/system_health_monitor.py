# D:\projetos-inovexa\mindscan\scripts\system_health_monitor.py
"""
Monitoramento de saúde do sistema MindScan.
Verifica uso de CPU, RAM e disco, com logs e alertas leves.
"""
import psutil
import json
import datetime
from pathlib import Path

LOG_PATH = Path("D:/projetos-inovexa/mindscan/logs/system_health_{}.json".format(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")))

def monitor():
    data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_usage_percent": psutil.disk_usage("D:/").percent
    }

    status = "ok"
    if data["disk_usage_percent"] > 85 or data["memory_percent"] > 90:
        status = "alert"

    data["status"] = status

    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"[Monitor] Status: {status.upper()} | CPU {data['cpu_percent']}% | RAM {data['memory_percent']}% | Disco {data['disk_usage_percent']}%")

if __name__ == "__main__":
    monitor()
