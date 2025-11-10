import { useState } from "react";
import { api } from "../services/api";

export default function QuizForm() {
  const [performance, setPerformance] = useState<number[]>([]);
  const [matcher, setMatcher] = useState<number[]>([]);
  const [result, setResult] = useState<any>(null);

  const handleChange = (
    arraySetter: React.Dispatch<React.SetStateAction<number[]>>,
    index: number,
    value: string
  ) => {
    const val = parseInt(value);
    arraySetter((prev) => {
      const copy = [...prev];
      copy[index] = isNaN(val) ? 0 : val;
      return copy;
    });
  };

  const submit = async () => {
    try {
      const response = await api.post("/quiz/submit", {
        performance,
        matcher,
      });
      setResult(response.data);
    } catch (err) {
      alert("Erro ao enviar questionário.");
    }
  };

  return (
    <div className="w-full max-w-md mt-6 space-y-4">
      {[...Array(3)].map((_, i) => (
        <div key={i} className="flex gap-4">
          <input
            type="number"
            placeholder={`Performance ${i + 1}`}
            className="w-full p-2 border rounded"
            onChange={(e) => handleChange(setPerformance, i, e.target.value)}
          />
          <input
            type="number"
            placeholder={`Matcher ${i + 1}`}
            className="w-full p-2 border rounded"
            onChange={(e) => handleChange(setMatcher, i, e.target.value)}
          />
        </div>
      ))}

      <button
        onClick={submit}
        className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
      >
        Enviar
      </button>

      {result && (
        <div className="mt-4 p-4 bg-white rounded shadow">
          <h2 className="font-bold text-lg text-green-700">Resultado:</h2>
          <pre className="text-sm text-gray-700 mt-2">
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
