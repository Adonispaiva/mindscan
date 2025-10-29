const BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";

export async function obterOrientacao(prompt: string): Promise<string> {
  try {
    const response = await fetch(`${BASE}/api/orientacao`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt })
    });

    if (!response.ok) {
      let msg = response.statusText;
      try { const j = await response.json(); msg = j.detail || msg; } catch {}
      throw new Error(msg);
    }

    const data = await response.json();
    return data.resposta;
  } catch (err) {
    console.error("API erro:", err);
    return "Erro na requisição.";
  }
}




