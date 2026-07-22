import { useParams, Link } from "react-router-dom"
import { useQuery } from "@tanstack/react-query"
import { FileText, MessageSquare, Settings, ArrowLeft } from "lucide-react"

import { Skeleton } from "@/components/ui/skeleton"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Button } from "@/components/ui/button"
import { workspacesService } from "@/api/workspaces.service"

import { DocumentsList } from "./components/documents/DocumentsList"

export function WorkspaceDetailsPage() {
  const { id, workspaceId } = useParams<{ id: string; workspaceId: string }>()

  const { data: workspace, isLoading } = useQuery({
    queryKey: ["workspaces", id, workspaceId],
    queryFn: () => workspacesService.getWorkspace(id!, workspaceId!),
    enabled: !!id && !!workspaceId,
  })

  if (isLoading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-10 w-1/3" />
        <Skeleton className="h-[400px] w-full" />
      </div>
    )
  }

  if (!workspace) {
    return (
      <div className="flex h-[400px] flex-col items-center justify-center text-center">
        <h3 className="text-lg font-semibold">Workspace not found</h3>
        <p className="text-muted-foreground">The workspace you are looking for does not exist.</p>
        <Button asChild className="mt-4" variant="outline">
          <Link to={`/organizations/${id}`}>
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Organization
          </Link>
        </Button>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button asChild variant="ghost" size="icon" className="h-8 w-8 rounded-full">
          <Link to={`/organizations/${id}`}>
            <ArrowLeft className="h-4 w-4" />
          </Link>
        </Button>
        <div>
          <h2 className="text-2xl font-bold tracking-tight">{workspace.name}</h2>
          {workspace.description && <p className="text-muted-foreground mt-1">{workspace.description}</p>}
        </div>
      </div>

      <Tabs defaultValue="overview" className="w-full">
        <TabsList className="grid w-full grid-cols-4 lg:w-[500px]">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="documents">Documents</TabsTrigger>
          <TabsTrigger value="chat">Chat</TabsTrigger>
          <TabsTrigger value="settings">Settings</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4 mt-6">
          <Card>
            <CardHeader>
              <CardTitle>Workspace Overview</CardTitle>
              <CardDescription>General information about this workspace.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-1">
                  <p className="text-sm font-medium leading-none">Workspace ID</p>
                  <p className="text-sm text-muted-foreground">{workspace.id}</p>
                </div>
                <div className="space-y-1">
                  <p className="text-sm font-medium leading-none">Organization ID</p>
                  <p className="text-sm text-muted-foreground">{workspace.organization_id}</p>
                </div>
                <div className="space-y-1">
                  <p className="text-sm font-medium leading-none">Created At</p>
                  <p className="text-sm text-muted-foreground">{new Date(workspace.created_at).toLocaleString()}</p>
                </div>
                <div className="space-y-1">
                  <p className="text-sm font-medium leading-none">Status</p>
                  <p className="text-sm text-muted-foreground">Active</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="documents" className="mt-6">
          <DocumentsList />
        </TabsContent>

        <TabsContent value="chat" className="mt-6">
          <Card>
            <CardHeader>
              <CardTitle>Chat</CardTitle>
              <CardDescription>Interact with your workspace knowledge base.</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex h-48 flex-col items-center justify-center border rounded-lg border-dashed text-sm text-muted-foreground">
                <MessageSquare className="mb-2 h-8 w-8 text-muted-foreground/50" />
                <p>Chat interface coming soon...</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="settings" className="mt-6">
          <Card>
            <CardHeader>
              <CardTitle>Settings</CardTitle>
              <CardDescription>Configure your workspace settings.</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex h-48 flex-col items-center justify-center border rounded-lg border-dashed text-sm text-muted-foreground">
                <Settings className="mb-2 h-8 w-8 text-muted-foreground/50" />
                <p>Workspace settings coming soon...</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
