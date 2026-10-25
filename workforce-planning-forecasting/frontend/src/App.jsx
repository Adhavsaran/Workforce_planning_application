import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Sidebar from './components/layout/Sidebar'
import Topbar from './components/layout/Topbar'
import './App.css'
import DashboardPage from './pages/Dashboard'
import EmployeesPage from './pages/Employees'
import DepartmentsPage from './pages/Departments'
import AnalyticsPage from './pages/Analytics'
import ForecastingPage from './pages/Forecasting'
import AttritionPage from './pages/Attrition'
import WorkforceGapPage from './pages/WorkforceGap'
import RecommendationsPage from './pages/Recommendations'

function LoginPage() {
  return (
    <div className="login-shell">
      <div className="login-card">
        <p className="eyebrow">Secure Access</p>
        <h2>Workforce Planning Portal</h2>
        <p className="login-copy">Login to review workforce insights, staffing levels, and HR decisions.</p>
        <div className="login-field">
          <label>Email</label>
          <input type="email" placeholder="hr.admin@company.com" />
        </div>
        <div className="login-field">
          <label>Password</label>
          <input type="password" placeholder="••••••••" />
        </div>
        <button type="button" className="primary-button full-width">Login</button>
      </div>
    </div>
  )
}

function AppLayout() {
  return (
    <div className="app-shell">
      <Sidebar />
      <main className="content-area">
        <Topbar />
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/" element={<DashboardPage />} />
          <Route path="/employees" element={<EmployeesPage />} />
          <Route path="/departments" element={<DepartmentsPage />} />
          <Route path="/analytics" element={<AnalyticsPage />} />
          <Route path="/forecasting" element={<ForecastingPage />} />
          <Route path="/attrition" element={<AttritionPage />} />
          <Route path="/workforce-gap" element={<WorkforceGapPage />} />
          <Route path="/recommendations" element={<RecommendationsPage />} />
        </Routes>
      </main>
    </div>
  )
}

function App() {
  return (
    <BrowserRouter>
      <AppLayout />
    </BrowserRouter>
  )
}

export default App
