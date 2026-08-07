import { useState } from "react"
import { motion } from "framer-motion"
import { Link, useNavigate } from "react-router"
import { Button } from "@/components/ui/button"
import { ModeToggle } from "@/components/mode-toggle"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Eye, EyeOff } from "lucide-react"

export default function RegisterDonor() {
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
        email: formData.get("email"),
        password: formData.get("password"),
        blood_group: formData.get("blood_group"),
        state: formData.get("state"),
        district: formData.get("district"),
        age: parseInt(formData.get("age") as string),
        weight: parseInt(formData.get("weight") as string),
        gender: formData.get("gender")
      }

      const API_URL = import.meta.env.VITE_API_URL || ""
      const res = await fetch(`${API_URL}/api/auth/register/donor`, {
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
        className="w-full max-w-lg glass p-6 sm:p-10 rounded-3xl mt-12 sm:mt-0"
      >
        <h2 className="text-3xl font-bold mb-2 text-primary">Become a Donor</h2>
        <p className="text-muted-foreground mb-8">
          Join the verified network and save lives in your area.
        </p>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <Label htmlFor="name">Full Name</Label>
              <Input id="name" name="name" placeholder="John Doe" required />
            </div>

            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input id="email" name="email" type="email" placeholder="you@example.com" required />
            </div>

            {/* Password with toggle */}
            <div className="space-y-2 md:col-span-2">
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
              <Label htmlFor="blood_group">Blood Group</Label>
              <select
                id="blood_group"
                name="blood_group"
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                required
              >
                <option value="">Select Group</option>
                {["A+","O+","B+","AB+","A-","O-","B-","AB-"].map(g => (
                  <option key={g} value={g}>{g}</option>
                ))}
              </select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="state">State</Label>
              <Input id="state" name="state" defaultValue="Tamil Nadu" required />
            </div>

            <div className="space-y-2">
              <Label htmlFor="district">District</Label>
              <Input id="district" name="district" placeholder="e.g. Chennai" required />
            </div>

            <div className="space-y-2">
              <Label htmlFor="age">Age</Label>
              <Input id="age" name="age" type="number" min="18" max="65" placeholder="18–65" required />
            </div>

            <div className="space-y-2">
              <Label htmlFor="weight">Weight (kg)</Label>
              <Input id="weight" name="weight" type="number" min="45" placeholder="min 45 kg" required />
            </div>

            <div className="space-y-2">
              <Label htmlFor="gender">Gender</Label>
              <select
                id="gender"
                name="gender"
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                required
              >
                <option value="">Select Gender</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
              </select>
            </div>
          </div>

          <Button type="submit" className="w-full h-12 text-md mt-4" disabled={loading}>
            {loading ? "Registering..." : "Register & Send OTP"}
          </Button>
        </form>

        <div className="mt-6 text-center text-sm text-muted-foreground">
          Already registered?{" "}
          <Link to="/login" className="text-primary font-semibold hover:underline">
            Login
          </Link>
        </div>
      </motion.div>
    </div>
  )
}
