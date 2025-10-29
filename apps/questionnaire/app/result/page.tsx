// D:\projetos-inovexa\MindScan\apps\questionnaire\app\result\page.tsx

"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";

const descriptions: Record<string, string> = {
  REALIZADOR: "Focado em resultados, busca performance e ação imediata.",
  INOVADOR: "Explora novas ideias com foco em impacto e autonomia.",
  INSPIRADOR: "Motiva e engaja pessoas com visão humana e energia emocional.",
  ESTRATEGISTA: "Planeja com lógica e consistência para decisões inteligentes.",
};

export default function ResultPage() {
  const params = useSearchParams();
  const territory = params.get("t") ?? "Indefinido";
  const description = descriptions[territory as keyof typeof descriptions] || "Perfil não reconhecido.";

  return (
    <div className="min-h-screen p-8 max-w-xl mx-auto">
      <h1 className="text-3xl font-bold mb-4">Seu Território: {territory}</h1>
      <p className="text-lg text-gray-700 mb-6">{description}</p>
      <a href="/" className="text-blue-600 hover:underline">Refazer o questionário</a>
    </div>
  );
}




