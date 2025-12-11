import React, { useEffect, useState } from "react";

export default function AdminConsole() {
  const [logs, setLogs] = useState([]);

  async function load() {
    const res = await fetch("/api/admin/reports");
    const data = await res.json();
    setLogs(data);
  }

  useEffect(() => {
    load();
  }, []);

  return (
    <div style={styles.box}>
      <h2>Painel Administrativo — MindScan</h2>

      <button style={styles.btn} onClick={load}>
        Atualizar
      </button>

      <div style={styles.list}>
        {logs.map((l: any, i) => (
          <div key={i} style={styles.item}>
            <b>{l.subject_id}</b> — {l.mi_mode} — score {l.mi_score}
            <br />
            Relatório: <a href={l.pdf_url} target="_blank">abrir</a>
            <br />
            <small>{l.timestamp}</small>
          </div>
        ))}
      </div>
    </div>
  );
}

const styles: any = {
  box: {
    maxWidth: "800px",
    margin: "40px auto",
    background: "#fff",
    padding: "20px",
    borderRadius: "12px",
    boxShadow: "0 3px 16px rgba(0,0,0,0.15)"
  },
  btn: {
    padding: "10px",
    background: "#000",
    color: "#fff",
    borderRadius: "8px",
    cursor: "pointer",
    marginBottom: "20px"
  },
  list: {
    marginTop: "20px"
  },
  item: {
    padding: "12px",
    borderBottom: "1px solid #ddd",
    lineHeight: "1.4"
  }
};
