// Auto-gerado pelo MindScan AutoDeliver
// Cliente mínimo para endpoints administrativos da API MindScan (SynMind).
// Pode ser utilizado por painéis internos, scripts ou serviços Node/TS.

import axios, { AxiosInstance } from "axios";

export interface HealthStatus {
  status: string;
  uptime?: number;
  version?: string;
  details?: Record<string, unknown>;
}

export interface AdminStats {
  users_total?: number;
  diagnostics_total?: number;
  last_run_at?: string;
  [key: string]: unknown;
}

export class AdminAPI {
  private client: AxiosInstance;

  /**
   * @param baseURL Base da API.
   * Ex.: "/api" se o backend expõe "/api/admin/...", ou "" se expõe "/admin/...".
   */
  constructor(baseURL: string = "/api") {
    this.client = axios.create({
      baseURL,
      withCredentials: true,
    });
  }

  /**
   * GET /admin/health
   * Retorna o status de saúde geral do backend MindScan.
   */
  async getHealth(): Promise<HealthStatus> {
    const resp = await this.client.get<HealthStatus>("/admin/health");
    return resp.data;
  }

  /**
   * GET /admin/stats
   * Retorna estatísticas agregadas (usuários, diagnósticos, etc.).
   */
  async getStats(): Promise<AdminStats> {
    const resp = await this.client.get<AdminStats>("/admin/stats");
    return resp.data;
  }

  /**
   * POST /admin/sync
   * Dispara rotinas de sincronização administrativa (ex.: SynMind, cache, etc.).
   */
  async triggerSync(payload?: Record<string, unknown>): Promise<unknown> {
    const resp = await this.client.post("/admin/sync", payload ?? {});
    return resp.data;
  }
}

export const adminAPI = new AdminAPI();
