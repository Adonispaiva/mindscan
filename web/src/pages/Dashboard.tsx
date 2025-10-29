// D:\projetos-inovexa\mindscan\web\src\pages\Dashboard.tsx

import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface Metrics {
  total_users: number;
  total_quizzes: number;
  total_responses: number;
}

const Dashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const token = localStorage.getItem('token');
        const res = await axios.get('/metrics', {
          headers: { Authorization: `Bearer ${token}` },
        });
        setMetrics(res.data);
      } catch (err) {
        setError('Erro ao carregar métricas');
      }
    };

    fetchMetrics();
  }, []);

  const handleExport = async () => {
    try {
      const token = localStorage.getItem('token');
      const res = await axios.get('/export', {
        headers: { Authorization: `Bearer ${token}` },
        responseType: 'blob'
      });

      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'respostas_mindscan.csv');
      document.body.appendChild(link);
      link.click();
    } catch (err) {
      alert('Erro ao exportar dados.');
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-4">Dashboard</h1>
      {error && <p className="text-red-500">{error}</p>}
      {metrics ? (
        <div className="space-y-4">
          <p>Total de Usuários: <strong>{metrics.total_users}</strong></p>
          <p>Total de Quizzes Enviados: <strong>{metrics.total_quizzes}</strong></p>
          <p>Total de Respostas: <strong>{metrics.total_responses}</strong></p>

          <button
            onClick={handleExport}
            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
          >
            Exportar Respostas (CSV)
          </button>
        </div>
      ) : (
        <p>Carregando...</p>
      )}
    </div>
  );
};

export default Dashboard;
