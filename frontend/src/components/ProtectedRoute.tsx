import { Navigate } from "react-router"

interface ProtectedRouteProps {
  children: React.ReactNode
  requiredRole?: string
}

export default function ProtectedRoute({ children, requiredRole }: ProtectedRouteProps) {
  const token = localStorage.getItem("token")
  const role = localStorage.getItem("role")

  if (!token || !role) {
    return <Navigate to="/login" replace />
  }

  if (requiredRole && role !== requiredRole) {
    const redirectMap: Record<string, string> = {
      donor: "/donor",
      hospital: "/hospital",
      admin: "/admin"
    }
    return <Navigate to={redirectMap[role] || "/"} replace />
  }

  return <>{children}</>
}
