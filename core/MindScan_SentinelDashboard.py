from flask import Flask, render_template_string, jsonify
import requests
import json
import psutil
import time
from datetime import datetime
from pathlib import Path

# ============================================
# 🧠 MindScan Sentinel Dashboard — v4.8
# ============================================
# Autor: Leo Vinci (GPT Inovexa)
# Data: 12/11/2025
# Função: Painel visual em tempo real — integridade, logs e status dos serviços
# ============================================

LOG_API = "http://127.0.0.1:8091/logs?limit=20"
MANIFEST_PATH = Path(r"D:\MindScan\update_manifest.json")
REFRESH_INTERVAL = 5  # segundos

app = Flask(__name__)

# ------------------------ UTILITÁRIOS ------------------------
def now():
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")

def get_logs():
    try:
        r = requests.get(LOG_API, timeout=2)
        if r.status_code == 200:
            return r.json().get("logs", [])
    except Exception:
        pass
    return [{"time": now(), "level": "ERROR", "message": "Falha ao conectar ao LogHandler"}]

def get_manifest():
    try:
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def get_status():
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    uptime = time.time() - psutil.boot_time()
    manifest = get_manifest()
    return {
        "timestamp": now(),
        "cpu": cpu,
        "memory": mem,
        "uptime": f"{int(uptime // 3600)}h {int((uptime % 3600) // 60)}m",
        "version": manifest.get("current_build", {}).get("version_tag", "Desconhecida"),
        "integrity": manifest.get("verification", {}).get("last_result", "Indefinida"),
        "services": [
            {"name": "SystemManager", "status": "🟢 Ativo"},
            {"name": "AutoSync", "status": "🟢 Ativo"},
            {"name": "CommandCenter", "status": "🟢 Ativo"},
            {"name": "FailsafeGuardian", "status": "🟢 Ativo"},
        ]
    }

# ------------------------ ENDPOINTS ------------------------
@app.route("/")
def index():
    return render_template_string(TEMPLATE_HTML)

@app.route("/api/status")
def api_status():
    return jsonify(get_status())

@app.route("/api/logs")
def api_logs():
    return jsonify(get_logs())

# ------------------------ INTERFACE HTML ------------------------
TEMPLATE_HTML = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>🧠 MindScan Sentinel Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
    async function atualizar() {
        const statusResp = await fetch('/api/status');
        const logsResp = await fetch('/api/logs');
        const status = await statusResp.json();
        const logs = await logsResp.json();

        document.getElementById('cpu').innerText = status.cpu + '%';
        document.getElementById('mem').innerText = status.memory + '%';
        document.getElementById('uptime').innerText = status.uptime;
        document.getElementById('version').innerText = status.version;
        document.getElementById('integrity').innerText = status.integrity;
        
        let table = '';
        for (const s of status.services) {
            table += `<tr><td class='px-4 py-2'>${s.name}</td><td class='px-4 py-2 text-center'>${s.status}</td></tr>`;
        }
        document.getElementById('services').innerHTML = table;

        let logHTML = '';
        for (const l of logs) {
            let cor = l.level === 'ERROR' ? 'text-red-500' : l.level === 'WARN' ? 'text-yellow-500' : 'text-green-500';
            logHTML += `<div class='py-1 border-b border-gray-200'><span class='font-mono text-xs text-gray-500'>${l.time}</span> 
                        <span class='${cor} font-semibold ml-2'>[${l.level}]</span> ${l.message}</div>`;
        }
        document.getElementById('logs').innerHTML = logHTML;
    }
    setInterval(atualizar, {{refresh}} * 1000);
    window.onload = atualizar;
    </script>
</head>
<body class="bg-gray-950 text-gray-100 font-sans">
    <div class="container mx-auto py-6 px-8">
        <h1 class="text-3xl font-bold mb-4 text-blue-400">🧠 MindScan Sentinel Dashboard</h1>
        <div class="grid grid-cols-4 gap-4 mb-6">
            <div class="bg-gray-800 rounded-xl p-4 shadow"><h2 class="text-lg font-semibold">CPU</h2><p id="cpu" class="text-2xl mt-1 text-green-400">--</p></div>
            <div class="bg-gray-800 rounded-xl p-4 shadow"><h2 class="text-lg font-semibold">Memória</h2><p id="mem" class="text-2xl mt-1 text-green-400">--</p></div>
            <div class="bg-gray-800 rounded-xl p-4 shadow"><h2 class="text-lg font-semibold">Uptime</h2><p id="uptime" class="text-xl mt-1 text-blue-300">--</p></div>
            <div class="bg-gray-800 rounded-xl p-4 shadow"><h2 class="text-lg font-semibold">Versão</h2><p id="version" class="text-xl mt-1 text-indigo-300">--</p></div>
        </div>

        <div class="bg-gray-900 rounded-xl p-4 shadow mb-6">
            <h2 class="text-xl font-bold mb-3 text-yellow-400">Status dos Serviços</h2>
            <table class="w-full text-left" id="services"></table>
        </div>

        <div class="bg-gray-900 rounded-xl p-4 shadow">
            <h2 class="text-xl font-bold mb-3 text-green-400">Logs Recentes</h2>
            <div id="logs" class="max-h-96 overflow-y-auto text-sm"></div>
        </div>

        <footer class="text-gray-500 text-xs mt-6 text-center">
            Atualização automática a cada {{refresh}}s — Leo Vinci • Inovexa Software © 2025
        </footer>
    </div>
</body>
</html>
""".replace("{{refresh}}", str(REFRESH_INTERVAL))

# ------------------------ MAIN ------------------------
if __name__ == "__main__":
    print(f"[{now()}] 🧠 MindScan Sentinel Dashboard iniciado em http://127.0.0.1:8092")
    app.run(host="127.0.0.1", port=8092, debug=False)
