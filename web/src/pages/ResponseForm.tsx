import { useState } from "react";
import { api } from "../services/api";

export default function ResponseForm() {
  const [respostas, setRespostas] = useState(["", "", ""]);
  const [resultado, setResultado] = useState(null);

  const handleChange = (index: number, valor: string) => {
    const copia = [...respostas];
    copia[index] = valor;
    setRespostas(copia);
  };

  const handleSubmit = async () => {
    try {
      const response = await api.post("/responder", { respostas });
      setResultado(response.data);
    } catch (err) {
      alert("Erro ao enviar respostas.");
    }
  };

  return (
    <div className="p-4 max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-4">Responder ao MindScan</h1>

      {respostas.map((resposta, index) => (
        <input
          key={index}
          type="text"
          placeholder={`Resposta ${index + 1}`}
          className="w-full p-2 border rounded mb-2"
          value={resposta}
          onChange={(e) => handleChange(index, e.target.value)}
        />
      ))}

      <button
        onClick={handleSubmit}
        className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
      >
        Enviar
      </button>

      {resultado && (
        <div className="mt-4 bg-white p-4 rounded shadow">
          <h2 className="text-lg font-semibold">Resultado:</h2>
          <pre className="text-sm text-gray-700 mt-2">
            {JSON.stringify(resultado, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
