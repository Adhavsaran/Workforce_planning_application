import { useEffect, useMemo, useState } from 'react'
import { BarChart, Bar, CartesianGrid, PieChart, Pie, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { getDepartments, getEmployees } from '../services/api'

const colors = ['#123a5a', '#2574c7', '#14b8a6', '#64748b', '#f59e0b']

export default function AnalyticsPage() {
  const [employees, setEmployees] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true)
        const response = await getEmployees({ page: 1, page_size: 1000, sort_by: 'name', sort_order: 'asc' })
        setEmployees(response.data.items || [])
        setError('')
      } catch (err) {
        setError('Unable to load analytics data.')
      } finally {
        setLoading(false)
      }
    }

    loadData()
  }, [])

  const analytics = useMemo(() => {
    const departmentData = Object.entries(
      employees.reduce((acc, employee) => {
        const departmentName = employee.department?.name || 'Unassigned'
        acc[departmentName] = (acc[departmentName] || 0) + 1
        return acc
      }, {})
    ).map(([name, value]) => ({ name, value }))

    const employmentTypeData = Object.entries(
      employees.reduce((acc, employee) => {
        const label = employee.employment_type || 'UNKNOWN'
        acc[label] = (acc[label] || 0) + 1
        return acc
      }, {})
    ).map(([name, value]) => ({ name, value }))

    const attritionData = [
      { name: 'Active', value: employees.filter((employee) => String(employee.attrition_status).toUpperCase() === 'ACTIVE').length },
      { name: 'Left', value: employees.filter((employee) => String(employee.attrition_status).toUpperCase() === 'LEFT').length },
    ]

    const experienceGroups = [
      { name: '0–2 years', value: employees.filter((employee) => Number(employee.experience_years || 0) <= 2).length },
      { name: '3–5 years', value: employees.filter((employee) => Number(employee.experience_years || 0) > 2 && Number(employee.experience_years || 0) <= 5).length },
      { name: '6–10 years', value: employees.filter((employee) => Number(employee.experience_years || 0) > 5 && Number(employee.experience_years || 0) <= 10).length },
      { name: '10+ years', value: employees.filter((employee) => Number(employee.experience_years || 0) > 10).length },
    ]

    return { departmentData, employmentTypeData, attritionData, experienceGroups }
  }, [employees])

  if (loading) return <div className="page-shell"><div className="panel"><p>Loading analytics...</p></div></div>
  if (error) return <div className="page-shell"><div className="panel"><p className="error-text">{error}</p></div></div>

  return (
    <div className="page-shell">
      <div className="panel">
        <div className="panel-header">
          <h3>Employee Distribution</h3>
          <span className="panel-tag">By department</span>
        </div>
        <div style={{ width: '100%', height: 280 }}>
          <ResponsiveContainer>
            <BarChart data={analytics.departmentData}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5edf7" />
              <XAxis dataKey="name" tick={{ fontSize: 12 }} />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Bar dataKey="value" radius={[8, 8, 0, 0]} fill="#2574c7" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="panel-grid two-columns">
        <div className="panel">
          <div className="panel-header">
            <h3>Employment Type</h3>
            <span className="panel-tag">Live</span>
          </div>
          <div style={{ width: '100%', height: 260 }}>
            <ResponsiveContainer>
              <PieChart>
                <Pie data={analytics.employmentTypeData} dataKey="value" nameKey="name" innerRadius={48} outerRadius={86} paddingAngle={3}>
                  {analytics.employmentTypeData.map((entry, index) => (
                    <Cell key={`${entry.name}-${index}`} fill={colors[index % colors.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="panel">
          <div className="panel-header">
            <h3>Attrition Status</h3>
            <span className="panel-tag">Current</span>
          </div>
          <div style={{ width: '100%', height: 260 }}>
            <ResponsiveContainer>
              <PieChart>
                <Pie data={analytics.attritionData} dataKey="value" nameKey="name" innerRadius={48} outerRadius={86} paddingAngle={3}>
                  {analytics.attritionData.map((entry, index) => (
                    <Cell key={`${entry.name}-${index}`} fill={index === 0 ? '#14b8a6' : '#f59e0b'} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="panel">
        <div className="panel-header">
          <h3>Experience Distribution</h3>
          <span className="panel-tag">Grouped</span>
        </div>
        <div style={{ width: '100%', height: 260 }}>
          <ResponsiveContainer>
            <BarChart data={analytics.experienceGroups}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5edf7" />
              <XAxis dataKey="name" tick={{ fontSize: 12 }} />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Bar dataKey="value" radius={[8, 8, 0, 0]} fill="#123a5a" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}
