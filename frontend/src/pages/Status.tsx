import React, { useEffect, useState } from 'react';
import axios from 'axios';

const StatusPage = () => {
  const [status, setStatus] = useState<string>('Verificando status da API...');

  useEffect(() => {
    axios.get('http://localhost:8000/status')
      .then(res => {
        const dbStatus = res.data?.db || 'Indefinido';
        setStatus(`API OK. Banco de dados: ${dbStatus}`);
      })
      .catch(() => setStatus('API OFFLINE'));
  }, []);

  return (
    <div>
      <h2>Status do Sistema</h2>
      <p>{status}</p>
    </div>
  );
};

export default StatusPage;
