// src/pages/NotFound.tsx
import React from 'react';
import { Link } from 'react-router-dom';

const NotFound: React.FC = () => {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center text-center px-4">
      <h1 className="text-5xl font-bold mb-4">404</h1>
      <p className="text-xl mb-6">Página não encontrada.</p>
      <Link to="/" className="text-blue-500 hover:underline">
        Voltar para a Home
      </Link>
    </div>
  );
};

export default NotFound;
