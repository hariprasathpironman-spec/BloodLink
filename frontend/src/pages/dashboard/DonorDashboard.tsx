import { useState } from "react"
import { motion } from "framer-motion"
import { Bell, MapPin, Droplets, Calendar, Power, LogOut } from "lucide-react"
import { Button } from "@/components/ui/button"
import { ModeToggle } from "@/components/mode-toggle"
import { useNavigate } from "react-router"

export default function DonorDashboard() {
  const [isAvailable, setIsAvailable] = useState(true)
  const navigate = useNavigate()

  const handleLogout = () => {
    localStorage.removeItem("token")
    localStorage.removeItem("role")
    navigate("/")
  }

  // Mock Active Requests for UI presentation
  const mockRequests = [
    { id: 1, hospital: "Apollo Main", patient: "Rajesh K.", group: "O+", urgency: "High", dist: "Chennai", time: "2 hours ago" },
    { id: 2, hospital: "GH Hospital", patient: "Sita M.", group: "O-", urgency: "Medium", dist: "Chennai", time: "5 hours ago" }
  ]

  return (
    <div className="min-h-screen bg-background">
      {/* Top Navbar */}
      <nav className="border-b bg-card px-6 py-4 flex justify-between items-center shadow-sm">
        <div className="flex items-center gap-2">
          <Droplets className="h-6 w-6 text-primary" />
          <span className="text-xl font-bold">Donor Portal</span>
        </div>
        <div className="flex items-center gap-4">
          <ModeToggle />
          <button className="relative p-2 hover:bg-accent rounded-full transition-colors">
            <Bell className="h-5 w-5 text-muted-foreground" />
            <span className="absolute top-1 right-1 h-2 w-2 bg-primary rounded-full" />
          </button>
          <div className="h-8 w-8 bg-secondary/20 rounded-full flex items-center justify-center text-secondary font-bold">
            JD
          </div>
          <Button variant="ghost" size="icon" onClick={handleLogout} className="text-muted-foreground">
            <LogOut className="h-5 w-5" />
          </Button>
        </div>
      </nav>

      <main className="container mx-auto p-6 grid lg:grid-cols-3 gap-6 sm:gap-8 mt-4">
        {/* Left Column: Profile & Status */}
        <div className="space-y-6 sm:space-y-8">
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="glass p-6 sm:p-8 rounded-3xl"
          >
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold">Your Status</h2>
              <div className={`px-3 py-1 rounded-full text-xs font-semibold ${isAvailable ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                {isAvailable ? "Available" : "Unavailable"}
              </div>
            </div>
            
            <div className="flex items-center justify-center gap-4 py-6 border-y mb-6">
              <div className="text-center">
                <div className="text-3xl font-black text-primary">O+</div>
                <div className="text-sm text-muted-foreground">Blood Group</div>
              </div>
              <div className="h-10 w-px bg-border" />
              <div className="text-center">
                <div className="text-3xl font-black text-secondary">3</div>
                <div className="text-sm text-muted-foreground">Donations</div>
              </div>
            </div>

            <Button 
              variant={isAvailable ? "outline" : "default"} 
              className="w-full flex items-center gap-2"
              onClick={() => setIsAvailable(!isAvailable)}
            >
              <Power className="h-4 w-4" />
              {isAvailable ? "Go Offline" : "Go Online"}
            </Button>
          </motion.div>
        </div>

        {/* Right Column: Emergency Feed */}
        <div className="lg:col-span-2 space-y-6">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex justify-between items-center"
          >
            <h2 className="text-2xl font-bold">Emergency Feed</h2>
            <span className="text-sm text-muted-foreground">Showing matches near Chennai</span>
          </motion.div>

          <div className="grid gap-4">
            {mockRequests.map((req, i) => (
              <motion.div 
                key={req.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.1 }}
                className="glass p-6 rounded-2xl border-l-4 border-l-primary flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 hover:shadow-md transition-shadow"
              >
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="px-2 py-0.5 rounded text-xs font-bold bg-primary/10 text-primary uppercase">
                      {req.urgency} Priority
                    </span>
                    <span className="text-sm text-muted-foreground flex items-center gap-1">
                      <Calendar className="h-3 w-3" /> {req.time}
                    </span>
                  </div>
                  <h3 className="text-lg font-bold">{req.patient} needs {req.group} Blood</h3>
                  <div className="text-sm text-muted-foreground flex items-center gap-1 mt-1">
                    <MapPin className="h-4 w-4" /> {req.hospital}, {req.dist}
                  </div>
                </div>
                <Button className="w-full sm:w-auto shrink-0 shadow-lg shadow-primary/20">
                  Accept Request
                </Button>
              </motion.div>
            ))}
            
            {mockRequests.length === 0 && (
              <div className="text-center py-12 glass rounded-2xl text-muted-foreground">
                No active emergencies in your area right now.
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}
