// D:\projetos-inovexa\mindscan\web\src\AppRouter.tsx

import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Home from './pages/Home';
import QuizForm from './pages/QuizForm';
import QuizResult from './pages/QuizResult';
import ResponseForm from './pages/ResponseForm';
import UserList from './pages/UserList';
import ResponseList from './pages/ResponseList';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import NotFound from './pages/notFound';

const isAuthenticated = (): boolean => {
  const token = localStorage.getItem('token');
  return !!token;
};

const ProtectedRoute = ({ children }: { children: JSX.Element }) => {
  return isAuthenticated() ? children : <Navigate to="/login" replace />;
};

const AppRouter: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/quiz" element={<QuizForm />} />
        <Route path="/result" element={<QuizResult />} />
        <Route path="/response" element={<ResponseForm />} />
        <Route path="/login" element={<Login />} />

        <Route
          path="/users"
          element={<ProtectedRoute><UserList /></ProtectedRoute>}
        />
        <Route
          path="/responses"
          element={<ProtectedRoute><ResponseList /></ProtectedRoute>}
        />
        <Route
          path="/dashboard"
          element={<ProtectedRoute><Dashboard /></ProtectedRoute>}
        />

        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  );
};

export default AppRouter;
