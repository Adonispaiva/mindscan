import { useEffect, useState } from "react";
import { api } from "../services/api";

interface User {
  id: number;
  name: string;
  email: string;
}

function UserList() {
  const [users, setUsers] = useState<User[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    api.get("/users")
      .then((res) => setUsers(res.data))
      .catch(() => setError("Erro ao carregar usuários."));
  }, []);

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-4 text-center">Usuários Cadastrados</h1>

      {error && <p className="text-red-500 text-center">{error}</p>}

      <ul className="bg-white shadow rounded divide-y">
        {users.map((user) => (
          <li key={user.id} className="p-4 hover:bg-gray-50">
            <p><strong>Nome:</strong> {user.name}</p>
            <p><strong>Email:</strong> {user.email}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default UserList;
