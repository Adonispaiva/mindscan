// D:\projetos-inovexa\mindscan\frontend\src\services\authService.ts

import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const TOKEN_KEY = 'auth_token';

export const login = async (email: string, password: string) => {
  const response = await axios.post(`${API_URL}/auth/token`, {
    username: email,
    password,
  });

  const token = response.data.access_token;
  localStorage.setItem(TOKEN_KEY, token);
};

export const logout = () => {
  localStorage.removeItem(TOKEN_KEY);
};

export const getToken = (): string | null => {
  return localStorage.getItem(TOKEN_KEY);
};

export const isAuthenticated = (): boolean => {
  const token = getToken();
  if (!token) return false;
  return !isTokenExpired(token);
};

export const isTokenExpired = (token: string): boolean => {
  try {
    const [, payloadBase64] = token.split('.');
    const payload = JSON.parse(atob(payloadBase64));
    const now = Math.floor(Date.now() / 1000);
    return payload.exp < now;
  } catch {
    return true;
  }
};
