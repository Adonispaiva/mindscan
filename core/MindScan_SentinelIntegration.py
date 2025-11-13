from flask import Flask, render_template_string, jsonify
import psutil, requests, json, time
from datetime import datetime
from pathlib import Path

# ============================================
# 🧠 MindScan Sentinel Integration — v5.4
# ============================================
# Autor: Leo Vinci (GPT Inovexa)
# Data: 12/11/2025
# Função: Painel unificado de monitoramento, logs e conformidade
# ============================================

LOG_API = "http://127.0.0.1:8091/logs?limit=50"
MANIFEST_PATH = Path(r"D:\MindScan\update_manifest.json")
REPORT_DIR = Path(r"D:\MindScan\reports")
REFRESH_INTERVAL = 5
app = Flask(__name__)

def now():
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")

# ---------------------- DATA SOURCES ----------------------
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
    m = get_manifest()
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    uptime = time.time() - psutil.boot_time()
    return {
        "cpu": cpu,
        "memory": mem,
        "uptime": f"{int(uptime // 3600)}h {int((uptime % 3600) // 60)}m",
        "version": m.get("current_build", {}).get("version_tag", "desconhecida"),
        "integrity": m.get("verification", {}).get("last_result", "indefinida")
    }

def get_compliance():
    files = sorted(REPORT_DIR.glob("Compliance_*.json"), reverse=True)
    if not files:
        return {"status": "UNKNOWN", "findings": 0, "anonymized": 0, "reports": []}
    latest = json.loads(files[0].read_text(encoding="utf-8"))
    findings = len(latest.get("findings", []))
    status = "OK" if findings == 0 else "WARN" if findings < 3 else "FAIL"
    history = []
    for file in files[:5]:
        data = json.loads(file.read_text(encoding="utf-8"))
        history.append({
            "file": file.name,
            "findings": len(data.get("findings", [])),
            "anon": data.get("anonymized_files", 0),
            "timestamp": data.get("timestamp")
        })
    return {"status": status, "findings": findings, "anonymized": latest.get("anonymized_files", 0), "reports": history}

# ---------------------- API ----------------------
@app.route("/api/status")
def api_status(): return jsonify(get_status())
@app.route("/api/logs")
def api_logs(): return jsonify(get_logs())
@app.route("/api/compliance")
def api_compliance(): return jsonify(get_compliance())

# ---------------------- UI ----------------------
@app.route("/")
def index(): return render_template_string(TEMPLATE_HTML)

# ---------------------- TEMPLATE ----------------------
TEMPLATE_HTML = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<title>🧠 MindScan Sentinel — Painel Unificado</title>
<script src="https://cdn.tailwindcss.com"></script>
<script>
let abaAtiva = localStorage.getItem('aba') || 'monitor';
async function atualizar(){
  const [s, l, c] = await Promise.all([
    fetch('/api/status').then(r=>r.json()),
    fetch('/api/logs').then(r=>r.json()),
    fetch('/api/compliance').then(r=>r.json())
  ]);
  // Monitor
  document.getElementById('cpu').innerText = s.cpu + '%';
  document.getElementById('mem').innerText = s.memory + '%';
  document.getElementById('uptime').innerText = s.uptime;
  document.getElementById('version').innerText = s.version;
  document.getElementById('integrity').innerText = s.integrity;
  // Logs
  let logHTML = '';
  for(const e of l){ const color = e.level==='ERROR'?'text-red-500':e.level==='WARN'?'text-yellow-400':'text-green-400';
    logHTML += `<div class='border-b border-gray-800 py-1'><span class='${color} font-bold'>[${e.level}]</span> ${e.message}</div>`;
  }
  document.getElementById('logs').innerHTML = logHTML;
  // Compliance
  document.getElementById('comp-status').innerHTML = c.status==='OK' ? '🟢 Conformidade Plena' : c.status==='WARN' ? '🟡 Atenção' : '🔴 Violações Detectadas';
  document.getElementById('comp-findings').innerText = c.findings;
  document.getElementById('comp-anon').innerText = c.anonymized;
  let hist = '';
  for(const h of c.reports){ hist += `<tr><td>${h.timestamp}</td><td>${h.file}</td><td>${h.findings}</td><td>${h.anon}</td></tr>`;}
  document.getElementById('comp-history').innerHTML = hist;
}
function trocarAba(nome){ abaAtiva=nome; localStorage.setItem('aba',nome);
  document.querySelectorAll('.aba').forEach(el=>el.classList.add('hidden'));
  document.getElementById(nome).classList.remove('hidden');
}
setInterval(atualizar, {{refresh}}*1000);
window.onload=()=>{trocarAba(abaAtiva); atualizar();}
</script>
</head>
<body class="bg-gray-950 text-gray-100 font-sans">
  <div class="container mx-auto px-6 py-6">
    <h1 class="text-3xl font-bold text-blue-400 mb-4">🧠 MindScan Sentinel — Painel Unificado</h1>
    <div class="flex gap-4 mb-4">
      <button class="bg-gray-800 px-4 py-2 rounded hover:bg-gray-700" onclick="trocarAba('monitor')">Monitoramento</button>
      <button class="bg-gray-800 px-4 py-2 rounded hover:bg-gray-700" onclick="trocarAba('logs')">Logs</button>
      <button class="bg-gray-800 px-4 py-2 rounded hover:bg-gray-700" onclick="trocarAba('compliance')">Conformidade</button>
    </div>
    
    <div id="monitor" class="aba">
      <div class="grid grid-cols-4 gap-4 mb-6">
        <div class="bg-gray-800 rounded-xl p-4 shadow"><h2>CPU</h2><p id="cpu" class="text-2xl text-green-400">--</p></div>
        <div class="bg-gray-800 rounded-xl p-4 shadow"><h2>Memória</h2><p id="mem" class="text-2xl text-green-400">--</p></div>
        <div class="bg-gray-800 rounded-xl p-4 shadow"><h2>Uptime</h2><p id="uptime" class="text-xl text-blue-300">--</p></div>
        <div class="bg-gray-800 rounded-xl p-4 shadow"><h2>Versão</h2><p id="version" class="text-xl text-indigo-300">--</p></div>
      </div>
      <div class="bg-gray-900 rounded-xl p-4"><h2 class="text-lg text-yellow-400 mb-2">Integridade</h2><p id="integrity" class="text-xl text-gray-300">--</p></div>
    </div>

    <div id="logs" class="aba hidden bg-gray-900 rounded-xl p-4 max-h-96 overflow-y-auto"></div>

    <div id="compliance" class="aba hidden">
      <div class="grid grid-cols-3 gap-4 mb-4">
        <div class="bg-gray-800 rounded-xl p-4 shadow"><h2>Status</h2><p id="comp-status" class="text-xl text-green-400">--</p></div>
        <div class="bg-gray-800 rounded-xl p-4 shadow"><h2>Ocorrências</h2><p id="comp-findings" class="text-2xl text-yellow-400">--</p></div>
        <div class="bg-gray-800 rounded-xl p-4 shadow"><h2>Anonimizados</h2><p id="comp-anon" class="text-2xl text-indigo-300">--</p></div>
      </div>
      <div class="bg-gray-900 rounded-xl p-4">
        <h2 class="text-lg font-bold mb-2 text-green-400">Histórico</h2>
        <table class="w-full text-sm text-left">
          <thead><tr class="text-gray-500 border-b border-gray-800"><th>Data</th><th>Relatório</th><th>Ocorrências</th><th>Anon.</th></tr></thead>
          <tbody id="comp-history"></tbody>
        </table>
      </div>
    </div>
    <footer class="text-gray-500 text-xs mt-6 text-center">Atualização a cada {{refresh}}s — Inovexa Software © 2025</footer>
  </div>
</body>
</html>
""".replace("{{refresh}}", str(REFRESH_INTERVAL))

# ---------------------- MAIN ----------------------
if __name__ == "__main__":
    print(f"[{now()}] 🧠 Painel Unificado disponível em http://127.0.0.1:8095")
    app.run(host="127.0.0.1", port=8095, debug=False)
