// ===============================================================
//  COMPONENTE: ADMIN PANEL MILENA
//  Projeto: MindScan — SynMind MI v2.0
//  Autor: Leo Vinci (GPT Inovexa)
//  Data: 07/11/2025
//  Função: Painel administrativo da SynMind (Milena)
// ===============================================================

import React, { useState, useEffect } from "react";
import axios from "axios";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Input } from "@/components/ui/input";
import { BarChart3, FileText, Settings, Sliders } from "lucide-react";

export default function AdminPanelMilena() {
  const [diagnostics, setDiagnostics] = useState<any[]>([]);
  const [templates, setTemplates] = useState<any[]>([]);
  const [weights, setWeights] = useState<any[]>([]);
  const [selectedTab, setSelectedTab] = useState("dashboard");
  const [saving, setSaving] = useState(false);

  // Simulação de APIs (substituir por endpoints reais)
  const fetchDiagnostics = async () => {
    const res = await axios.get("/admin/diagnostics");
    setDiagnostics(res.data || []);
  };

  const fetchWeights = async () => {
    const res = await axios.get("/admin/jobs");
    setWeights(res.data || []);
  };

  const saveWeights = async () => {
    setSaving(true);
    await axios.post("/admin/jobs", weights);
    setSaving(false);
  };

  const fetchTemplates = async () => {
    const res = await axios.get("/admin/templates");
    setTemplates(res.data || []);
  };

  useEffect(() => {
    fetchDiagnostics();
    fetchWeights();
    fetchTemplates();
  }, []);

  return (
    <motion.div
      className="min-h-screen bg-gradient-to-b from-slate-950 to-slate-900 text-gray-100 p-6"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
    >
      <header className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-indigo-400 flex items-center gap-3">
          <BarChart3 className="w-7 h-7 text-indigo-400" /> Painel SynMind — Milena
        </h1>
        <Button className="bg-indigo-600 hover:bg-indigo-700">Exportar Relatórios</Button>
      </header>

      <Tabs value={selectedTab} onValueChange={setSelectedTab}>
        <TabsList className="bg-slate-800 border border-slate-700">
          <TabsTrigger value="dashboard">📊 Dashboard</TabsTrigger>
          <TabsTrigger value="relatorios">📁 Relatórios</TabsTrigger>
          <TabsTrigger value="pesos">⚙️ Pesos & Cargos</TabsTrigger>
          <TabsTrigger value="templates">🎨 Templates</TabsTrigger>
        </TabsList>

        {/* Dashboard */}
        <TabsContent value="dashboard" className="mt-6">
          <Card className="bg-slate-800 border-slate-700">
            <CardHeader>
              <CardTitle>Visão Geral</CardTitle>
            </CardHeader>
            <CardContent>
              <p>Total de diagnósticos realizados: {diagnostics.length}</p>
              <p>Templates disponíveis: {templates.length}</p>
              <p>Última atualização: {new Date().toLocaleString()}</p>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Relatórios */}
        <TabsContent value="relatorios" className="mt-6">
          <Card className="bg-slate-800 border-slate-700">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileText className="w-5 h-5 text-indigo-400" /> Relatórios Gerados
              </CardTitle>
            </CardHeader>
            <CardContent>
              {diagnostics.length > 0 ? (
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Usuário</TableHead>
                      <TableHead>Data</TableHead>
                      <TableHead>Quadrante</TableHead>
                      <TableHead>Status</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {diagnostics.map((d, i) => (
                      <TableRow key={i}>
                        <TableCell>{d.usuario}</TableCell>
                        <TableCell>{new Date(d.data).toLocaleString()}</TableCell>
                        <TableCell>{d.quadrante}</TableCell>
                        <TableCell>{d.status || "Concluído"}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              ) : (
                <p>Nenhum relatório disponível.</p>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Pesos e Cargos */}
        <TabsContent value="pesos" className="mt-6">
          <Card className="bg-slate-800 border-slate-700">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Sliders className="w-5 h-5 text-indigo-400" /> Configuração de Pesos de Cargos
              </CardTitle>
            </CardHeader>
            <CardContent>
              {weights.length > 0 ? (
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Cargo</TableHead>
                      <TableHead>Empatia</TableHead>
                      <TableHead>Liderança</TableHead>
                      <TableHead>Inovação</TableHead>
                      <TableHead>Organização</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {weights.map((w, i) => (
                      <TableRow key={i}>
                        <TableCell>{w.cargo}</TableCell>
                        {["empatia", "lideranca", "inovacao", "organizacao"].map((k) => (
                          <TableCell key={k}>
                            <Input
                              type="number"
                              min="0"
                              max="100"
                              value={w[k]}
                              onChange={(e) => {
                                const val = Number(e.target.value);
                                const updated = [...weights];
                                updated[i][k] = val;
                                setWeights(updated);
                              }}
                              className="w-20 text-center bg-slate-900 border-slate-700"
                            />
                          </TableCell>
                        ))}
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              ) : (
                <p>Nenhum cargo configurado.</p>
              )}

              <Button
                onClick={saveWeights}
                className="mt-4 bg-indigo-600 hover:bg-indigo-700"
                disabled={saving}
              >
                {saving ? "Salvando..." : "Salvar Alterações"}
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Templates */}
        <TabsContent value="templates" className="mt-6">
          <Card className="bg-slate-800 border-slate-700">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Settings className="w-5 h-5 text-indigo-400" /> Gerenciar Templates
              </CardTitle>
            </CardHeader>
            <CardContent>
              {templates.length > 0 ? (
                <ul className="space-y-2">
                  {templates.map((t, i) => (
                    <li key={i} className="bg-slate-900 border border-slate-800 rounded p-3">
                      <p className="font-semibold">{t.nome}</p>
                      <p className="text-sm text-gray-400">{t.descricao}</p>
                    </li>
                  ))}
                </ul>
              ) : (
                <p>Nenhum template cadastrado.</p>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </motion.div>
  );
}
