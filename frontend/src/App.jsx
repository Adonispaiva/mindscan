// D:\projetos-inovexa\mindscan\frontend\src\App.jsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [message, setMessage] = useState('');

  useEffect(() => {
    axios.get('http://localhost:5000/')
      .then(response => setMessage(response.data.message))
      .catch(error => setMessage('Erro ao conectar com o backend.'));
  }, []);

  return (
    <div style={{ padding: '2rem', fontFamily: 'Arial' }}>
      <h1>MindScan</h1>
      <p>{message}</p>
    </div>
  );
}

export default App;
