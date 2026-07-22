import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

export function SettingsPage() {
  return (
    <div className="space-y-6 max-w-2xl">
      <div>
        <h2 className="text-2xl font-bold tracking-tight">Settings</h2>
        <p className="text-muted-foreground">
          Manage your account settings and preferences.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Profile</CardTitle>
          <CardDescription>
            Update your personal information.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid gap-2">
            <label className="text-sm font-medium leading-none">Full Name</label>
            <Input defaultValue="John Doe" />
          </div>
          <div className="grid gap-2">
            <label className="text-sm font-medium leading-none">Email</label>
            <Input defaultValue="m@example.com" disabled />
          </div>
          <Button>Save changes</Button>
        </CardContent>
      </Card>
    </div>
  )
}
