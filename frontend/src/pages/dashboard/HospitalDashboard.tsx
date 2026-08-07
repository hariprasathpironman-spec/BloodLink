import { motion } from "framer-motion"
import { Hospital, Plus, Activity, CheckCircle, Users, LogOut } from "lucide-react"
import { Button } from "@/components/ui/button"
import { ModeToggle } from "@/components/mode-toggle"
import { useNavigate } from "react-router"

export default function HospitalDashboard() {
  const navigate = useNavigate()

  const handleLogout = () => {
    localStorage.removeItem("token")
    localStorage.removeItem("role")
    navigate("/")
  }

  // Mock Active Requests & AI Matches
  const mockActiveRequests = [
    { id: 101, patient: "Anil K.", group: "A-", units: 2, status: "Open", matches: 4 },
  ]
  
  const mockMatchedDonors = [
    { id: 1, name: "Priya S.", group: "A-", score: 92, badge: "Best Match", dist: "Chennai" },
    { id: 2, name: "Ramesh T.", group: "O-", score: 75, badge: "Good Match", dist: "Chennai" }
  ]

  return (
    <div className="min-h-screen bg-background p-4 sm:p-8">
      <nav className="flex justify-between items-center mb-6 sm:mb-8">
        <div className="flex items-center gap-3">
          <Hospital className="h-6 w-6 sm:h-8 sm:w-8 text-primary" />
          <h1 className="text-xl sm:text-3xl font-bold">City Hospital Portal</h1>
        </div>
        <div className="flex gap-2 sm:gap-4 items-center">
          <div className="px-3 py-1 bg-green-100 text-green-700 text-xs font-bold rounded-full hidden md:flex items-center gap-1">
            <CheckCircle className="h-3 w-3" /> Verified by Admin
          </div>
          <ModeToggle />
          <Button variant="ghost" size="icon" onClick={handleLogout} className="text-muted-foreground">
            <LogOut className="h-5 w-5" />
          </Button>
        </div>
      </nav>

      <main className="container mx-auto">
        {/* Stats Row */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="glass p-6 rounded-2xl flex items-center gap-4 border-l-4 border-l-secondary">
            <div className="p-3 bg-secondary/10 rounded-xl text-secondary"><Activity className="h-6 w-6" /></div>
            <div><p className="text-sm text-muted-foreground font-semibold">Active Requests</p><h3 className="text-3xl font-black">1</h3></div>
          </motion.div>
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="glass p-6 rounded-2xl flex items-center gap-4">
            <div className="p-3 bg-primary/10 rounded-xl text-primary"><Users className="h-6 w-6" /></div>
            <div><p className="text-sm text-muted-foreground font-semibold">Matched Donors</p><h3 className="text-3xl font-black">4</h3></div>
          </motion.div>
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="glass p-6 rounded-2xl flex items-center gap-4">
            <div className="p-3 bg-green-100 rounded-xl text-green-600"><CheckCircle className="h-6 w-6" /></div>
            <div><p className="text-sm text-muted-foreground font-semibold">Requests Fulfilled</p><h3 className="text-3xl font-black">12</h3></div>
          </motion.div>
        </div>

        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold">Manage Emergency Requests</h2>
          <Button className="bg-secondary hover:bg-secondary/90 gap-2 shadow-lg shadow-secondary/20">
            <Plus className="h-4 w-4" /> Create Request
          </Button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 sm:gap-8">
          {/* Active Requests List */}
          <div className="lg:col-span-1 space-y-4">
            <h3 className="text-lg font-semibold text-muted-foreground mb-4">Open Requests</h3>
            {mockActiveRequests.map(req => (
              <div key={req.id} className="glass p-5 rounded-2xl border border-secondary/20 cursor-pointer hover:bg-secondary/5 transition-colors">
                <div className="flex justify-between items-start mb-2">
                  <h4 className="font-bold text-lg">{req.patient}</h4>
                  <span className="px-2 py-0.5 rounded text-xs font-bold bg-primary/10 text-primary">{req.group} Required</span>
                </div>
                <p className="text-sm text-muted-foreground mb-3">{req.units} Units • Needs fulfillment</p>
                <div className="text-xs font-semibold text-secondary flex items-center gap-1">
                  <Users className="h-3 w-3" /> {req.matches} Donors Found
                </div>
              </div>
            ))}
          </div>

          {/* AI Matches Panel */}
          <div className="lg:col-span-2 glass rounded-2xl p-6 border border-border">
            <div className="flex justify-between items-center border-b pb-4 mb-4">
              <h3 className="text-xl font-bold">AI Donor Matches</h3>
              <span className="text-sm font-semibold text-muted-foreground">Showing matches for Anil K. (A-)</span>
            </div>
            
            <div className="space-y-4">
              {mockMatchedDonors.map((match, i) => (
                <motion.div 
                  key={match.id}
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.1 }}
                  className="flex items-center justify-between p-4 rounded-xl border bg-card hover:shadow-sm transition-shadow"
                >
                  <div className="flex items-center gap-4">
                    <div className="h-12 w-12 rounded-full bg-accent flex items-center justify-center font-bold text-lg">
                      {match.group}
                    </div>
                    <div>
                      <h4 className="font-bold">{match.name}</h4>
                      <p className="text-sm text-muted-foreground">{match.dist}</p>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-4">
                    <div className="text-right">
                      <div className="font-black text-lg">{match.score}/100</div>
                      <div className={`text-xs font-bold ${match.score >= 85 ? 'text-green-600' : 'text-orange-500'}`}>
                        {match.badge}
                      </div>
                    </div>
                    <Button variant="outline" size="sm">Contact</Button>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
