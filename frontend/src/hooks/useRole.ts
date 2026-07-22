import { useAuthStore } from "@/store/auth.store"
import type { Role, Membership } from "@/api/membership.service"

const roleHierarchy: Record<Role, number> = {
  OWNER: 4,
  ADMIN: 3,
  MEMBER: 2,
  VIEWER: 1,
}

export function useRole(memberships: Membership[] = []) {
  const { user } = useAuthStore()

  // Find the current user's role in this organization
  const currentMembership = memberships.find((m) => m.user_id === user?.id)
  const currentRole = currentMembership?.role

  // Check if user has at least the required role
  const hasRole = (requiredRole: Role) => {
    if (!currentRole) return false
    return roleHierarchy[currentRole] >= roleHierarchy[requiredRole]
  }

  // Permission checks
  const canManageMembers = hasRole("ADMIN")
  const canDeleteOrganization = hasRole("OWNER")
  const canUpdateRole = (targetRole: Role) => {
    if (!currentRole) return false
    // Cannot manage someone with higher or equal role unless OWNER
    if (currentRole === "OWNER") return true
    return roleHierarchy[currentRole] > roleHierarchy[targetRole]
  }

  return {
    currentRole,
    hasRole,
    canManageMembers,
    canDeleteOrganization,
    canUpdateRole,
  }
}
