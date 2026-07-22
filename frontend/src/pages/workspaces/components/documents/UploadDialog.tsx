import { useState, useCallback } from "react"
import { useDropzone } from "react-dropzone"
import { Upload, X, File, Loader2 } from "lucide-react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useParams } from "react-router-dom"
import { toast } from "sonner"

import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { documentsService } from "@/api/documents.service"

export function UploadDialog() {
  const { id, workspaceId } = useParams<{ id: string; workspaceId: string }>()
  const [open, setOpen] = useState(false)
  const [file, setFile] = useState<File | null>(null)
  const queryClient = useQueryClient()

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0])
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    maxFiles: 1,
    multiple: false,
  })

  const uploadMutation = useMutation({
    mutationFn: (uploadFile: File) => documentsService.uploadDocument(id!, workspaceId!, uploadFile),
    onSuccess: () => {
      toast.success("Document uploaded successfully")
      queryClient.invalidateQueries({ queryKey: ["documents", id, workspaceId] })
      setOpen(false)
      setFile(null)
    },
    onError: (error) => {
      toast.error("Failed to upload document")
      console.error("Upload error:", error)
    },
  })

  const handleUpload = () => {
    if (file) {
      uploadMutation.mutate(file)
    }
  }

  const handleOpenChange = (newOpen: boolean) => {
    if (uploadMutation.isPending) return // Prevent closing while uploading
    setOpen(newOpen)
    if (!newOpen) {
      setFile(null)
    }
  }

  return (
    <Dialog open={open} onOpenChange={handleOpenChange}>
      <DialogTrigger asChild>
        <Button>
          <Upload className="mr-2 h-4 w-4" />
          Upload Document
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Upload Document</DialogTitle>
          <DialogDescription>
            Drag and drop a file here, or click to select a file.
          </DialogDescription>
        </DialogHeader>

        {!file ? (
          <div
            {...getRootProps()}
            className={`mt-4 border-2 border-dashed rounded-lg p-10 text-center cursor-pointer transition-colors ${
              isDragActive ? "border-primary bg-primary/5" : "border-muted-foreground/25 hover:border-primary/50"
            }`}
          >
            <input {...getInputProps()} />
            <Upload className="mx-auto h-8 w-8 text-muted-foreground mb-4" />
            {isDragActive ? (
              <p className="text-sm font-medium">Drop the file here ...</p>
            ) : (
              <div className="space-y-1">
                <p className="text-sm font-medium">Drag & drop a file here</p>
                <p className="text-xs text-muted-foreground">or click to browse from your computer</p>
              </div>
            )}
          </div>
        ) : (
          <div className="mt-4 p-4 border rounded-lg flex items-center justify-between">
            <div className="flex items-center gap-3 overflow-hidden">
              <div className="p-2 bg-primary/10 rounded">
                <File className="h-4 w-4 text-primary" />
              </div>
              <div className="truncate">
                <p className="text-sm font-medium truncate">{file.name}</p>
                <p className="text-xs text-muted-foreground">
                  {(file.size / 1024 / 1024).toFixed(2)} MB
                </p>
              </div>
            </div>
            {!uploadMutation.isPending && (
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setFile(null)}
                className="shrink-0"
              >
                <X className="h-4 w-4" />
              </Button>
            )}
          </div>
        )}

        <div className="mt-4 flex justify-end gap-2">
          <Button variant="outline" onClick={() => handleOpenChange(false)} disabled={uploadMutation.isPending}>
            Cancel
          </Button>
          <Button onClick={handleUpload} disabled={!file || uploadMutation.isPending}>
            {uploadMutation.isPending && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
            {uploadMutation.isPending ? "Uploading..." : "Upload"}
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  )
}
