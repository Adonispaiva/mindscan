# -*- coding: utf-8 -*-
"""
MindScan Web Interface — FastAPI Dashboard
Autor: Leo Vinci
Inovexa Software
"""

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import psutil, asyncio, datetime

app = FastAPI(title="MindScan Web", version="1.0")

HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>MindScan Web Console</title>
<style>
body { font-family: Consolas, monospace; background:#0c0c0c; color:#0ff; text-align:center; }
h1 { color:#ff0; }
.card { border:1px solid #222; margin:10px; padding:10px; display:inline-block; width:200px; border-radius:10px; }
.value { font-size:24px; color:#0f0; }
</style>
</head>
<body>
<h1>🧠 MindScan Web Console</h1>
<div id="stats"></div>
<script>
const ws = new WebSocket("ws://localhost:8000/ws");
ws.onmessage = e => {
  const d = JSON.parse(e.data);
  document.getElementById("stats").innerHTML = `
    <div class='card'>CPU: <span class='value'>${d.cpu}%</span></div>
    <div class='card'>Memória: <span class='value'>${d.mem}%</span></div>
    <div class='card'>Disco: <span class='value'>${d.disk}%</span></div>
    <div class='card'>Status: <span style='color:${d.status=="OK"?"#0f0":"#f00"}'>${d.status}</span></div>
    <div style='margin-top:10px;font-size:12px;color:#888'>Atualizado ${d.time}</div>`;
};
</script>
</body>
</html>
"""

@app.get("/")
async def index():
    return HTMLResponse(HTML)

@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    while True:
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent
        status = "OK" if cpu < 80 and mem < 80 and disk < 90 else "ALERTA"
        data = {
            "cpu": cpu, "mem": mem, "disk": disk,
            "status": status,
            "time": datetime.datetime.now().strftime("%H:%M:%S")
        }
        await ws.send_json(data)
        await asyncio.sleep(1)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
