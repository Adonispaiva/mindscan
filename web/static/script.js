// ===============================================
// MindScan Web Frontend Script (v3.2)
// ===============================================

const consolePanel = document.getElementById("console");
const btnStart = document.getElementById("btnStart");
const btnStop = document.getElementById("btnStop");
const statusLabel = document.getElementById("statusLabel");

let ws = null;
let reconnectTimer = null;

// ---------------------- FUNÇÕES AUXILIARES ----------------------
function log(message) {
  const timestamp = new Date().toLocaleTimeString();
  const line = `[${timestamp}] ${message}`;
  const div = document.createElement("div");
  div.textContent = line;
  consolePanel.appendChild(div);
  consolePanel.scrollTop = consolePanel.scrollHeight;
}

function setStatus(text, color = "var(--accent)") {
  statusLabel.textContent = text;
  statusLabel.style.color = color;
}

function setButtonState(running) {
  btnStart.disabled = running;
  btnStop.disabled = !running;
  if (running) {
    btnStart.classList.add("disabled");
    btnStop.classList.remove("disabled");
  } else {
    btnStart.classList.remove("disabled");
    btnStop.classList.add("disabled");
  }
}

// ---------------------- CONEXÃO WEBSOCKET ----------------------
function connectWebSocket() {
  ws = new WebSocket("ws://127.0.0.1:8080/ws");

  ws.onopen = () => {
    log("✅ Conectado ao servidor MindScan WebSocket.");
    setStatus("Conectado", "#00ff88");
    if (reconnectTimer) clearTimeout(reconnectTimer);
  };

  ws.onmessage = (event) => {
    log(event.data);
  };

  ws.onclose = () => {
    setStatus("Reconectando...", "#ffaa00");
    reconnectTimer = setTimeout(connectWebSocket, 3000);
  };

  ws.onerror = () => {
    setStatus("Erro de conexão", "#ff4444");
  };
}

// ---------------------- CONTROLE DE BOTÕES ----------------------
async function startMindScan() {
  try {
    setButtonState(true);
    setStatus("Inicializando...", "#ffaa00");
    log("🚀 Enviando comando: Iniciar MindScan...");
    const res = await fetch("http://127.0.0.1:8080/start", { method: "POST" });
    const data = await res.json();
    log("🟢 Resposta: " + JSON.stringify(data));
    setStatus("Executando", "#00ff88");
  } catch (err) {
    log("❌ Erro ao iniciar: " + err);
    setStatus("Falha ao iniciar", "#ff4444");
    setButtonState(false);
  }
}

async function stopMindScan() {
  try {
    setStatus("Encerrando...", "#ffaa00");
    log("🛑 Enviando comando: Encerrar MindScan...");
    const res = await fetch("http://127.0.0.1:8080/stop", { method: "POST" });
    const data = await res.json();
    log("🔴 Resposta: " + JSON.stringify(data));
    setStatus("Encerrado", "#ff5555");
    setButtonState(false);
  } catch (err) {
    log("❌ Erro ao encerrar: " + err);
    setStatus("Falha ao encerrar", "#ff4444");
  }
}

// ---------------------- INICIALIZAÇÃO ----------------------
btnStart.addEventListener("click", startMindScan);
btnStop.addEventListener("click", stopMindScan);
setButtonState(false);
connectWebSocket();

log("🧠 MindScan Web Console iniciado.");
