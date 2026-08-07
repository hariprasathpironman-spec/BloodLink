import { motion } from "framer-motion"
import { Link } from "react-router"
import { Button } from "@/components/ui/button"
import { ModeToggle } from "@/components/mode-toggle"
import { HeartPulse, Hospital, ShieldCheck } from "lucide-react"

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background relative overflow-hidden">
      {/* Decorative Background */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden -z-10">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-primary/10 blur-[100px]" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-secondary/10 blur-[100px]" />
      </div>

      {/* Navbar */}
      <nav className="container mx-auto px-6 py-6 flex justify-between items-center relative z-10 glass rounded-b-2xl mb-10">
        <div className="flex items-center gap-2">
          <HeartPulse className="h-8 w-8 text-primary" />
          <span className="text-xl font-bold tracking-tight">BloodLink</span>
        </div>
        <div className="flex gap-2 sm:gap-4 items-center">
          <Link to="/login">
            <Button variant="ghost" className="hidden sm:inline-flex">Login</Button>
            <Button variant="ghost" className="sm:hidden px-2">Log in</Button>
          </Link>
          <Link to="/register/donor">
            <Button className="px-3 sm:px-4">Donate</Button>
          </Link>
          <ModeToggle />
        </div>
      </nav>

      {/* Hero Section */}
      <main className="container mx-auto px-6 flex flex-col items-center justify-center text-center pt-20 pb-32">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <span className="px-4 py-1.5 rounded-full bg-primary/10 text-primary text-sm font-semibold mb-6 inline-block">
            Verified Emergency Network
          </span>
          <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-extrabold tracking-tight mb-4 sm:mb-6 leading-tight">
            Save a life.<br />
            <span className="gradient-text">Be a Hero.</span>
          </h1>
          <p className="text-base sm:text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto mb-8 sm:mb-10 px-4">
            Connecting verified hospitals directly with willing donors through our AI Match Score Engine. No scams, no delays, just secure life-saving connections.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/register/donor">
              <Button size="lg" className="w-full sm:w-auto h-14 px-8 text-lg rounded-full shadow-lg hover:shadow-primary/25 transition-all">
                I want to Donate
              </Button>
            </Link>
            <Link to="/register/hospital">
              <Button variant="outline" size="lg" className="w-full sm:w-auto h-14 px-8 text-lg rounded-full glass hover:bg-secondary/5">
                Register Hospital
              </Button>
            </Link>
          </div>
        </motion.div>

        {/* Features */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8 mt-20 sm:mt-32">
          <motion.div 
            className="glass p-8 rounded-2xl text-left"
            whileHover={{ y: -5 }}
          >
            <ShieldCheck className="h-10 w-10 text-primary mb-4" />
            <h3 className="text-xl font-bold mb-2">Verified Network</h3>
            <p className="text-muted-foreground">Every hospital is strictly verified by administrators via document checks to prevent fraudulent requests.</p>
          </motion.div>
          <motion.div 
            className="glass p-8 rounded-2xl text-left"
            whileHover={{ y: -5 }}
          >
            <HeartPulse className="h-10 w-10 text-secondary mb-4" />
            <h3 className="text-xl font-bold mb-2">AI Match Score</h3>
            <p className="text-muted-foreground">Our deterministic matching engine instantly connects the most compatible donors to urgent emergencies.</p>
          </motion.div>
          <motion.div 
            className="glass p-8 rounded-2xl text-left"
            whileHover={{ y: -5 }}
          >
            <Hospital className="h-10 w-10 text-primary mb-4" />
            <h3 className="text-xl font-bold mb-2">Direct Hospital Access</h3>
            <p className="text-muted-foreground">Donors communicate directly with verified medical professionals, ensuring privacy and rapid response.</p>
          </motion.div>
        </div>
      </main>
    </div>
  )
}
