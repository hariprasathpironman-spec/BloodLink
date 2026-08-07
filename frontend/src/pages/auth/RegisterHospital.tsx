import { useState } from "react"
import { motion } from "framer-motion"
import { Link, useNavigate } from "react-router"
import { Button } from "@/components/ui/button"
import { ModeToggle } from "@/components/mode-toggle"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { ShieldCheck, Eye, EyeOff } from "lucide-react"

export default function RegisterHospital() {
  const [loading, setLoading] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setLoading(true)
    try {
      const formData = new FormData(e.currentTarget)
      const data = {
        name: formData.get("name"),
        hospital_name: formData.get("hospital_name"),
        email: formData.get("email"),
        password: formData.get("password"),
        contact: formData.get("contact"),
        state: formData.get("state"),
        district: formData.get("district"),
        address: formData.get("address")
      }

      const API_URL = import.meta.env.VITE_API_URL || ""
      const res = await fetch(`${API_URL}/api/auth/register/hospital`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      })

      let result
      const text = await res.text()
      try {
        result = JSON.parse(text)
      } catch {
        result = { msg: text || "Unexpected server response" }
      }

      if (!res.ok) {
        alert(result.msg || JSON.stringify(result))
      } else {
        const registeredEmail = formData.get("email") as string
        navigate(`/verify-otp?email=${encodeURIComponent(registeredEmail)}`)
      }
    } catch (err: any) {
      alert(`Connection error: ${err.message || err}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-background flex flex-col items-center justify-center p-4 py-12 relative overflow-y-auto">
      <div className="absolute top-4 sm:top-8 left-4 sm:left-8">
        <Link to="/">
          <Button variant="ghost" className="text-muted-foreground">&larr; Home</Button>
        </Link>
      </div>
      <div className="absolute top-4 sm:top-8 right-4 sm:right-8">
        <ModeToggle />
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-lg glass p-6 sm:p-10 rounded-3xl mt-12 sm:mt-0 border-secondary/20"
      >
        <div className="flex items-center gap-3 mb-2">
          <ShieldCheck className="h-8 w-8 text-secondary" />
          <h2 className="text-3xl font-bold text-secondary">Hospital Registration</h2>
        </div>
        <p className="text-muted-foreground mb-8">
          Submit your institutional details and verify your email to get started.
        </p>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid md:grid-cols-2 gap-6">
            <div className="space-y-2 md:col-span-2">
              <Label htmlFor="hospital_name">Hospital Name</Label>
              <Input id="hospital_name" name="hospital_name" placeholder="e.g. Apollo Hospitals" required />
            </div>

            <div className="space-y-2 md:col-span-2">
              <Label htmlFor="name">Authorized Person Name</Label>
              <Input id="name" name="name" placeholder="Full name of contact person" required />
            </div>

            <div className="space-y-2">
              <Label htmlFor="email">Official Email</Label>
              <Input id="email" name="email" type="email" placeholder="hospital@example.com" required />
            </div>

            {/* Password with toggle */}
            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <div className="relative">
                <Input
                  id="password"
                  name="password"
                  type={showPassword ? "text" : "password"}
                  placeholder="Create a strong password"
                  required
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

            <div className="space-y-2">
              <Label htmlFor="contact">Contact Number</Label>
              <Input id="contact" name="contact" type="tel" placeholder="+91 99999 99999" required />
            </div>

            <div className="space-y-2">
              <Label htmlFor="state">State</Label>
              <Input id="state" name="state" defaultValue="Tamil Nadu" required />
            </div>

            <div className="space-y-2">
              <Label htmlFor="district">District</Label>
              <Input id="district" name="district" placeholder="e.g. Chennai" required />
            </div>

            <div className="space-y-2 md:col-span-2">
              <Label htmlFor="address">Full Address</Label>
              <Input id="address" name="address" placeholder="Street, City, PIN" required />
            </div>
          </div>

          <Button
            type="submit"
            variant="secondary"
            className="w-full h-12 text-md mt-4"
            disabled={loading}
          >
            {loading ? "Registering..." : "Register & Send OTP"}
          </Button>
        </form>

        <div className="mt-6 text-center text-sm text-muted-foreground">
          Already registered?{" "}
          <Link to="/login" className="text-secondary font-semibold hover:underline">
            Login
          </Link>
        </div>
      </motion.div>
    </div>
  )
}
