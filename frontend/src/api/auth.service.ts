import { apiClient } from "./client"
import type { User } from "@/store/auth.store"

export interface LoginCredentials {
  username: string // FastAPI OAuth2PasswordRequestForm expects username
  password: string
}

export interface RegisterCredentials {
  email: string
  password: string
  confirm_password: string
  full_name: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
}

export const authService = {
  login: async (credentials: LoginCredentials): Promise<TokenResponse> => {
    const response = await apiClient.post<TokenResponse>("/auth/login", {
      email: credentials.username, // mapping username to email as expected by backend
      password: credentials.password
    })
    return response.data
  },

  register: async (data: RegisterCredentials): Promise<void> => {
    await apiClient.post("/auth/register", data)
  },

  logout: async (): Promise<void> => {
    await apiClient.post("/auth/logout")
  },

  getMe: async (): Promise<User> => {
    const response = await apiClient.get<User>("/users/me")
    return response.data
  },
}
