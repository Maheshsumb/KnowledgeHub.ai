import { useState } from "react"
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { UserPlus, MoreHorizontal, Trash2 } from "lucide-react"
import { toast } from "sonner"
import { z } from "zod"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Skeleton } from "@/components/ui/skeleton"
import { Badge } from "@/components/ui/badge"
import { ConfirmDialog } from "@/components/ui/confirm-dialog"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  DropdownMenuSeparator,
} from "@/components/ui/dropdown-menu"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"

import { membershipService } from "@/api/membership.service"
import type { Role, Membership } from "@/api/membership.service"
import { useRole } from "@/hooks/useRole"

const inviteSchema = z.object({
  user_id: z.string().uuid("Must be a valid user UUID"),
  role: z.enum(["OWNER", "ADMIN", "MEMBER", "VIEWER"]),
})

export function MembersList({ organizationId }: { organizationId: string }) {
  const [inviteOpen, setInviteOpen] = useState(false)
  const [removeOpen, setRemoveOpen] = useState(false)
  const [selectedMember, setSelectedMember] = useState<Membership | null>(null)

  const queryClient = useQueryClient()

  const { data: members, isLoading } = useQuery({
    queryKey: ["organizations", organizationId, "members"],
    queryFn: () => membershipService.getMembers(organizationId),
  })

  const { canManageMembers, canUpdateRole, currentRole } = useRole(members)

  const form = useForm({
    resolver: zodResolver(inviteSchema),
    defaultValues: { user_id: "", role: "MEMBER" as Role },
  })

  const inviteMutation = useMutation({
    mutationFn: (vars: { user_id: string; role: Role }) =>
      membershipService.addMember(organizationId, vars),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["organizations", organizationId, "members"] })
      toast.success("Member invited successfully")
      setInviteOpen(false)
      form.reset()
    },
    onError: () => toast.error("Failed to invite member"),
  })

  const updateRoleMutation = useMutation({
    mutationFn: (vars: { userId: string; role: Role }) =>
      membershipService.updateRole(organizationId, vars.userId, vars.role),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["organizations", organizationId, "members"] })
      toast.success("Role updated successfully")
    },
    onError: () => toast.error("Failed to update role"),
  })

  const removeMutation = useMutation({
    mutationFn: (userId: string) => membershipService.removeMember(organizationId, userId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["organizations", organizationId, "members"] })
      toast.success("Member removed successfully")
      setRemoveOpen(false)
    },
    onError: () => toast.error("Failed to remove member"),
  })

  const handleInvite = (values: { user_id: string; role: Role }) => {
    inviteMutation.mutate(values)
  }

  const handleRemove = () => {
    if (selectedMember) {
      removeMutation.mutate(selectedMember.user_id)
    }
  }

  const roleColors: Record<Role, "default" | "secondary" | "destructive" | "outline"> = {
    OWNER: "default",
    ADMIN: "secondary",
    MEMBER: "outline",
    VIEWER: "outline",
  }

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-lg font-medium">Members</h3>
          <p className="text-sm text-muted-foreground">
            Manage who has access to this organization.
          </p>
        </div>
        {canManageMembers && (
          <Button onClick={() => setInviteOpen(true)}>
            <UserPlus className="mr-2 h-4 w-4" />
            Invite Member
          </Button>
        )}
      </div>

      <div className="border rounded-lg">
        <table className="w-full text-sm text-left">
          <thead className="bg-muted/50 text-muted-foreground">
            <tr>
              <th className="px-4 py-3 font-medium">User</th>
              <th className="px-4 py-3 font-medium">Role</th>
              <th className="px-4 py-3 font-medium text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {isLoading ? (
              Array.from({ length: 3 }).map((_, i) => (
                <tr key={i}>
                  <td className="px-4 py-4"><Skeleton className="h-4 w-48" /></td>
                  <td className="px-4 py-4"><Skeleton className="h-5 w-16 rounded-full" /></td>
                  <td className="px-4 py-4 text-right"><Skeleton className="h-8 w-8 ml-auto" /></td>
                </tr>
              ))
            ) : members?.length === 0 ? (
              <tr>
                <td colSpan={3} className="px-4 py-8 text-center text-muted-foreground">
                  No members found.
                </td>
              </tr>
            ) : (
              members?.map((member) => (
                <tr key={member.id} className="hover:bg-muted/50 transition-colors">
                  <td className="px-4 py-3 font-medium text-sm">
                    {member.user ? (
                      <div>
                        <div>{member.user.full_name}</div>
                        <div className="text-xs text-muted-foreground font-normal">{member.user.email}</div>
                      </div>
                    ) : (
                      <span className="font-mono text-xs">{member.user_id}</span>
                    )}
                  </td>
                  <td className="px-4 py-3">
                    <Badge variant={roleColors[member.role]}>{member.role}</Badge>
                  </td>
                  <td className="px-4 py-3 text-right">
                    {canManageMembers && member.role !== "OWNER" && (
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button variant="ghost" className="h-8 w-8 p-0">
                            <MoreHorizontal className="h-4 w-4" />
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                          {/* Role Change */}
                          {canUpdateRole(member.role) && (
                            <>
                              <div className="px-2 py-1.5 text-xs font-semibold text-muted-foreground">
                                Change Role
                              </div>
                              {(["OWNER", "ADMIN", "MEMBER", "VIEWER"] as Role[]).map((role) => (
                                <DropdownMenuItem
                                  key={role}
                                  onClick={() => updateRoleMutation.mutate({ userId: member.user_id, role })}
                                  disabled={member.role === role || !canUpdateRole(role)}
                                >
                                  {role}
                                </DropdownMenuItem>
                              ))}
                              <DropdownMenuSeparator />
                            </>
                          )}
                          
                          {/* Remove Member */}
                          {canUpdateRole(member.role) && (
                            <DropdownMenuItem
                              className="text-destructive focus:bg-destructive/10"
                              onClick={() => {
                                setSelectedMember(member)
                                setRemoveOpen(true)
                              }}
                            >
                              <Trash2 className="mr-2 h-4 w-4" /> Remove
                            </DropdownMenuItem>
                          )}
                        </DropdownMenuContent>
                      </DropdownMenu>
                    )}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Invite Dialog */}
      <Dialog open={inviteOpen} onOpenChange={setInviteOpen}>
        <DialogContent>
          <form onSubmit={form.handleSubmit(handleInvite)}>
            <DialogHeader>
              <DialogTitle>Invite Member</DialogTitle>
              <DialogDescription>Add a new member to the organization using their User ID.</DialogDescription>
            </DialogHeader>
            <div className="grid gap-4 py-4">
              <div className="grid gap-2">
                <label htmlFor="user_id" className="text-sm font-medium">User ID (UUID)</label>
                <Input id="user_id" {...form.register("user_id")} placeholder="123e4567-e89b-12d3-a456-426614174000" />
                {form.formState.errors.user_id && (
                  <p className="text-xs text-destructive">{form.formState.errors.user_id.message}</p>
                )}
              </div>
              <div className="grid gap-2">
                <label htmlFor="role" className="text-sm font-medium">Role</label>
                <select
                  {...form.register("role")}
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  <option value="MEMBER">Member</option>
                  <option value="VIEWER">Viewer</option>
                  {currentRole === "OWNER" && <option value="ADMIN">Admin</option>}
                </select>
              </div>
            </div>
            <DialogFooter>
              <Button type="button" variant="outline" onClick={() => setInviteOpen(false)}>Cancel</Button>
              <Button type="submit" disabled={inviteMutation.isPending}>Invite</Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>

      {/* Remove Confirm */}
      <ConfirmDialog
        open={removeOpen}
        onOpenChange={setRemoveOpen}
        title="Remove Member"
        description="Are you sure you want to remove this member? They will lose access to the organization immediately."
        confirmText="Remove"
        destructive
        onConfirm={handleRemove}
      />
    </div>
  )
}
