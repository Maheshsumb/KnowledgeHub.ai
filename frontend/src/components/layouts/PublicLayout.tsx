import { Outlet } from "react-router-dom"

export function PublicLayout() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-muted/30">
      <div className="w-full max-w-md px-4">
        <div className="mb-8 flex justify-center">
          <div className="flex items-center gap-2 font-bold text-xl tracking-tight">
            <div className="h-6 w-6 rounded-md bg-primary flex items-center justify-center text-primary-foreground text-xs">
              K
            </div>
            KnowledgeHub AI
          </div>
        </div>
        <Outlet />
      </div>
    </div>
  )
}
