# -*- coding: utf-8 -*-
"""
MindScan Command Center v1.2.1 — Inovexa Software
Diretor Técnico: Leo Vinci
Descrição:
Interface principal do Painel Supervisor MindScan.
Gerencia exibição de eventos, status do sistema, logs e telemetria em tempo real.
Agora com suporte total a UTF-8 no console do Windows e hora local (UTC-3).
"""

import os
import time
import json
from datetime import datetime, timezone, timedelta
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.layout import Layout

# === CONFIGURAÇÕES GERAIS ===
EVENTS_FILE = os.path.join(os.path.dirname(__file__), "..", "notifiers", "notifier_events.json")
console = Console()
system_status = "OK"

# === FUNÇÕES DE SUPORTE ===
def local_time():
    """Retorna o horário local (UTC-3)"""
    br_time = datetime.now(timezone.utc) - timedelta(hours=3)
    return br_time.strftime("%Y-%m-%d %H:%M:%S")

def load_events():
    """Carrega eventos do arquivo JSON."""
    if not os.path.exists(EVENTS_FILE):
        return []
    try:
        with open(EVENTS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data[-20:]  # últimos 20 eventos
    except Exception:
        return []

def build_table(events):
    """Monta a tabela principal de eventos."""
    table = Table(show_header=True, header_style="bold magenta", expand=True)
    table.add_column("Horário (Local)", width=25)
    table.add_column("Evento", width=70)
    table.add_column("Status", width=10)

    for e in events:
        ts = e.get("timestamp", "-")
        ev = e.get("event", "-")
        st = e.get("status", "OK")
        color = "green" if st == "OK" else "red"
        table.add_row(ts, ev, f"[{color}]{st}[/{color}]")
    return table

def build_footer(events):
    """Monta o rodapé do painel."""
    total = len(events)
    errors = sum(1 for e in events if e.get("status") == "ERROR")
    last_event = events[-1]["timestamp"] if total > 0 else "-"
    footer_text = (
        f"[cyan]Eventos:[/cyan] {total} | "
        f"[red]Erros:[/red] {errors} | "
        f"[yellow]Último:[/yellow] {last_event}"
    )
    return footer_text

def build_layout():
    """Estrutura geral da tela."""
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1),
        Layout(name="footer", size=1)
    )
    return layout

# === CABEÇALHO ===
def header_panel():
    title = Text("🧠 MindScan Supervisor Live — Inovexa Command Center", style="bold white on magenta")
    return Panel(title, expand=True, border_style="bright_magenta")

# === CORPO ===
def body_panel(events):
    return Panel(build_table(events), border_style="cyan", title="Eventos", title_align="left")

# === RODAPÉ ===
def footer_panel(events):
    return Panel(build_footer(events), border_style="blue")

# === EXECUÇÃO PRINCIPAL ===
def main():
    os.system("cls" if os.name == "nt" else "clear")
    console.print("🧠 MindScan Command Center v1.2.1 — Inovexa Software\n", style="bold magenta")

    layout = build_layout()

    with Live(layout, refresh_per_second=1, screen=True):
        while True:
            events = load_events()
            layout["header"].update(header_panel())
            layout["body"].update(body_panel(events))
            layout["footer"].update(footer_panel(events))
            time.sleep(1)

if __name__ == "__main__":
    main()
