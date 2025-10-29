"use client";

import { useState } from "react";

export default function TalentGPTPage() {
  const [context, setContext] = useState("");
  const [advice, setAdvice] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!context.trim()) return;

    setLoading(true);
    setAdvice(null);

    try {
      const res = await fetch("http://localhost:8000/talentgpt/advice", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          territory: "especialistas", // ← fixo nesta versão inicial
          context,
        }),
      });

      const data = await res.json();
      setAdvice(data.advice ?? "Sem resposta");
    } catch (error) {
      setAdvice("Erro na requisição.");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen p-6 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">TalentGPT</h1>

      <textarea
        value={context}
        onChange={(e) => setContext(e.target.value)}
        placeholder="Descreva seu objetivo ou desafio..."
        className="w-full h-32 p-4 border rounded mb-4"
      />

      <button
        onClick={handleSubmit}
        disabled={loading}
        className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 transition"
      >
        {loading ? "Consultando IA..." : "Obter orientação"}
      </button>

      {advice && (
        <div className="mt-6 border-t pt-4 text-lg whitespace-pre-line">
          <strong>Resposta da IA:</strong>
          <p className="mt-2">{advice}</p>
        </div>
      )}
    </div>
  );
}




