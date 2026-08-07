import { useState } from "react"
import { motion } from "framer-motion"
import { Link, useNavigate } from "react-router"
import { Button } from "@/components/ui/button"
import { ModeToggle } from "@/components/mode-toggle"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { HeartPulse, Eye, EyeOff } from "lucide-react"

export default function Login() {
  const [loading, setLoading] = useState(false)
  const [email, setEmail] = useState("")
  const [showPassword, setShowPassword] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setLoading(true)

    try {
      const formData = new FormData(e.currentTarget)
      const currentEmail = formData.get("email") as string
      const password = formData.get("password") as string
      setEmail(currentEmail)

      const API_URL = import.meta.env.VITE_API_URL || ""
      const res = await fetch(`${API_URL}/api/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: currentEmail, password })
      })
      const data = await res.json()

      if (!res.ok) {
        if (data.msg && data.msg.toLowerCase().includes("verify your email")) {
          navigate(`/verify-otp?email=${encodeURIComponent(currentEmail)}`)
        } else {
          alert(data.msg || "Login failed. Please try again.")
        }
      } else {
        localStorage.setItem("token", data.access_token)
        localStorage.setItem("role", data.user.role)

        if (data.user.role === "donor") navigate("/donor")
        else if (data.user.role === "hospital") navigate("/hospital")
        else navigate("/admin")
      }
    } catch {
      alert("Cannot connect to server. Please try again later.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4 bg-background relative">
      <div className="absolute top-4 sm:top-8 left-4 sm:left-8">
        <Link to="/">
          <Button variant="ghost" className="text-muted-foreground">&larr; Back to Home</Button>
        </Link>
      </div>
      <div className="absolute top-4 sm:top-8 right-4 sm:right-8">
        <ModeToggle />
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-md glass p-6 sm:p-10 rounded-3xl"
      >
        <div className="flex justify-center mb-6">
          <Link to="/" className="flex items-center gap-2">
            <HeartPulse className="h-8 w-8 text-primary" />
            <span className="text-2xl font-bold tracking-tight">BloodLink</span>
          </Link>
        </div>

        <h2 className="text-2xl font-bold mb-2 text-center">Welcome Back</h2>
        <p className="text-muted-foreground text-center mb-8">Sign in to your account</p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input id="email" name="email" type="email" defaultValue={email} required placeholder="you@example.com" />
          </div>

          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <div className="relative">
              <Input
                id="password"
                name="password"
                type={showPassword ? "text" : "password"}
                required
                placeholder="Enter your password"
                className="pr-10"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
                tabIndex={-1}
                aria-label={showPassword ? "Hide password" : "Show password"}
              >
                {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
              </button>
            </div>
          </div>

          <Button type="submit" className="w-full h-12 text-md mt-6" disabled={loading}>
            {loading ? "Please wait..." : "Login"}
          </Button>
        </form>

        <div className="mt-6 text-center text-sm text-muted-foreground">
          Don&apos;t have an account?{" "}
          <div className="flex justify-center gap-4 mt-2">
            <Link to="/register/donor" className="text-primary font-semibold hover:underline">
              Donor Sign Up
            </Link>
            <Link to="/register/hospital" className="text-secondary font-semibold hover:underline">
              Hospital Sign Up
            </Link>
          </div>
        </div>
      </motion.div>
    </div>
  )
}
