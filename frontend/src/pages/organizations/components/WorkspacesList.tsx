import { useState } from "react"
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { FolderGit2, Plus, Trash2, Edit } from "lucide-react"
import { useNavigate } from "react-router-dom"
import { toast } from "sonner"
import { z } from "zod"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Skeleton } from "@/components/ui/skeleton"
import { EmptyState } from "@/components/ui/empty-state"
import { ConfirmDialog } from "@/components/ui/confirm-dialog"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"

import { workspacesService } from "@/api/workspaces.service"
import type { Workspace } from "@/api/workspaces.service"
import { useRole } from "@/hooks/useRole"
import { membershipService } from "@/api/membership.service"

const workspaceSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters"),
  description: z.string().optional(),
})

interface WorkspacesListProps {
  organizationId: string
}

export function WorkspacesList({ organizationId }: WorkspacesListProps) {
  const [createOpen, setCreateOpen] = useState(false)
  const [updateOpen, setUpdateOpen] = useState(false)
  const [deleteOpen, setDeleteOpen] = useState(false)
  const [selectedWorkspace, setSelectedWorkspace] = useState<Workspace | null>(null)

  const queryClient = useQueryClient()
  const navigate = useNavigate()

  const { data: members } = useQuery({
    queryKey: ["members", organizationId],
    queryFn: () => membershipService.getMembers(organizationId),
  })
  const { canManageMembers } = useRole(members || []) // Using this as proxy for admin rights for now

  const { data: workspaces, isLoading } = useQuery({
    queryKey: ["workspaces", organizationId],
    queryFn: () => workspacesService.getWorkspaces(organizationId),
  })

  const form = useForm({
    resolver: zodResolver(workspaceSchema),
    defaultValues: { name: "", description: "" },
  })

  const updateForm = useForm({
    resolver: zodResolver(workspaceSchema),
    defaultValues: { name: "", description: "" },
  })

  const createMutation = useMutation({
    mutationFn: (values: { name: string; description?: string }) =>
      workspacesService.createWorkspace(organizationId, values),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["workspaces", organizationId] })
      toast.success("Workspace created successfully")
      setCreateOpen(false)
      form.reset()
    },
    onError: () => toast.error("Failed to create workspace"),
  })

  const updateMutation = useMutation({
    mutationFn: (values: { id: string; name: string; description?: string }) =>
      workspacesService.updateWorkspace(organizationId, values.id, {
        name: values.name,
        description: values.description,
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["workspaces", organizationId] })
      toast.success("Workspace updated successfully")
      setUpdateOpen(false)
    },
    onError: () => toast.error("Failed to update workspace"),
  })

  const deleteMutation = useMutation({
    mutationFn: (id: string) => workspacesService.deleteWorkspace(organizationId, id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["workspaces", organizationId] })
      toast.success("Workspace deleted successfully")
      setDeleteOpen(false)
    },
    onError: () => toast.error("Failed to delete workspace"),
  })

  const handleCreate = (values: { name: string; description?: string }) => {
    createMutation.mutate(values)
  }

  const handleUpdate = (values: { name: string; description?: string }) => {
    if (selectedWorkspace) {
      updateMutation.mutate({ id: selectedWorkspace.id, ...values })
    }
  }

  const handleDelete = () => {
    if (selectedWorkspace) {
      deleteMutation.mutate(selectedWorkspace.id)
    }
  }

  const openUpdate = (workspace: Workspace) => {
    setSelectedWorkspace(workspace)
    updateForm.reset({ name: workspace.name, description: workspace.description || "" })
    setUpdateOpen(true)
  }

  const openDelete = (workspace: Workspace) => {
    setSelectedWorkspace(workspace)
    setDeleteOpen(true)
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-medium">Workspaces</h3>
        {canManageMembers && (
          <Button onClick={() => setCreateOpen(true)} size="sm">
            <Plus className="mr-2 h-4 w-4" />
            New Workspace
          </Button>
        )}
      </div>

      <div className="border rounded-lg">
        <table className="w-full text-sm text-left">
          <thead className="bg-muted/50 text-muted-foreground">
            <tr>
              <th className="px-4 py-3 font-medium">Name</th>
              <th className="px-4 py-3 font-medium">Description</th>
              <th className="px-4 py-3 font-medium text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {isLoading ? (
              Array.from({ length: 3 }).map((_, i) => (
                <tr key={i}>
                  <td className="px-4 py-4"><Skeleton className="h-4 w-48" /></td>
                  <td className="px-4 py-4"><Skeleton className="h-4 w-64" /></td>
                  <td className="px-4 py-4 text-right">
                    <div className="flex justify-end gap-2">
                      <Skeleton className="h-8 w-16" />
                      <Skeleton className="h-8 w-8" />
                      <Skeleton className="h-8 w-8" />
                    </div>
                  </td>
                </tr>
              ))
            ) : workspaces?.length === 0 ? (
              <tr>
                <td colSpan={3} className="px-4 py-8">
                  <EmptyState
                    icon={FolderGit2}
                    title="No workspaces found"
                    description="You don't have any workspaces in this organization yet."
                    className="border-0"
                  />
                </td>
              </tr>
            ) : (
              workspaces?.map((workspace) => (
                <tr key={workspace.id} className="hover:bg-muted/50 transition-colors">
                  <td className="px-4 py-3 font-medium">{workspace.name}</td>
                  <td className="px-4 py-3 text-muted-foreground">{workspace.description || "—"}</td>
                  <td className="px-4 py-3 text-right">
                    <div className="flex justify-end gap-2">
                      <Button 
                        variant="outline" 
                        size="sm" 
                        onClick={() => navigate(`/organizations/${organizationId}/workspaces/${workspace.id}`)}
                      >
                        View
                      </Button>
                      {canManageMembers && (
                        <>
                          <Button variant="ghost" size="icon" className="h-8 w-8" onClick={() => openUpdate(workspace)}>
                            <Edit className="h-4 w-4" />
                          </Button>
                          <Button 
                            variant="ghost" 
                            size="icon" 
                            className="h-8 w-8 text-destructive hover:bg-destructive/10 hover:text-destructive" 
                            onClick={() => openDelete(workspace)}
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </>
                      )}
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Create Dialog */}
      <Dialog open={createOpen} onOpenChange={setCreateOpen}>
        <DialogContent>
          <form onSubmit={form.handleSubmit(handleCreate)}>
            <DialogHeader>
              <DialogTitle>Create Workspace</DialogTitle>
              <DialogDescription>Enter the details for the new workspace.</DialogDescription>
            </DialogHeader>
            <div className="grid gap-4 py-4">
              <div className="grid gap-2">
                <label htmlFor="name" className="text-sm font-medium">Name</label>
                <Input id="name" {...form.register("name")} placeholder="Engineering" />
              </div>
              <div className="grid gap-2">
                <label htmlFor="description" className="text-sm font-medium">Description (Optional)</label>
                <Input id="description" {...form.register("description")} placeholder="Workspace for engineering team" />
              </div>
            </div>
            <DialogFooter>
              <Button type="button" variant="outline" onClick={() => setCreateOpen(false)}>Cancel</Button>
              <Button type="submit" disabled={createMutation.isPending}>Create</Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>

      {/* Update Dialog */}
      <Dialog open={updateOpen} onOpenChange={setUpdateOpen}>
        <DialogContent>
          <form onSubmit={updateForm.handleSubmit(handleUpdate)}>
            <DialogHeader>
              <DialogTitle>Edit Workspace</DialogTitle>
              <DialogDescription>Update the details of the workspace.</DialogDescription>
            </DialogHeader>
            <div className="grid gap-4 py-4">
              <div className="grid gap-2">
                <label htmlFor="update-name" className="text-sm font-medium">Name</label>
                <Input id="update-name" {...updateForm.register("name")} />
              </div>
              <div className="grid gap-2">
                <label htmlFor="update-description" className="text-sm font-medium">Description (Optional)</label>
                <Input id="update-description" {...updateForm.register("description")} />
              </div>
            </div>
            <DialogFooter>
              <Button type="button" variant="outline" onClick={() => setUpdateOpen(false)}>Cancel</Button>
              <Button type="submit" disabled={updateMutation.isPending}>Save</Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>

      {/* Delete Confirm */}
      <ConfirmDialog
        open={deleteOpen}
        onOpenChange={setDeleteOpen}
        title="Delete Workspace"
        description="Are you sure you want to delete this workspace? This action cannot be undone."
        confirmText="Delete"
        destructive
        onConfirm={handleDelete}
      />
    </div>
  )
}
