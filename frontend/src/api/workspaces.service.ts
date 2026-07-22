import { apiClient } from "./client"

export interface Workspace {
  id: string
  name: string
  description?: string
  organization_id: string
  created_at: string
  updated_at: string
}

export interface WorkspaceCreate {
  name: string
  description?: string
}

export interface WorkspaceUpdate {
  name?: string
  description?: string
}

export const workspacesService = {
  getWorkspaces: async (organizationId: string) => {
    const { data } = await apiClient.get<Workspace[]>(`/organizations/${organizationId}/workspaces`)
    return data
  },

  getWorkspace: async (organizationId: string, workspaceId: string) => {
    const { data } = await apiClient.get<Workspace>(`/organizations/${organizationId}/workspaces/${workspaceId}`)
    return data
  },

  createWorkspace: async (organizationId: string, payload: WorkspaceCreate) => {
    const { data } = await apiClient.post<Workspace>(`/organizations/${organizationId}/workspaces`, payload)
    return data
  },

  updateWorkspace: async (organizationId: string, workspaceId: string, payload: WorkspaceUpdate) => {
    const { data } = await apiClient.patch<Workspace>(`/organizations/${organizationId}/workspaces/${workspaceId}`, payload)
    return data
  },

  deleteWorkspace: async (organizationId: string, workspaceId: string) => {
    await apiClient.delete(`/organizations/${organizationId}/workspaces/${workspaceId}`)
  },
}
