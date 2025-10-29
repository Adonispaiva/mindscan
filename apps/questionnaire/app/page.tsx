"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { submitQuiz } from "../services/api";

export default function QuestionnairePage() {
  const [performance, setPerformance] = useState<string[]>(Array(10).fill(""));
  const [matcher, setMatcher] = useState<string[]>(Array(10).fill(""));
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const router = useRouter();

  const handleChange = (index: number, value: string, type: "performance" | "matcher") => {
    const numeric = value.replace(/\D/g, "");
    const arr = type === "performance" ? [...performance] : [...matcher];
    arr[index] = numeric;
    type === "performance" ? setPerformance(arr) : setMatcher(arr);
  };

  const handleSubmit = async () => {
    setError("");
    const allValues = [...performance, ...matcher].map(Number);
    if (allValues.some(v => isNaN(v) || v < 0 || v > 100)) {
      setError("Todos os valores devem estar entre 0 e 100.");
      return;
    }

    setLoading(true);
    try {
      const territory = await submitQuiz(
        performance.map(Number),
        matcher.map(Number)
      );
      router.push(`/result?t=${territory}`);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen p-6 max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-6 text-center">Questionário de Performance</h1>

      <div className="grid grid-cols-2 gap-6">
        <div>
          <h2 className="font-semibold mb-2">Performance</h2>
          {performance.map((value, i) => (
            <input
              key={`p-${i}`}
              type="number"
              min="0"
              max="100"
              value={value}
              onChange={(e) => handleChange(i, e.target.value, "performance")}
              className="w-full border p-2 rounded mb-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder={`Valor ${i + 1}`}
              aria-label={`Valor de performance ${i + 1}`}
            />
          ))}
        </div>

        <div>
          <h2 className="font-semibold mb-2">Matcher</h2>
          {matcher.map((value, i) => (
            <input
              key={`m-${i}`}
              type="number"
              min="0"
              max="100"
              value={value}
              onChange={(e) => handleChange(i, e.target.value, "matcher")}
              className="w-full border p-2 rounded mb-2 focus:outline-none focus:ring-2 focus:ring-green-500"
              placeholder={`Valor ${i + 1}`}
              aria-label={`Valor de matcher ${i + 1}`}
            />
          ))}
        </div>
      </div>

      {error && <p className="text-red-600 mt-4 text-center font-medium">{error}</p>}

      <div className="mt-6 text-center">
        <button
          onClick={handleSubmit}
          disabled={loading}
          className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 transition disabled:opacity-50"
        >
          {loading ? "Enviando..." : "Enviar"}
        </button>
      </div>
    </main>
  );
}




