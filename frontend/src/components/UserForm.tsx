import React, { useState } from 'react';
import DASSForm from './DASSForm';

export default function UserForm() {
  const [formData, setFormData] = useState({ nome: '', email: '', idade: '' });
  const [formCompleted, setFormCompleted] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Dados do usuário:', formData);
    setFormCompleted(true);
  };

  if (formCompleted) {
    return <DASSForm />;
  }

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white dark:bg-gray-800 shadow-lg rounded-2xl">
      <h2 className="text-xl font-bold mb-4 text-center text-gray-800 dark:text-white">
        Informações do Usuário
      </h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          required
          name="nome"
          placeholder="Nome"
          value={formData.nome}
          onChange={handleChange}
          className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
        />
        <input
          required
          name="email"
          placeholder="E-mail"
          type="email"
          value={formData.email}
          onChange={handleChange}
          className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
        />
        <input
          required
          name="idade"
          placeholder="Idade"
          type="number"
          value={formData.idade}
          onChange={handleChange}
          className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
        />
        <div className="text-center">
          <button
            type="submit"
            className="px-6 py-2 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-lg transition-all duration-300"
          >
            Continuar
          </button>
        </div>
      </form>
    </div>
  );
}
