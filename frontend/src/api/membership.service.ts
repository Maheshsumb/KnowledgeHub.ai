import { apiClient } from "./client"

export type Role = "OWNER" | "ADMIN" | "MEMBER" | "VIEWER"

export interface Membership {
  id: string
  user_id: string
  organization_id: string
  role: Role
  user?: {
    id: string
    full_name: string
    email: string
  }
}

export interface MembershipCreate {
  user_id: string
  role: Role
}

export const membershipService = {
  getMembers: async (organizationId: string): Promise<Membership[]> => {
    const response = await apiClient.get<Membership[]>(`/organizations/${organizationId}/members`)
    return response.data
  },

  addMember: async (organizationId: string, data: MembershipCreate): Promise<Membership> => {
    const response = await apiClient.post<Membership>(`/organizations/${organizationId}/members`, data)
    return response.data
  },

  // Assuming backend doesn't have a PATCH endpoint, you'd typically need one for updateRole,
  // or it relies on addMember to upsert. We'll define it assuming standard REST.
  updateRole: async (organizationId: string, userId: string, role: Role): Promise<Membership> => {
    const response = await apiClient.patch<Membership>(`/organizations/${organizationId}/members/${userId}`, { role })
    return response.data
  },

  removeMember: async (organizationId: string, userId: string): Promise<void> => {
    await apiClient.delete(`/organizations/${organizationId}/members/${userId}`)
  },
}
