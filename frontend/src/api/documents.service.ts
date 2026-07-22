import { apiClient } from "./client"

export interface Document {
  id: string
  workspace_id: string
  name: string
  status: "UPLOADING" | "PROCESSING" | "READY" | "FAILED"
  file_path: string
  metadata_info: Record<string, any>
  created_at: string
  updated_at: string
}

export const documentsService = {
  getDocuments: async (organizationId: string, workspaceId: string) => {
    const { data } = await apiClient.get<Document[]>(
      `/organizations/${organizationId}/workspaces/${workspaceId}/documents`
    )
    return data
  },

  getDocument: async (organizationId: string, workspaceId: string, documentId: string) => {
    const { data } = await apiClient.get<Document>(
      `/organizations/${organizationId}/workspaces/${workspaceId}/documents/${documentId}`
    )
    return data
  },

  uploadDocument: async (organizationId: string, workspaceId: string, file: File) => {
    const formData = new FormData()
    formData.append("file", file)
    
    const { data } = await apiClient.post<Document>(
      `/organizations/${organizationId}/workspaces/${workspaceId}/documents`,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    )
    return data
  },

  deleteDocument: async (organizationId: string, workspaceId: string, documentId: string) => {
    await apiClient.delete(
      `/organizations/${organizationId}/workspaces/${workspaceId}/documents/${documentId}`
    )
  },
}
