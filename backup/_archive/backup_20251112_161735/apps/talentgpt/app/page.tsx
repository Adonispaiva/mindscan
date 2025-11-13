// Caminho: D:\projetos-inovexa\MindScan\apps\talentgpt\app\page.tsx

"use client";

import { useState } from "react";
import { obterOrientacao } from "../src/lib/api";

export default function Home() {
  const [prompt, setPrompt] = useState("");
  const [resposta, setResposta] = useState("");
  const [carregando, setCarregando] = useState(false);

  const handleSubmit = async () => {
    setCarregando(true);
    const respostaIA = await obterOrientacao(prompt);
    setResposta(respostaIA);
    setCarregando(false);
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-black text-white p-4">
      <h1 className="text-2xl font-bold mb-4">TalentGPT</h1>
      <textarea
        className="w-full max-w-xl h-32 p-4 text-black"
        placeholder="Descreva seu objetivo ou desafio..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />
      <button
        onClick={handleSubmit}
        className="mt-4 bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
        disabled={carregando || !prompt.trim()}
      >
        {carregando ? "Carregando..." : "Obter orientação"}
      </button>
      {resposta && (
        <div className="mt-8 max-w-xl">
          <h2 className="text-lg font-semibold mb-2">Resposta da IA:</h2>
          <p className="bg-white text-black p-4 rounded whitespace-pre-line">{resposta}</p>
        </div>
      )}
    </main>
  );
}

// ----------------------------------------
// Caminho: D:\projetos-inovexa\MindScan\apps\talentgpt\src\lib\api.ts

export async function obterOrientacao(prompt: string): Promise<string> {
  try {
    const response = await fetch("http://127.0.0.1:8000/api/orientacao", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ prompt }),
    });

    if (!response.ok) {
      const err = await response.json();
      console.error("Erro na resposta da API:", err);
      throw new Error("Erro na requisição: " + err.detail ?? response.statusText);
    }

    const data = await response.json();
    return data.resposta;
  } catch (error) {
    console.error("Erro ao obter orientação:", error);
    return "Erro na requisição.";
  }
}

// ----------------------------------------
// Caminho: D:\projetos-inovexa\MindScan\apps\talentgpt\tsconfig.json

{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "incremental": true,
    "plugins": [{ "name": "next" }]
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}




