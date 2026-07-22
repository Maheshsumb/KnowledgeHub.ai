import { useParams } from "react-router-dom"
import { useQuery } from "@tanstack/react-query"


import { Skeleton } from "@/components/ui/skeleton"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { organizationsService } from "@/api/organizations.service"
import { MembersList } from "./components/MembersList"

import { WorkspacesList } from "./components/WorkspacesList"

export function OrganizationDetailsPage() {
  const { id } = useParams<{ id: string }>()

  const { data: org, isLoading } = useQuery({
    queryKey: ["organizations", id],
    queryFn: () => organizationsService.getOrganization(id!),
    enabled: !!id,
  })

  if (isLoading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-10 w-1/3" />
        <Skeleton className="h-[400px] w-full" />
      </div>
    )
  }

  if (!org) {
    return (
      <div className="flex h-[400px] flex-col items-center justify-center text-center">
        <h3 className="text-lg font-semibold">Organization not found</h3>
        <p className="text-muted-foreground">The organization you are looking for does not exist.</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">{org.name}</h2>
          {org.description && <p className="text-muted-foreground mt-1">{org.description}</p>}
        </div>
      </div>

      <Tabs defaultValue="overview" className="w-full">
        <TabsList className="grid w-full grid-cols-3 lg:w-[400px]">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="members">Members</TabsTrigger>
          <TabsTrigger value="workspaces">Workspaces</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4 mt-6">
          <Card>
            <CardHeader>
              <CardTitle>Organization Overview</CardTitle>
              <CardDescription>General information about this organization.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-1">
                  <p className="text-sm font-medium leading-none">Organization ID</p>
                  <p className="text-sm text-muted-foreground">{org.id}</p>
                </div>
                <div className="space-y-1">
                  <p className="text-sm font-medium leading-none">Name</p>
                  <p className="text-sm text-muted-foreground">{org.name}</p>
                </div>
                <div className="space-y-1">
                  <p className="text-sm font-medium leading-none">Status</p>
                  <p className="text-sm text-muted-foreground">Active</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="members" className="mt-6">
          <MembersList organizationId={org.id} />
        </TabsContent>

        <TabsContent value="workspaces" className="mt-6">
          <WorkspacesList organizationId={org.id} />
        </TabsContent>
      </Tabs>
    </div>
  )
}
