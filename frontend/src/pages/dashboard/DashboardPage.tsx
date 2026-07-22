import { useQuery } from "@tanstack/react-query"
import { Building2, FolderGit2, FileText, Activity, Plus, CheckCircle2, AlertCircle } from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Skeleton } from "@/components/ui/skeleton"
import { dashboardService } from "@/api/dashboard.service"

import { useNavigate } from "react-router-dom"

export function DashboardPage() {
  const navigate = useNavigate()

  const { data: stats, isLoading: isStatsLoading } = useQuery({
    queryKey: ["dashboard", "stats"],
    queryFn: dashboardService.getStats,
    retry: false, // Don't retry since endpoints might not exist yet
  })

  const { data: activity, isLoading: isActivityLoading } = useQuery({
    queryKey: ["dashboard", "activity"],
    queryFn: dashboardService.getRecentActivity,
    retry: false,
  })

  const { data: systemStatus, isLoading: isStatusLoading } = useQuery({
    queryKey: ["dashboard", "status"],
    queryFn: dashboardService.getSystemStatus,
    retry: false,
  })

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Dashboard</h2>
          <p className="text-muted-foreground">
            Overview of your KnowledgeHub AI platform.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button onClick={() => navigate("/organizations")}>
            <Plus className="mr-2 h-4 w-4" />
            New Organization
          </Button>
        </div>
      </div>

      {/* Stats Overview */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Organizations</CardTitle>
            <Building2 className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            {isStatsLoading ? (
              <Skeleton className="h-8 w-16" />
            ) : (
              <div className="text-2xl font-bold">{stats?.organizations_count ?? "—"}</div>
            )}
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Workspaces</CardTitle>
            <FolderGit2 className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            {isStatsLoading ? (
              <Skeleton className="h-8 w-16" />
            ) : (
              <div className="text-2xl font-bold">{stats?.workspaces_count ?? "—"}</div>
            )}
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Documents</CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            {isStatsLoading ? (
              <Skeleton className="h-8 w-16" />
            ) : (
              <div className="text-2xl font-bold">{stats?.documents_count ?? "—"}</div>
            )}
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
        {/* Recent Activity */}
        <Card className="lg:col-span-4">
          <CardHeader>
            <CardTitle>Recent Activity</CardTitle>
            <CardDescription>Latest actions across your organizations.</CardDescription>
          </CardHeader>
          <CardContent>
            {isActivityLoading ? (
              <div className="space-y-4">
                <Skeleton className="h-12 w-full" />
                <Skeleton className="h-12 w-full" />
                <Skeleton className="h-12 w-full" />
              </div>
            ) : activity && activity.length > 0 ? (
              <div className="space-y-4">
                {activity.map((item) => (
                  <div key={item.id} className="flex items-center gap-4 border-b pb-4 last:border-0 last:pb-0">
                    <Activity className="h-4 w-4 text-muted-foreground" />
                    <div className="grid gap-1">
                      <p className="text-sm font-medium leading-none">
                        {item.action} {item.entity_type}
                      </p>
                      <p className="text-sm text-muted-foreground">
                        {item.entity_name} • {new Date(item.created_at).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="flex h-32 items-center justify-center text-sm text-muted-foreground border rounded-lg border-dashed">
                No recent activity.
              </div>
            )}
          </CardContent>
        </Card>

        {/* Sidebar / Quick Actions & Status */}
        <div className="grid gap-4 lg:col-span-3">
          <Card>
            <CardHeader>
              <CardTitle>Quick Actions</CardTitle>
            </CardHeader>
            <CardContent className="grid gap-2">
              <Button variant="outline" className="justify-start" onClick={() => navigate("/organizations")}>
                <Building2 className="mr-2 h-4 w-4" />
                Manage Organizations
              </Button>
              <Button variant="outline" className="justify-start" onClick={() => navigate("/workspaces")}>
                <FolderGit2 className="mr-2 h-4 w-4" />
                View Workspaces
              </Button>
              <Button variant="outline" className="justify-start" onClick={() => navigate("/documents")}>
                <FileText className="mr-2 h-4 w-4" />
                Upload Document
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>System Status</CardTitle>
            </CardHeader>
            <CardContent>
              {isStatusLoading ? (
                <div className="space-y-2">
                  <Skeleton className="h-4 w-full" />
                  <Skeleton className="h-4 w-3/4" />
                </div>
              ) : systemStatus ? (
                <div className="flex items-center gap-4">
                  {systemStatus.status === "operational" ? (
                    <CheckCircle2 className="h-8 w-8 text-green-500" />
                  ) : (
                    <AlertCircle className="h-8 w-8 text-destructive" />
                  )}
                  <div className="grid gap-1">
                    <p className="text-sm font-medium leading-none">
                      {systemStatus.status === "operational" ? "All Systems Operational" : "System Degraded"}
                    </p>
                    <p className="text-sm text-muted-foreground">
                      Version {systemStatus.version}
                    </p>
                  </div>
                </div>
              ) : (
                <div className="text-sm text-muted-foreground">
                  Status unavailable.
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
