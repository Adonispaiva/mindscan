// ===============================================================
//  COMPONENTE: INOVEXA CONTROL PANEL
//  Projeto: MindScan — SynMind MI v2.0
//  Autor: Leo Vinci (GPT Inovexa)
//  Data: 07/11/2025
//  Função: Painel de controle técnico reservado à Inovexa
// ===============================================================

import React, { useEffect, useState } from "react";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Shield, Terminal, Database, Activity } from "lucide-react";
import { motion } from "framer-motion";

const API_URL = "/inovexa-admin";

export default function InovexaControlPanel() {
  const [token, setToken] = useState("");
  const [auth, setAuth] = useState(false);
  const [status, setStatus] = useState<any>(null);
  const [command, setCommand] = useState("");
  const [output, setOutput] = useState("");
  const [logs, setLogs] = useState<any[]>([]);
  const [error, setError] = useState("");

  const headers = { "X-Inovexa-Token": token };

  const fetchStatus = async () => {
    try {
      const res = await axios.get(`${API_URL}/status`, { headers });
      setStatus(res.data);
      setAuth(true);
      setError("");
    } catch (err: any) {
      setAuth(false);
      setError("Falha de autenticação ou sistema inacessível.");
    }
  };

  const runCommand = async () => {
    try {
      const res = await axios.post(`${API_URL}/exec`, { cmd: command }, { headers });
      setOutput(res.data.saida || "Comando executado com sucesso.");
    } catch (err: any) {
      setOutput("Erro ao executar comando.");
    }
  };

  const fetchLogs = async () => {
    try {
      const res = await axios.get(`${API_URL}/logs`, { headers });
      setLogs([res.data]);
    } catch (err: any) {
      setLogs([]);
    }
  };

  useEffect(() => {
    if (auth) {
      fetchStatus();
      fetchLogs();
    }
  }, [auth]);

  if (!auth)
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-slate-950 text-white">
        <Shield className="w-16 h-16 mb-4 text-indigo-400" />
        <h1 className="text-2xl font-bold mb-2">Inovexa Control Access</h1>
        <p className="text-sm mb-4">Autenticação técnica restrita</p>
        <Input
          type="password"
          placeholder="Token Inovexa"
          value={token}
          onChange={(e) => setToken(e.target.value)}
          className="w-64 mb-4 bg-slate-800 border-slate-700 text-white"
        />
        <Button onClick={fetchStatus} className="bg-indigo-600 hover:bg-indigo-700">
          Entrar
        </Button>
        {error && <p className="mt-3 text-red-400">{error}</p>}
      </div>
    );

  return (
    <motion.div
      className="p-6 min-h-screen bg-slate-900 text-gray-100"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
    >
      <h1 className="text-3xl font-bold mb-6 text-indigo-400 flex items-center gap-2">
        <Activity className="w-7 h-7" /> Inovexa Control Panel
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="bg-slate-800 border-slate-700">
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <Database className="w-5 h-5 text-indigo-400" /> Status do Sistema
            </CardTitle>
          </CardHeader>
          <CardContent>
            {status ? (
              <div className="text-sm space-y-2">
                <p>🧩 Sistema: {status.sistema}</p>
                <p>🚀 Versão: {status.versao}</p>
                <p>💻 Ambiente: {status.ambiente}</p>
                <p>🕒 {status.data_hora}</p>
                <div className="mt-3">
                  <p className="font-semibold">Módulos ativos:</p>
                  <ul className="list-disc list-inside">
                    {Object.entries(status.modulos).map(([k, v]) => (
                      <li key={k}>{k}: {v ? "✅" : "❌"}</li>
                    ))}
                  </ul>
                </div>
              </div>
            ) : (
              <p>Carregando...</p>
            )}
          </CardContent>
        </Card>

        <Card className="bg-slate-800 border-slate-700 md:col-span-2">
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <Terminal className="w-5 h-5 text-indigo-400" /> Execução de Comandos
            </CardTitle>
          </CardHeader>
          <CardContent>
            <Textarea
              placeholder="Digite um comando shell..."
              value={command}
              onChange={(e) => setCommand(e.target.value)}
              className="bg-slate-900 border-slate-700 text-gray-100 mb-3"
            />
            <Button onClick={runCommand} className="bg-indigo-600 hover:bg-indigo-700">
              Executar
            </Button>
            <pre className="mt-4 bg-slate-950 p-3 text-xs rounded overflow-x-auto border border-slate-800">
              {output || "Saída do comando exibida aqui..."}
            </pre>
          </CardContent>
        </Card>

        <Card className="bg-slate-800 border-slate-700 md:col-span-3">
          <CardHeader>
            <CardTitle className="text-lg">Últimos Logs de MI</CardTitle>
          </CardHeader>
          <CardContent>
            {logs.length > 0 ? (
              <pre className="bg-slate-950 p-3 rounded text-xs overflow-x-auto">
                {JSON.stringify(logs, null, 2)}
              </pre>
            ) : (
              <p>Nenhum log encontrado.</p>
            )}
          </CardContent>
        </Card>
      </div>
    </motion.div>
  );
}
