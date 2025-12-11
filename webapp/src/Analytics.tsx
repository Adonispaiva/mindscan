import React, { useEffect, useState } from "react";
import { Bar, Pie, Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  ArcElement,
  PointElement,
  LineElement
} from "chart.js";

ChartJS.register(
  BarElement,
  CategoryScale,
  LinearScale,
  ArcElement,
  PointElement,
  LineElement
);

export default function Analytics() {
  const [data, setData] = useState<any>(null);

  async function load() {
    const res = await fetch("/api/analytics/summary");
    const d = await res.json();
    setData(d);
  }

  useEffect(() => {
    load();
  }, []);

  if (!data) return <p style={{ textAlign: "center", marginTop: 40 }}>Carregando...</p>;

  // Preparar datasets
  const modesData = {
    labels: Object.keys(data.modes),
    datasets: [
      {
        label: "Modos MI utilizados",
        data: Object.values(data.modes),
        backgroundColor: "#000"
      }
    ]
  };

  const typesData = {
    labels: Object.keys(data.report_types),
    datasets: [
      {
        label: "Tipos de relatório",
        data: Object.values(data.report_types),
        backgroundColor: "#444"
      }
    ]
  };

  const perDayData = {
    labels: Object.keys(data.per_day),
    datasets: [
      {
        label: "Relatórios por dia",
        data: Object.values(data.per_day),
        borderColor: "#000",
        fill: false
      }
    ]
  };

  return (
    <div style={styles.container}>
      <h1>MindScan — Analytics</h1>
      <p>Total de relatórios: <b>{data.total_reports}</b></p>
      <p>Média geral MI Score: <b>{data.avg_score.toFixed(3)}</b></p>

      <div style={styles.chartBox}>
        <h3>Distribuição dos Modos MI</h3>
        <Pie data={modesData} />
      </div>

      <div style={styles.chartBox}>
        <h3>Distribuição dos Tipos de Relatório</h3>
        <Bar data={typesData} />
      </div>

      <div style={styles.chartBox}>
        <h3>Volume diário de relatórios</h3>
        <Line data={perDayData} />
      </div>
    </div>
  );
}

const styles: any = {
  container: {
    maxWidth: "900px",
    margin: "40px auto",
    padding: "20px",
    background: "#fff",
    borderRadius: "12px",
    boxShadow: "0 4px 16px rgba(0,0,0,0.1)"
  },
  chartBox: {
    marginTop: "40px",
    padding: "20px",
    background: "#fafafa",
    borderRadius: "12px"
  }
};
