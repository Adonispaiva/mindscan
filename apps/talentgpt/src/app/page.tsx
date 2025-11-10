"use client";

import { useState } from "react";
import { obterOrientacao } from "../lib/api";

export default function Home() {
  const [prompt, setPrompt] = useState("");
  const [resposta, setResposta] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit() {
    if (!prompt.trim()) return;
    setLoading(true);
    const r = await obterOrientacao(prompt);
    setResposta(r);
    setLoading(false);
  }

  return (
    <main className="min-h-screen flex flex-col items-center p-6">
      <h1 className="text-2xl font-bold mb-4">TalentGPT</h1>
      <textarea
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Cole um resumo do candidato ou objetivo…"
        className="w-full max-w-2xl h-32 p-3 rounded text-black"
      />
      <button
        onClick={handleSubmit}
        disabled={loading}
        className="mt-4 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded"
      >
        {loading ? "Consultando…" : "Obter orientação"}
      </button>

      {resposta && (
        <div className="mt-6 w-full max-w-2xl border-t pt-4 whitespace-pre-line">
          <strong>Resposta da IA:</strong>
          <p className="mt-2">{resposta}</p>
        </div>
      )}
    </main>
  );
}




