# ================================================
# Inovexa Monitoring v8.0.5
# Grafana Provision Omni - Monitor Agent API
# ================================================
# Codificação: UTF-8 (sem BOM)
# Autor: Inovexa Software / Leo Vinci
# Criado em: 2025-11-09
# -----------------------------------------------

import os
import psutil
import socket
from time import time
from flask import Flask, Response, jsonify
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST

# --- Configuração do ambiente ---
APP_VERSION = "8.0.5"
HOSTNAME = socket.gethostname()
START_TIME = time()

PROMETHEUS_URL = os.getenv("PROMETHEUS_URL", "http://localhost:9090")
GRAFANA_URL = os.getenv("GRAFANA_URL", "http://localhost:3000")
MONITOR_AGENT_ENV = os.getenv("MONITOR_AGENT_ENV", "development")

# --- Criação da aplicação Flask ---
app = Flask(__name__)

# --- Métricas principais ---
cpu_usage = Gauge("mindscan_host_cpu", "Uso de CPU do host Mindscan")
memory_usage = Gauge("mindscan_host_memory", "Uso de memória do host Mindscan")
uptime_seconds = Gauge("mindscan_host_uptime_seconds", "Tempo de atividade do Mindscan Agent")

# --- Endpoint de saúde ---
@app.route("/healthz")
def health_check():
    return jsonify({
        "status": "ok",
        "version": APP_VERSION,
        "environment": MONITOR_AGENT_ENV,
        "hostname": HOSTNAME,
        "prometheus": PROMETHEUS_URL,
        "grafana": GRAFANA_URL,
        "uptime_seconds": round(time() - START_TIME, 2)
    }), 200

# --- Endpoint de métricas Prometheus ---
@app.route("/metrics")
def metrics():
    try:
        cpu_usage.set(psutil.cpu_percent())
        memory_usage.set(psutil.virtual_memory().percent)
        uptime_seconds.set(time() - START_TIME)
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Página inicial ---
@app.route("/")
def index():
    return f"""
    <h2>Inovexa Mindscan Monitoring Agent v{APP_VERSION}</h2>
    <p>Ambiente: <b>{MONITOR_AGENT_ENV}</b></p>
    <p>Prometheus: <a href="{PROMETHEUS_URL}" target="_blank">{PROMETHEUS_URL}</a></p>
    <p>Grafana: <a href="{GRAFANA_URL}" target="_blank">{GRAFANA_URL}</a></p>
    <hr>
    <p><a href="/healthz">Verificar status</a> | <a href="/metrics">Ver métricas Prometheus</a></p>
    """

# --- Inicialização ---
if __name__ == "__main__":
    print(f"\n[Inovexa Mindscan] Agente de Monitoramento Ativo")
    print("------------------------------------------------")
    print(f"Versão: {APP_VERSION}")
    print(f"Ambiente: {MONITOR_AGENT_ENV}")
    print(f"Prometheus: {PROMETHEUS_URL}")
    print(f"Grafana: {GRAFANA_URL}")
    print(f"Host: {HOSTNAME}")
    print(f"-----------------------------------------------\n")
    app.run(host="0.0.0.0", port=8000)
