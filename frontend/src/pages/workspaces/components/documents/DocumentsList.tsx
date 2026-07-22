import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { useParams } from "react-router-dom"
import { FileText, MoreHorizontal, Trash, FileIcon, Loader2 } from "lucide-react"
import { toast } from "sonner"

import { Button } from "@/components/ui/button"
import { Skeleton } from "@/components/ui/skeleton"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { documentsService, type Document } from "@/api/documents.service"
import { UploadDialog } from "./UploadDialog"

export function DocumentsList() {
  const { id, workspaceId } = useParams<{ id: string; workspaceId: string }>()
  const queryClient = useQueryClient()

  const { data: documents, isLoading } = useQuery({
    queryKey: ["documents", id, workspaceId],
    queryFn: () => documentsService.getDocuments(id!, workspaceId!),
    enabled: !!id && !!workspaceId,
  })

  const deleteMutation = useMutation({
    mutationFn: (documentId: string) => documentsService.deleteDocument(id!, workspaceId!, documentId),
    onSuccess: () => {
      toast.success("Document deleted")
      queryClient.invalidateQueries({ queryKey: ["documents", id, workspaceId] })
    },
    onError: () => {
      toast.error("Failed to delete document")
    }
  })

  const getStatusBadge = (status: Document["status"]) => {
    switch (status) {
      case "UPLOADING":
        return <span className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold bg-secondary text-secondary-foreground"><Loader2 className="mr-1 h-3 w-3 animate-spin"/> Uploading</span>
      case "PROCESSING":
        return <span className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold bg-blue-100 text-blue-800"><Loader2 className="mr-1 h-3 w-3 animate-spin"/> Processing</span>
      case "READY":
        return <span className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold bg-green-100 text-green-800">Ready</span>
      case "FAILED":
        return <span className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold bg-red-100 text-red-800">Failed</span>
      default:
        return <span className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold">{status}</span>
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-lg font-medium">Documents</h3>
          <p className="text-sm text-muted-foreground">Manage files uploaded to this workspace.</p>
        </div>
        <UploadDialog />
      </div>

      <div className="border rounded-md">
        {isLoading ? (
          <div className="p-8 space-y-4">
            <Skeleton className="h-10 w-full" />
            <Skeleton className="h-10 w-full" />
            <Skeleton className="h-10 w-full" />
          </div>
        ) : documents?.length === 0 ? (
          <div className="flex h-[300px] flex-col items-center justify-center text-sm text-muted-foreground">
            <FileText className="mb-2 h-8 w-8 text-muted-foreground/50" />
            <p>No documents found</p>
            <p className="text-xs">Upload your first document to get started</p>
          </div>
        ) : (
          <div className="relative w-full overflow-auto">
            <table className="w-full caption-bottom text-sm">
              <thead className="[&_tr]:border-b">
                <tr className="border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted">
                  <th className="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Name</th>
                  <th className="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Status</th>
                  <th className="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Size</th>
                  <th className="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Uploaded</th>
                  <th className="h-12 px-4 align-middle"></th>
                </tr>
              </thead>
              <tbody className="[&_tr:last-child]:border-0">
                {documents?.map((doc) => (
                  <tr key={doc.id} className="border-b transition-colors hover:bg-muted/50">
                    <td className="p-4 align-middle">
                      <div className="flex items-center gap-2 font-medium">
                        <FileIcon className="h-4 w-4 text-muted-foreground" />
                        {doc.name}
                      </div>
                    </td>
                    <td className="p-4 align-middle">
                      {getStatusBadge(doc.status)}
                    </td>
                    <td className="p-4 align-middle text-muted-foreground">
                      {doc.metadata_info?.size ? `${(doc.metadata_info.size / 1024 / 1024).toFixed(2)} MB` : "-"}
                    </td>
                    <td className="p-4 align-middle text-muted-foreground">
                      {new Date(doc.created_at).toLocaleDateString()}
                    </td>
                    <td className="p-4 align-middle text-right">
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button variant="ghost" className="h-8 w-8 p-0">
                            <span className="sr-only">Open menu</span>
                            <MoreHorizontal className="h-4 w-4" />
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                          <DropdownMenuItem
                            className="text-red-600 focus:text-red-600 cursor-pointer"
                            onClick={() => deleteMutation.mutate(doc.id)}
                            disabled={deleteMutation.isPending}
                          >
                            <Trash className="mr-2 h-4 w-4" />
                            Delete
                          </DropdownMenuItem>
                        </DropdownMenuContent>
                      </DropdownMenu>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}
