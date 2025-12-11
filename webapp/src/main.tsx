import React from "react";
import ReactDOM from "react-dom/client";

import App from "./App";
import Login from "./Login";
import AdminConsole from "./AdminConsole";
import Analytics from "./Analytics";
import LiveMonitor from "./LiveMonitor";

function handleLogin(token: string, redirect: string) {
  localStorage.setItem("ms_token", token);
  window.location.href = redirect;
}

function resolveRootComponent() {
  const path = window.location.pathname;
  const token = localStorage.getItem("ms_token");

  if (path.startsWith("/live")) {
    if (!token) return <Login onLogin={(t) => handleLogin(t, "/live")} />;
    return <LiveMonitor />;
  }

  if (path.startsWith("/analytics")) {
    if (!token) return <Login onLogin={(t) => handleLogin(t, "/analytics")} />;
    return <Analytics />;
  }

  if (path.startsWith("/admin")) {
    if (!token) return <Login onLogin={(t) => handleLogin(t, "/admin")} />;
    return <AdminConsole />;
  }

  if (path.startsWith("/login")) {
    return <Login onLogin={(t) => handleLogin(t, "/")} />;
  }

  return <App />;
}

ReactDOM.createRoot(document.getElementById("root")!).render(resolveRootComponent());
