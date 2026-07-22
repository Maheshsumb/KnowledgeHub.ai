import { createBrowserRouter, Navigate } from "react-router-dom"
import { PublicLayout } from "@/components/layouts/PublicLayout"
import { DashboardLayout } from "@/components/layouts/DashboardLayout"
import { ProtectedRoute } from "@/components/layouts/ProtectedRoute"
import { GuestRoute } from "@/components/layouts/GuestRoute"

import { LoginPage } from "@/pages/auth/LoginPage"
import { RegisterPage } from "@/pages/auth/RegisterPage"
import { DashboardPage } from "@/pages/dashboard/DashboardPage"
import { OrganizationsPage } from "@/pages/organizations/OrganizationsPage"
import { OrganizationDetailsPage } from "@/pages/organizations/OrganizationDetailsPage"
import { WorkspaceDetailsPage } from "@/pages/workspaces/WorkspaceDetailsPage"
import { WorkspacesPage } from "@/pages/workspaces/WorkspacesPage"
import { SettingsPage } from "@/pages/settings/SettingsPage"

export const router = createBrowserRouter([
  {
    path: "/",
    element: <Navigate to="/dashboard" replace />,
  },
  {
    element: <GuestRoute />,
    children: [
      {
        element: <PublicLayout />,
        children: [
          {
            path: "login",
            element: <LoginPage />,
          },
          {
            path: "register",
            element: <RegisterPage />,
          },
        ],
      },
    ],
  },
  {
    element: <ProtectedRoute />,
    children: [
      {
        element: <DashboardLayout />,
        children: [
          {
            path: "dashboard",
            element: <DashboardPage />,
          },
          {
            path: "organizations",
            element: <OrganizationsPage />,
          },
          {
            path: "organizations/:id",
            element: <OrganizationDetailsPage />,
          },
          {
            path: "organizations/:id/workspaces/:workspaceId",
            element: <WorkspaceDetailsPage />,
          },
          {
            path: "workspaces",
            element: <WorkspacesPage />,
          },
          {
            path: "documents",
            element: <div className="p-6">Documents Placeholder</div>,
          },
          {
            path: "chat",
            element: <div className="p-6">Chat Placeholder</div>,
          },
          {
            path: "settings",
            element: <SettingsPage />,
          },
        ],
      },
    ],
  },
])
