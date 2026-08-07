import { useState, useRef, useEffect, FormEvent, KeyboardEvent } from "react"
import { useNavigate, Link } from "react-router"
import { motion } from "framer-motion"
import { HeartPulse, ArrowLeft, CheckCircle2, AlertCircle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { ModeToggle } from "@/components/mode-toggle"

const API_URL = import.meta.env.VITE_API_URL || ""

export default function VerifyOTP() {
  const navigate = useNavigate()
  const [email, setEmail] = useState<string | null>(null)
  const [otp, setOtp] = useState<string[]>(Array(6).fill(""))
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)
  
  // Timer state
  const [timeLeft, setTimeLeft] = useState(600) // 10 minutes
  const [resendDisabled, setResendDisabled] = useState(true)
  const [resendTimer, setResendTimer] = useState(60)

  const inputRefs = useRef<(HTMLInputElement | null)[]>([])

  useEffect(() => {
    const params = new URLSearchParams(window.location.search)
    const emailParam = params.get("email")
    if (!emailParam) {
      navigate("/login")
      return
    }
    setEmail(emailParam)
  }, [navigate])

  useEffect(() => {
    if (timeLeft <= 0) return
    const timerId = setInterval(() => setTimeLeft((prev) => prev - 1), 1000)
    return () => clearInterval(timerId)
  }, [timeLeft])

  useEffect(() => {
    if (resendTimer <= 0) {
      setResendDisabled(false)
      return
    }
    const timerId = setInterval(() => setResendTimer((prev) => prev - 1), 1000)
    return () => clearInterval(timerId)
  }, [resendTimer])

  const formatTime = (seconds: number) => {
    const m = Math.floor(seconds / 60)
    const s = seconds % 60
    return `${m}:${s.toString().padStart(2, "0")}`
  }

  const handleChange = (index: number, value: string) => {
    if (!/^\d*$/.test(value)) return
    
    const newOtp = [...otp]
    newOtp[index] = value.slice(-1)
    setOtp(newOtp)

    if (value && index < 5) {
      inputRefs.current[index + 1]?.focus()
    }
  }

  const handleKeyDown = (index: number, e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Backspace" && !otp[index] && index > 0) {
      inputRefs.current[index - 1]?.focus()
    }
  }

  const handlePaste = (e: React.ClipboardEvent) => {
    e.preventDefault()
    const pastedData = e.clipboardData.getData("text").slice(0, 6).replace(/\D/g, "")
    if (!pastedData) return

    const newOtp = [...otp]
    for (let i = 0; i < pastedData.length; i++) {
      newOtp[i] = pastedData[i]
    }
    setOtp(newOtp)
    
    const focusIndex = Math.min(pastedData.length, 5)
    inputRefs.current[focusIndex]?.focus()
  }

  const handleResend = async () => {
    setResendDisabled(true)
    setResendTimer(60)
    setError("")
    try {
      const res = await fetch(`${API_URL}/api/auth/resend-otp`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      })
      const data = await res.json()
      if (!res.ok) {
        setError(data.msg || "Failed to resend OTP")
      }
      setTimeLeft(600)
    } catch {
      setError("Network error. Could not resend OTP.")
    }
  }

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setError("")
    
    const otpCode = otp.join("")
    if (otpCode.length !== 6) {
      setError("Please enter all 6 digits")
      return
    }

    setLoading(true)
    try {
      const response = await fetch(`${API_URL}/api/auth/verify-otp`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, otp_code: otpCode }),
      })

      const data = await response.json()

      if (response.ok) {
        setSuccess(true)
        setTimeout(() => {
          navigate("/login")
        }, 2000)
      } else {
        setError(data.msg || "Invalid OTP code")
      }
    } catch (err: any) {
      setError("Network error. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  if (!email) return null

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-background relative overflow-hidden">
      <div className="absolute top-4 right-4 z-50">
        <ModeToggle />
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-md"
      >
        <Link
          to="/login"
          className="inline-flex items-center text-sm font-medium text-muted-foreground hover:text-foreground mb-6 transition-colors"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to login
        </Link>

        <div className="glass border rounded-2xl p-8 relative overflow-hidden">
          <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-red-500 to-red-600" />
          
          <div className="text-center mb-8">
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: "spring", bounce: 0.5 }}
              className="w-16 h-16 bg-red-100/10 dark:bg-red-500/10 rounded-2xl flex items-center justify-center mx-auto mb-4 border border-red-500/20"
            >
              <HeartPulse className="w-8 h-8 text-red-500" />
            </motion.div>
            <h1 className="text-2xl font-bold mb-2">Verify Your Email</h1>
            <p className="text-muted-foreground text-sm">
              We sent a 6-digit code to<br />
              <span className="font-medium text-foreground">{email}</span>
            </p>
          </div>

          {success ? (
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              className="flex flex-col items-center justify-center py-8"
            >
              <CheckCircle2 className="w-16 h-16 text-green-500 mb-4" />
              <h2 className="text-xl font-semibold text-foreground">Verified Successfully!</h2>
              <p className="text-muted-foreground mt-2 text-sm">Redirecting to login...</p>
            </motion.div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="space-y-4">
                <div className="flex justify-between items-center px-1">
                  <Label>Security Code</Label>
                  <span className="text-sm text-red-500 font-mono">
                    {formatTime(timeLeft)}
                  </span>
                </div>
                
                <motion.div 
                  className="flex justify-between gap-2"
                  animate={error ? { x: [-10, 10, -10, 10, 0] } : {}}
                  transition={{ duration: 0.4 }}
                >
                  {otp.map((digit, index) => (
                    <input
                      key={index}
                      ref={(el) => (inputRefs.current[index] = el)}
                      type="text"
                      inputMode="numeric"
                      value={digit}
                      onChange={(e) => handleChange(index, e.target.value)}
                      onKeyDown={(e) => handleKeyDown(index, e)}
                      onPaste={handlePaste}
                      className={`w-12 h-14 text-center text-xl font-bold rounded-lg border bg-background/50 focus:bg-background focus:ring-2 focus:ring-red-500 focus:border-red-500 outline-none transition-all ${
                        error ? "border-red-500 focus:ring-red-500" : "border-border"
                      }`}
                      maxLength={1}
                    />
                  ))}
                </motion.div>
              </div>

              {error && (
                <motion.div
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="flex items-center gap-2 text-red-500 text-sm bg-red-500/10 p-3 rounded-lg border border-red-500/20"
                >
                  <AlertCircle className="w-4 h-4 shrink-0" />
                  <p>{error}</p>
                </motion.div>
              )}

              <Button
                type="submit"
                className="w-full bg-red-600 hover:bg-red-700 text-white"
                disabled={loading || otp.join("").length !== 6 || timeLeft <= 0}
              >
                {loading ? "Verifying..." : "Verify OTP"}
              </Button>

              <div className="text-center text-sm">
                <span className="text-muted-foreground">Didn't receive the code? </span>
                <button
                  type="button"
                  onClick={handleResend}
                  disabled={resendDisabled}
                  className="text-red-500 hover:text-red-400 font-medium disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {resendDisabled ? `Resend in ${resendTimer}s` : "Resend OTP"}
                </button>
              </div>
            </form>
          )}
        </div>
      </motion.div>
    </div>
  )
}
