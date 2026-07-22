import { Navigate, Outlet, useLocation } from "react-router-dom"
import { useAuthStore } from "@/store/auth.store"

export function GuestRoute() {
  const { isAuthenticated } = useAuthStore()
  const location = useLocation()

  const from = location.state?.from?.pathname || "/dashboard"

  if (isAuthenticated) {
    return <Navigate to={from} replace />
  }

  return <Outlet />
}
