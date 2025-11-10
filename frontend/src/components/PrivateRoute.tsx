// D:\projetos-inovexa\mindscan\frontend\src\components\PrivateRoute.tsx

import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuthContext } from '../contexts/AuthContext';

interface Props {
  children: React.ReactNode;
}

const PrivateRoute: React.FC<Props> = ({ children }) => {
  const { isAuthenticated } = useAuthContext();

  if (isAuthenticated === null) {
    return <div className="text-center p-4">Verificando autenticação...</div>;
  }

  return isAuthenticated ? <>{children}</> : <Navigate to="/login" replace />;
};

export default PrivateRoute;
