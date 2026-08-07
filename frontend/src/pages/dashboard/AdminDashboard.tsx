import { motion } from "framer-motion"
import { ShieldAlert, Check, X, AlertTriangle, FileText, LogOut } from "lucide-react"
import { Button } from "@/components/ui/button"
import { ModeToggle } from "@/components/mode-toggle"
import { useNavigate } from "react-router"

export default function AdminDashboard() {
  const navigate = useNavigate()

  const handleLogout = () => {
    localStorage.removeItem("token")
    localStorage.removeItem("role")
    navigate("/")
  }

  // Mock data for Admin Panel
  const pendingHospitals = [
    { id: "h10", name: "Metro General Hospital", regId: "REG-2023-899", date: "2023-10-24" },
  ]
  const fraudAlerts = [
    { id: "f1", type: "Multiple Accounts", ip: "192.168.1.100", severity: "High" }
  ]

  return (
    <div className="min-h-screen bg-background">
      <nav className="border-b bg-card px-4 sm:px-6 py-4 flex justify-between items-center shadow-sm">
        <div className="flex items-center gap-2">
          <ShieldAlert className="h-6 w-6 text-primary" />
          <span className="text-lg sm:text-xl font-bold">Admin Console</span>
        </div>
        <div className="flex items-center gap-2 sm:gap-4">
          <div className="text-xs sm:text-sm font-semibold text-muted-foreground hidden sm:block">
            Secure Session Active
          </div>
          <ModeToggle />
          <Button variant="ghost" size="icon" onClick={handleLogout} className="text-muted-foreground">
            <LogOut className="h-5 w-5" />
          </Button>
        </div>
      </nav>

      <main className="container mx-auto p-4 sm:p-6 mt-4">
        {/* Analytics Overview */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8 sm:mb-10">
          <div className="glass p-4 sm:p-5 rounded-2xl"><h4 className="text-muted-foreground text-xs sm:text-sm font-semibold mb-1">Total Donors</h4><p className="text-xl sm:text-2xl font-black">1,245</p></div>
          <div className="glass p-4 sm:p-5 rounded-2xl"><h4 className="text-muted-foreground text-xs sm:text-sm font-semibold mb-1">Verified Hospitals</h4><p className="text-xl sm:text-2xl font-black">48</p></div>
          <div className="glass p-4 sm:p-5 rounded-2xl"><h4 className="text-muted-foreground text-xs sm:text-sm font-semibold mb-1">Active Requests</h4><p className="text-xl sm:text-2xl font-black">12</p></div>
          <div className="glass p-4 sm:p-5 rounded-2xl bg-primary/5 border-primary/20"><h4 className="text-primary text-xs sm:text-sm font-semibold mb-1">Flagged Activity</h4><p className="text-xl sm:text-2xl font-black text-primary">1</p></div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 sm:gap-8">
          {/* Pending Hospital Verifications */}
          <section>
            <h2 className="text-lg sm:text-xl font-bold mb-4 flex items-center gap-2">
              <FileText className="h-5 w-5" /> Pending Verifications
            </h2>
            <div className="space-y-4">
              {pendingHospitals.map(h => (
                <motion.div key={h.id} initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="glass p-4 sm:p-5 rounded-2xl border-l-4 border-l-yellow-500">
                  <div className="flex flex-col sm:flex-row sm:justify-between sm:items-start mb-4 gap-2">
                    <div>
                      <h4 className="font-bold text-base sm:text-lg">{h.name}</h4>
                      <p className="text-sm text-muted-foreground">ID: {h.regId} | Applied: {h.date}</p>
                    </div>
                    <div className="flex gap-2">
                      <Button size="icon" variant="outline" className="text-green-600 border-green-600 hover:bg-green-50"><Check className="h-4 w-4" /></Button>
                      <Button size="icon" variant="outline" className="text-destructive border-destructive hover:bg-destructive/10"><X className="h-4 w-4" /></Button>
                    </div>
                  </div>
                  <Button variant="link" className="px-0 text-sm h-auto">View Submitted Documents</Button>
                </motion.div>
              ))}
            </div>
          </section>

          {/* Fraud & Audit Alerts */}
          <section>
            <h2 className="text-lg sm:text-xl font-bold mb-4 flex items-center gap-2 text-primary">
              <AlertTriangle className="h-5 w-5" /> Security Alerts
            </h2>
            <div className="space-y-4">
              {fraudAlerts.map(f => (
                <motion.div key={f.id} initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="glass p-4 sm:p-5 rounded-2xl border-l-4 border-l-primary bg-primary/5">
                  <div className="flex justify-between items-center mb-2">
                    <span className="font-bold">{f.type}</span>
                    <span className="text-xs px-2 py-1 bg-primary text-primary-foreground rounded-full">{f.severity} Risk</span>
                  </div>
                  <p className="text-sm text-muted-foreground mb-4">Origin IP: {f.ip}</p>
                  <Button variant="default" size="sm" className="w-full">Investigate Log</Button>
                </motion.div>
              ))}
            </div>
          </section>
        </div>
      </main>
    </div>
  )
}
