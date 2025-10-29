// src/pages/Dashboard.tsx
import React from 'react';

const Dashboard: React.FC = () => {
  return (
    <div>
      <h1>Dashboard</h1>
      <p>Bem-vindo ao sistema.</p>
    </div>
  );
};

export default Dashboard;

// src/pages/Status.tsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Status: React.FC = () => {
  const [status, setStatus] = useState('Verificando API...');

  useEffect(() => {
    axios.get('http://localhost:8000/status')
      .then(res => {
        const dbStatus = res.data.db || 'indefinido';
        setStatus(`API OK. Banco: ${dbStatus}`);
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

export default Status;

// src/components/PrivateRoute.tsx
import React from 'react';
import { Navigate } from 'react-router-dom';

const isAuthenticated = () => {
  return localStorage.getItem('auth_token') !== null;
};

const PrivateRoute = ({ children }: { children: JSX.Element }) => {
  return isAuthenticated() ? children : <Navigate to="/login" />;
};

export default PrivateRoute;
