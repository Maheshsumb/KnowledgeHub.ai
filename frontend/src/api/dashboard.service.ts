import { apiClient } from "./client"

export interface DashboardStats {
  organizations_count: number
  workspaces_count: number
  documents_count: number
}

export interface ActivityItem {
  id: string
  action: string
  entity_type: string
  entity_name: string
  created_at: string
}

export interface SystemStatus {
  status: "operational" | "degraded" | "down"
  version: string
}

interface HealthResponse {
  status: string
  version: string
}

export const dashboardService = {
  getStats: async (): Promise<DashboardStats> => {
    const response = await apiClient.get<DashboardStats>("/dashboard/stats")
    return response.data
  },

  getRecentActivity: async (): Promise<ActivityItem[]> => {
    const response = await apiClient.get<ActivityItem[]>("/dashboard/activity")
    return response.data
  },

  getSystemStatus: async (): Promise<SystemStatus> => {
    const response = await apiClient.get<HealthResponse>("/health")
    return {
      status: response.data.status === "healthy" ? "operational" : "degraded",
      version: response.data.version || "1.0.0"
    }
  },
}
