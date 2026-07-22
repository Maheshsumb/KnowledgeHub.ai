import { useQuery, useQueries } from "@tanstack/react-query"
import { Building2, FolderGit2, ArrowRight } from "lucide-react"
import { Link } from "react-router-dom"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Skeleton } from "@/components/ui/skeleton"
import { EmptyState } from "@/components/ui/empty-state"
import { organizationsService } from "@/api/organizations.service"
import { workspacesService, type Workspace } from "@/api/workspaces.service"

export function WorkspacesPage() {
  const { data: orgData, isLoading: isLoadingOrgs } = useQuery({
    queryKey: ["organizations"],
    queryFn: () => organizationsService.getOrganizations(1, 50, ""),
  })

  const workspaceQueries = useQueries({
    queries: (orgData?.items || []).map((org) => ({
      queryKey: ["workspaces", org.id],
      queryFn: () => workspacesService.getWorkspaces(org.id),
      enabled: !!org.id,
    })),
  })

  const isLoadingWorkspaces = workspaceQueries.some((query) => query.isLoading)
  const allWorkspaces = workspaceQueries
    .map((query) => query.data || [])
    .flat()

  const isLoading = isLoadingOrgs || isLoadingWorkspaces

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold tracking-tight">Workspaces</h2>
        <p className="text-muted-foreground">
          View and manage all your workspaces across your organizations.
        </p>
      </div>

      {isLoading ? (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          <Skeleton className="h-[160px] w-full" />
          <Skeleton className="h-[160px] w-full" />
          <Skeleton className="h-[160px] w-full" />
        </div>
      ) : orgData?.items?.length === 0 ? (
        <EmptyState
          icon={Building2}
          title="No organizations found"
          description="You need to be part of an organization to manage workspaces."
          action={
            <Button asChild>
              <Link to="/organizations">Go to Organizations</Link>
            </Button>
          }
        />
      ) : allWorkspaces.length === 0 ? (
        <EmptyState
          icon={FolderGit2}
          title="No workspaces found"
          description="Create a workspace in one of your organizations to get started."
          action={
            <Button asChild>
              <Link to="/organizations">Go to Organizations</Link>
            </Button>
          }
        />
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {allWorkspaces.map((workspace) => (
            <Card key={workspace.id} className="hover:border-primary/50 transition-colors">
              <CardHeader>
                <div className="flex items-center gap-2 mb-2">
                  <div className="p-2 bg-primary/10 rounded-lg">
                    <FolderGit2 className="h-5 w-5 text-primary" />
                  </div>
                  <CardTitle className="text-lg">{workspace.name}</CardTitle>
                </div>
                {workspace.description && (
                  <CardDescription className="line-clamp-2">{workspace.description}</CardDescription>
                )}
              </CardHeader>
              <CardContent>
                <Button asChild variant="outline" className="w-full justify-between">
                  <Link to={`/organizations/${workspace.organization_id}/workspaces/${workspace.id}`}>
                    <span className="flex items-center">
                      View Workspace
                    </span>
                    <ArrowRight className="h-4 w-4" />
                  </Link>
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}

