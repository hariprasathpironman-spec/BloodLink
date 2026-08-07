import { BrowserRouter, Routes, Route, Navigate } from "react-router";
import LandingPage from "./pages/LandingPage";
import Login from "./pages/auth/Login";
import RegisterDonor from "./pages/auth/RegisterDonor";
import RegisterHospital from "./pages/auth/RegisterHospital";
import VerifyOTP from "./pages/auth/VerifyOTP";
import DonorDashboard from "./pages/dashboard/DonorDashboard";
import HospitalDashboard from "./pages/dashboard/HospitalDashboard";
import AdminDashboard from "./pages/dashboard/AdminDashboard";
import ProtectedRoute from "./components/ProtectedRoute";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register/donor" element={<RegisterDonor />} />
        <Route path="/register/hospital" element={<RegisterHospital />} />
        <Route path="/verify-otp" element={<VerifyOTP />} />
        
        {/* Dashboards */}
        <Route path="/donor" element={
          <ProtectedRoute requiredRole="donor">
            <DonorDashboard />
          </ProtectedRoute>
        } />
        <Route path="/hospital" element={
          <ProtectedRoute requiredRole="hospital">
            <HospitalDashboard />
          </ProtectedRoute>
        } />
        <Route path="/admin" element={
          <ProtectedRoute requiredRole="admin">
            <AdminDashboard />
          </ProtectedRoute>
        } />

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
