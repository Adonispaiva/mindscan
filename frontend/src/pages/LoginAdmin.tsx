// ===============================================================
//  COMPONENTE: LOGIN ADMIN (Milena / Inovexa)
//  Projeto: MindScan — SynMind MI v2.0
//  Autor: Leo Vinci (GPT Inovexa)
//  Data: 07/11/2025
//  Função: Autenticação unificada e controle hierárquico de acesso
// ===============================================================

import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Lock, Shield, Brain } from "lucide-react";

export default function LoginAdmin() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    // Simulação de autenticação — em produção, substituir por API real
    if (email === "milena@synmind.com" && password === "synmind_admin") {
      const auth = { isAuthenticated: true, role: "admin", token: "synmind_token" };
      localStorage.setItem("mindscan_auth", JSON.stringify(auth));
      navigate("/admin");
    } else if (email === "adonis@inovexa.com" && password === "inovexa_root") {
      const auth = { isAuthenticated: true, role: "inovexa", token: "inovexa_root_token" };
      localStorage.setItem("mindscan_auth", JSON.stringify(auth));
      navigate("/inovexa/ctrl");
    } else {
      setError("Credenciais inválidas. Verifique seu e-mail e senha.");
    }
  };

  return (
    <motion.div
      className="flex items-center justify-center min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-indigo-950 text-gray-100"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
    >
      <div className="bg-slate-900/80 border border-slate-700 rounded-2xl p-8 w-[400px] shadow-xl">
        <div className="flex justify-center mb-6">
          <Brain className="w-12 h-12 text-indigo-400" />
        </div>

        <h1 className="text-2xl font-bold text-center mb-1 text-indigo-400">
          MindScan — Acesso Administrativo
        </h1>
        <p className="text-center text-sm text-gray-400 mb-6">
          Painel de Controle SynMind / Inovexa
        </p>

        <form onSubmit={handleLogin} className="space-y-4">
          <Input
            type="email"
            placeholder="E-mail"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="bg-slate-800 border-slate-700 text-white"
            required
          />
          <Input
            type="password"
            placeholder="Senha"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="bg-slate-800 border-slate-700 text-white"
            required
          />
          <Button
            type="submit"
            className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold"
          >
            Entrar
          </Button>
        </form>

        {error && <p className="text-red-400 text-center mt-3 text-sm">{error}</p>}

        <div className="flex justify-center mt-6 space-x-3 text-slate-500 text-xs">
          <Shield className="w-4 h-4" />
          <span>Ambiente seguro — Inovexa Software</span>
        </div>
      </div>
    </motion.div>
  );
}
