// D:\MindScan\src\pages\admin\AdminDashboard.tsx
import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { BarChart3, Brain, UserCog, RefreshCcw } from "lucide-react";
import { motion } from "framer-motion";

export default function AdminDashboard() {
  const [activeTab, setActiveTab] = useState("diagnostics");
  const [stats, setStats] = useState({ diagnostics: 0, users: 0, reports: 0 });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      setLoading(true);
      const res = await fetch("/api/admin/overview");
      const data = await res.json();
      setStats(data);
    } catch (err) {
      console.error("Erro ao carregar estatísticas:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="p-6 max-w-6xl mx-auto"
    >
      <Card className="mb-6 shadow-md rounded-2xl">
        <CardHeader className="flex justify-between items-center">
          <CardTitle className="text-2xl font-bold flex items-center gap-2">
            <UserCog size={24} /> Painel Administrativo — SynMind Control
          </CardTitle>
          <Button variant="outline" onClick={fetchStats} disabled={loading}>
            <RefreshCcw size={18} className="mr-2" /> Atualizar
          </Button>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <StatCard icon={<Brain />} label="Diagnósticos" value={stats.diagnostics} />
            <StatCard icon={<UserCog />} label="Usuários" value={stats.users} />
            <StatCard icon={<BarChart3 />} label="Relatórios" value={stats.reports} />
          </div>
        </CardContent>
      </Card>

      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="mb-4">
          <TabsTrigger value="diagnostics">Diagnósticos</TabsTrigger>
          <TabsTrigger value="users">Usuários</TabsTrigger>
          <TabsTrigger value="reports">Relatórios</TabsTrigger>
        </TabsList>

        <TabsContent value="diagnostics">
          <DiagnosticsPanel />
        </TabsContent>
        <TabsContent value="users">
          <UsersPanel />
        </TabsContent>
        <TabsContent value="reports">
          <ReportsPanel />
        </TabsContent>
      </Tabs>
    </motion.div>
  );
}

function StatCard({ icon, label, value }: { icon: JSX.Element; label: string; value: number }) {
  return (
    <Card className="rounded-xl border border-gray-200">
      <CardContent className="p-4 flex flex-col items-center">
        <div className="text-gray-500 mb-1">{icon}</div>
        <div className="text-sm text-gray-600">{label}</div>
        <div className="text-2xl font-semibold mt-1">{value}</div>
      </CardContent>
    </Card>
  );
}

function DiagnosticsPanel() {
  return (
    <Card className="p-4">
      <CardHeader>
        <CardTitle>Diagnósticos Recentes</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-gray-600">Visualização e análise dos últimos diagnósticos realizados.</p>
      </CardContent>
    </Card>
  );
}

function UsersPanel() {
  return (
    <Card className="p-4">
      <CardHeader>
        <CardTitle>Gestão de Usuários</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-gray-600">Listagem e controle de acessos dos usuários registrados.</p>
      </CardContent>
    </Card>
  );
}

function ReportsPanel() {
  return (
    <Card className="p-4">
      <CardHeader>
        <CardTitle>Relatórios Gerados</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-gray-600">Painel de relatórios e históricos de performance.</p>
      </CardContent>
    </Card>
  );
}
