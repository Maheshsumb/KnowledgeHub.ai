import { useState } from "react"
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { Building2, Plus, Search, Trash2, Edit } from "lucide-react"
import { Link, useNavigate } from "react-router-dom"
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

import { organizationsService } from "@/api/organizations.service"
import type { Organization } from "@/api/organizations.service"

const organizationSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters"),
})

export function OrganizationsPage() {
  const [search, setSearch] = useState("")
  const [page, setPage] = useState(1)
  const [createOpen, setCreateOpen] = useState(false)
  const [updateOpen, setUpdateOpen] = useState(false)
  const [deleteOpen, setDeleteOpen] = useState(false)
  const [selectedOrg, setSelectedOrg] = useState<Organization | null>(null)

  const queryClient = useQueryClient()
  const navigate = useNavigate()

  const { data, isLoading } = useQuery({
    queryKey: ["organizations", page, search],
    queryFn: () => organizationsService.getOrganizations(page, 10, search),
  })

  const form = useForm({
    resolver: zodResolver(organizationSchema),
    defaultValues: { name: "" },
  })

  const updateForm = useForm({
    resolver: zodResolver(organizationSchema),
    defaultValues: { name: "" },
  })

  const createMutation = useMutation({
    mutationFn: organizationsService.createOrganization,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["organizations"] })
      toast.success("Organization created successfully")
      setCreateOpen(false)
      form.reset()
    },
    onError: () => toast.error("Failed to create organization"),
  })

  const updateMutation = useMutation({
    mutationFn: (vars: { id: string; name: string }) =>
      organizationsService.updateOrganization(vars.id, { name: vars.name }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["organizations"] })
      toast.success("Organization updated successfully")
      setUpdateOpen(false)
    },
    onError: () => toast.error("Failed to update organization"),
  })

  const deleteMutation = useMutation({
    mutationFn: organizationsService.deleteOrganization,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["organizations"] })
      toast.success("Organization deleted successfully")
      setDeleteOpen(false)
    },
    onError: () => toast.error("Failed to delete organization"),
  })

  const handleCreate = (values: { name: string }) => {
    createMutation.mutate(values)
  }

  const handleUpdate = (values: { name: string }) => {
    if (selectedOrg) updateMutation.mutate({ id: selectedOrg.id, name: values.name })
  }

  const handleDelete = () => {
    if (selectedOrg) deleteMutation.mutate(selectedOrg.id)
  }

  const openUpdate = (org: Organization) => {
    setSelectedOrg(org)
    updateForm.reset({ name: org.name })
    setUpdateOpen(true)
  }

  const openDelete = (org: Organization) => {
    setSelectedOrg(org)
    setDeleteOpen(true)
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Organizations</h2>
          <p className="text-muted-foreground">Manage your organizations and their settings.</p>
        </div>
        <Button onClick={() => setCreateOpen(true)}>
          <Plus className="mr-2 h-4 w-4" />
          New Organization
        </Button>
      </div>

      <div className="flex items-center gap-2 max-w-sm">
        <Search className="h-4 w-4 text-muted-foreground absolute ml-3" />
        <Input
          placeholder="Search organizations..."
          className="pl-9"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      <div className="border rounded-lg">
        <table className="w-full text-sm text-left">
          <thead className="bg-muted/50 text-muted-foreground">
            <tr>
              <th className="px-4 py-3 font-medium">Name</th>
              <th className="px-4 py-3 font-medium text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {isLoading ? (
              Array.from({ length: 5 }).map((_, i) => (
                <tr key={i}>
                  <td className="px-4 py-4"><Skeleton className="h-4 w-48" /></td>
                  <td className="px-4 py-4 text-right">
                    <div className="flex justify-end gap-2">
                      <Skeleton className="h-8 w-16" />
                      <Skeleton className="h-8 w-8" />
                      <Skeleton className="h-8 w-8" />
                    </div>
                  </td>
                </tr>
              ))
            ) : data?.items?.length === 0 ? (
              <tr>
                <td colSpan={2} className="px-4 py-8">
                  <EmptyState
                    icon={Building2}
                    title="No organizations found"
                    description="You don't have any organizations yet. Create one to get started."
                    className="border-0 min-h-[300px]"
                  />
                </td>
              </tr>
            ) : (
              data?.items?.map((org) => (
                <tr key={org.id} className="hover:bg-muted/50 transition-colors">
                  <td className="px-4 py-3 font-medium">
                    <Link to={`/organizations/${org.id}`} className="hover:underline">
                      {org.name}
                    </Link>
                  </td>
                  <td className="px-4 py-3 text-right">
                    <div className="flex justify-end gap-2">
                      <Button variant="outline" size="sm" onClick={() => navigate(`/organizations/${org.id}`)}>
                        View
                      </Button>
                      <Button variant="ghost" size="icon" className="h-8 w-8" onClick={() => openUpdate(org)}>
                        <Edit className="h-4 w-4" />
                      </Button>
                      <Button variant="ghost" size="icon" className="h-8 w-8 text-destructive hover:bg-destructive/10 hover:text-destructive" onClick={() => openDelete(org)}>
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination Controls */}
      {data && data.pages > 1 && (
        <div className="flex items-center justify-end space-x-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setPage((p) => Math.max(1, p - 1))}
            disabled={page === 1}
          >
            Previous
          </Button>
          <div className="text-sm font-medium">
            Page {page} of {data.pages}
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={() => setPage((p) => Math.min(data.pages, p + 1))}
            disabled={page === data.pages}
          >
            Next
          </Button>
        </div>
      )}

      {/* Create Dialog */}
      <Dialog open={createOpen} onOpenChange={setCreateOpen}>
        <DialogContent>
          <form onSubmit={form.handleSubmit(handleCreate)}>
            <DialogHeader>
              <DialogTitle>Create Organization</DialogTitle>
              <DialogDescription>Enter the details for your new organization.</DialogDescription>
            </DialogHeader>
            <div className="grid gap-4 py-4">
              <div className="grid gap-2">
                <label htmlFor="name" className="text-sm font-medium">Name</label>
                <Input id="name" {...form.register("name")} placeholder="Acme Corp" />
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
              <DialogTitle>Edit Organization</DialogTitle>
              <DialogDescription>Update the name of the organization.</DialogDescription>
            </DialogHeader>
            <div className="grid gap-4 py-4">
              <div className="grid gap-2">
                <label htmlFor="update-name" className="text-sm font-medium">Name</label>
                <Input id="update-name" {...updateForm.register("name")} />
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
        title="Delete Organization"
        description="Are you sure you want to delete this organization? This action cannot be undone."
        confirmText="Delete"
        destructive
        onConfirm={handleDelete}
      />
    </div>
  )
}
