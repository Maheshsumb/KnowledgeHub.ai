import React, { useEffect, useState } from "react"
import { useAuthStore } from "@/store/auth.store"
import { authService } from "@/api/auth.service"
import { Loader2 } from "lucide-react"

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [isInitializing, setIsInitializing] = useState(true)
  const { accessToken, clearAuth, updateUser, isAuthenticated } = useAuthStore()

  useEffect(() => {
    let isMounted = true

    const initializeAuth = async () => {
      if (!accessToken || !isAuthenticated) {
        if (isMounted) setIsInitializing(false)
        return
      }

      try {
        const user = await authService.getMe()
        if (isMounted) {
          updateUser(user)
        }
      } catch (error) {
        if (isMounted) {
          clearAuth()
        }
      } finally {
        if (isMounted) {
          setIsInitializing(false)
        }
      }
    }

    initializeAuth()

    return () => {
      isMounted = false
    }
  }, [accessToken, isAuthenticated, clearAuth, updateUser])

  if (isInitializing) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    )
  }

  return <>{children}</>
}
