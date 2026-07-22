import { apiClient } from "./client"

export interface Organization {
  id: string
  name: string
  description?: string
  created_at: string
  updated_at: string
}

export interface OrganizationCreate {
  name: string
  description?: string
}

export interface OrganizationUpdate {
  name: string
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  size: number
  pages: number
}

export const organizationsService = {
  getOrganizations: async (
    page = 1,
    size = 10,
    search?: string
  ): Promise<PaginatedResponse<Organization>> => {
    const params = new URLSearchParams({
      page: page.toString(),
      size: size.toString(),
    })
    if (search) params.append("search", search)

    // Ensure this matches FastAPI's expected structure or handle locally
    const response = await apiClient.get<PaginatedResponse<Organization>>("/organizations", {
      params,
    })
    
    // If backend returns a flat array instead of paginated response currently, adapt it here for robustness
    if (Array.isArray(response.data)) {
        return {
            items: response.data,
            total: response.data.length,
            page: 1,
            size: response.data.length,
            pages: 1
        }
    }

    return response.data
  },

  getOrganization: async (id: string): Promise<Organization> => {
    const response = await apiClient.get<Organization>(`/organizations/${id}`)
    return response.data
  },

  createOrganization: async (data: OrganizationCreate): Promise<Organization> => {
    const response = await apiClient.post<Organization>("/organizations", data)
    return response.data
  },

  updateOrganization: async (id: string, data: OrganizationUpdate): Promise<Organization> => {
    const response = await apiClient.patch<Organization>(`/organizations/${id}`, data)
    return response.data
  },

  deleteOrganization: async (id: string): Promise<void> => {
    await apiClient.delete(`/organizations/${id}`)
  },
}
