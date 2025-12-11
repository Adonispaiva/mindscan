import React, { useEffect, useState } from "react";

export default function LiveMonitor() {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    const evt = new EventSource("/api/live/stream");

    evt.onmessage = (msg) => {
      try {
        const payload = JSON.parse(msg.data);
        setData(payload);
      } catch (err) {
        console.error("Erro SSE:", err);
      }
    };

    evt.onerror = () => console.error("Erro SSE");

    return () => evt.close();
  }, []);

  if (!data) return <p style={styles.loading}>Carregando streaming...</p>;

  return (
    <div style={styles.box}>
      <h1>MindScan — Live Monitor</h1>

      <p>Total últimos registros: <b>{data.total_recent}</b></p>
      <p>Média recente MI Score: <b>{data.avg_score_recent.toFixed(3)}</b></p>

      <h3>Distribuição de Modos (últimos 80 relatórios)</h3>
      <ul>
        {Object.entries(data.mode_distribution).map(([m, v]: any) => (
          <li key={m}>{m}: {v}</li>
        ))}
      </ul>

      <h3>Últimos sujeitos processados</h3>
      <div style={styles.list}>
        {data.recent.map((e: any, i: number) => (
          <div key={i} style={styles.item}>
            <b>{e.subject_id}</b> — {e.mode} (score: {e.score})
            <br />
            <small>{e.timestamp}</small>
          </div>
        ))}
      </div>
    </div>
  );
}

const styles: any = {
  box: {
    maxWidth: "900px",
    margin: "40px auto",
    padding: "20px",
    background: "#fff",
    borderRadius: "12px",
    boxShadow: "0 3px 16px rgba(0,0,0,0.15)"
  },
  loading: {
    marginTop: "40px",
    textAlign: "center"
  },
  list: {
    marginTop: "20px"
  },
  item: {
    padding: "10px",
    borderBottom: "1px solid #ddd"
  }
};
