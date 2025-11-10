import { useState } from "react";
import { api } from "../services/api";

function Home() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async () => {
    try {
      await api.post("/users", { name, email });
      setMessage("Usuário cadastrado com sucesso.");
      setName("");
      setEmail("");
    } catch (err) {
      setMessage("Erro ao cadastrar usuário.");
    }
  };

  return (
    <div className="p-6 max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-4 text-center">Cadastro de Usuário</h1>
      <input
        type="text"
        placeholder="Nome"
        className="w-full p-2 border rounded mb-2"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <input
        type="email"
        placeholder="Email"
        className="w-full p-2 border rounded mb-2"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <button
        onClick={handleSubmit}
        className="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700"
      >
        Cadastrar
      </button>

      {message && (
        <p className="mt-4 text-center font-medium text-gray-700">{message}</p>
      )}
    </div>
  );
}

export default Home;
