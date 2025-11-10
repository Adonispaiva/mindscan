import { useEffect, useState } from "react";
import { api } from "../services/api";

interface Response {
  id: number;
  user_id: number;
  question: string;
  answer: string;
}

function ResponseList() {
  const [responses, setResponses] = useState<Response[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    api.get("/responses")
      .then((res) => setResponses(res.data))
      .catch(() => setError("Erro ao carregar respostas."));
  }, []);

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <h1 className="text-2xl font-bold mb-4 text-center">Respostas Registradas</h1>

      {error && <p className="text-red-500 text-center">{error}</p>}

      <ul className="bg-white shadow rounded divide-y">
        {responses.map((resp) => (
          <li key={resp.id} className="p-4 hover:bg-gray-50">
            <p><strong>ID Usuário:</strong> {resp.user_id}</p>
            <p><strong>Pergunta:</strong> {resp.question}</p>
            <p><strong>Resposta:</strong> {resp.answer}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ResponseList;
