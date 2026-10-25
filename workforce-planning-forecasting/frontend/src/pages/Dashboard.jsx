import { useEffect, useMemo, useState } from 'react'
import { BarChart, Bar, CartesianGrid, PieChart, Pie, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import MetricCard from '../components/common/MetricCard'
import { getDashboardSummary, getDepartments, getHealth } from '../services/api'

const colors = ['#123a5a', '#2574c7', '#14b8a6', '#f59e0b', '#64748b', '#0ea5e9']

export default function DashboardPage() {
  const [summary, setSummary] = useState({ total_employees: 0, total_departments: 0, active_employees: 0, left_employees: 0, department_distribution: [] })
  const [health, setHealth] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const loadDashboard = async () => {
      try {
        setLoading(true)
        const [summaryRes, healthRes] = await Promise.all([
          getDashboardSummary(),
          getHealth(),
        ])

        setSummary(summaryRes.data || { total_employees: 0, total_departments: 0, active_employees: 0, left_employees: 0, department_distribution: [] })
        setHealth(healthRes.data)
        setError('')
      } catch (err) {
        setError('Unable to load dashboard data. Please check the backend connection.')
      } finally {
        setLoading(false)
      }
    }

    loadDashboard()
  }, [])

  const chartData = useMemo(() => {
    const departmentData = (summary.department_distribution || []).map((department) => ({
      name: department.department_name,
      employees: department.employee_count,
    }))

    return { departmentData }
  }, [summary])

  const employmentTypeData = useMemo(() => [
    { name: 'ACTIVE', value: summary.active_employees },
    { name: 'LEFT', value: summary.left_employees },
  ], [summary])

  if (loading) return <div className="page-shell"><div className="panel"><p>Loading dashboard...</p></div></div>
  if (error) return <div className="page-shell"><div className="panel"><p className="error-text">{error}</p></div></div>

  const totalEmployees = summary.total_employees || 0

  return (
    <div className="page-shell">
      <div className="metric-grid">
        <MetricCard label="Total Employees" value={String(totalEmployees)} detail="Live" tone="navy" />
        <MetricCard label="Departments" value={String(summary.total_departments || 0)} detail="Active" tone="blue" />
        <MetricCard label="Active Employees" value={String(summary.active_employees || 0)} detail="Current" tone="teal" />
        <MetricCard label="Employees Who Left" value={String(summary.left_employees || 0)} detail="Attrition" tone="amber" />
      </div>

      <div className="panel-grid two-columns">
        <div className="panel">
          <div className="panel-header">
            <h3>Department Distribution</h3>
            <span className="panel-tag">Live data</span>
          </div>
          <div style={{ width: '100%', height: 260 }}>
            <ResponsiveContainer>
              <BarChart data={chartData.departmentData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5edf7" />
                <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                <YAxis allowDecimals={false} />
                <Tooltip />
                <Bar dataKey="employees" radius={[8, 8, 0, 0]} fill="#123a5a" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="panel">
          <div className="panel-header">
            <h3>Status</h3>
            <span className="panel-tag">Distribution</span>
          </div>
          <div style={{ width: '100%', height: 260 }}>
            <ResponsiveContainer>
              <PieChart>
                <Pie data={employmentTypeData} dataKey="value" nameKey="name" innerRadius={55} outerRadius={82} paddingAngle={4}>
                  {employmentTypeData.map((entry, index) => (
                    <Cell key={`${entry.name}-${index}`} fill={colors[index % colors.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="legend-list">
            {employmentTypeData.map((item, index) => (
              <div key={item.name} className="legend-item">
                <span className="legend-swatch" style={{ background: colors[index % colors.length] }} />
                {item.name} ({item.value})
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="panel-grid two-columns">
        <div className="panel">
          <div className="panel-header">
            <h3>Workforce Overview</h3>
            <span className="panel-tag">Live</span>
          </div>
          <div className="info-stack">
            <div className="info-row"><span>Database status</span><strong>{health?.database || 'Unknown'}</strong></div>
            <div className="info-row"><span>Environment</span><strong>{health?.environment || 'development'}</strong></div>
            <div className="info-row"><span>Average employees by department</span><strong>{summary.total_departments ? (totalEmployees / summary.total_departments).toFixed(1) : '0.0'}</strong></div>
            <div className="info-row"><span>Forecast status</span><strong>Available when historical records exist</strong></div>
          </div>
        </div>

        <div className="panel">
          <div className="panel-header">
            <h3>Hiring Recommendation</h3>
            <span className="panel-tag">Decision support</span>
          </div>
          <div className="recommendation-box">
            <h4>Current HR priority</h4>
            <p>
              Review department demand and attrition risk using the backend analytics. Forecasting and recommendation rules are derived from live workforce and staffing data when available.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
