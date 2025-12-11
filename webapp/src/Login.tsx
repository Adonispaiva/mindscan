import React, { useState } from "react";

export default function Login({ onLogin }: { onLogin: (token: string) => void }) {
  const [user, setUser] = useState("admin");
  const [pass, setPass] = useState("admin123");
  const [error, setError] = useState("");

  async function submit() {
    setError("");
    const res = await fetch("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: user, password: pass })
    });

    const data = await res.json();
    if (data?.access_token) {
      onLogin(data.access_token);
    } else {
      setError("Credenciais inválidas");
    }
  }

  return (
    <div style={styles.box}>
      <h2>Login MindScan</h2>

      <input
        style={styles.input}
        value={user}
        onChange={(e) => setUser(e.target.value)}
        placeholder="usuário"
      />

      <input
        style={styles.input}
        type="password"
        value={pass}
        onChange={(e) => setPass(e.target.value)}
        placeholder="senha"
      />

      <button style={styles.btn} onClick={submit}>Entrar</button>

      {error && <p style={styles.err}>{error}</p>}
    </div>
  );
}

const styles: any = {
  box: {
    margin: "80px auto",
    maxWidth: "400px",
    padding: "20px",
    background: "#fff",
    borderRadius: "12px",
    boxShadow: "0 3px 12px rgba(0,0,0,0.2)",
    textAlign: "center"
  },
  input: {
    width: "100%",
    padding: "10px",
    margin: "10px 0"
  },
  btn: {
    width: "100%",
    padding: "12px",
    background: "black",
    color: "white",
    borderRadius: "8px",
    cursor: "pointer"
  },
  err: {
    color: "red",
    marginTop: "10px"
  }
};
