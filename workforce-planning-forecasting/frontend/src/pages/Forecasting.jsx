import { useEffect, useMemo, useState } from 'react'
import { BarChart, Bar, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { generateForecast, getDepartments } from '../services/api'

export default function ForecastingPage() {
  const [departments, setDepartments] = useState([])
  const [forecasts, setForecasts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const loadForecastData = async () => {
      try {
        setLoading(true)
        const [departmentsResponse] = await Promise.all([
          getDepartments(),
        ])

        setDepartments(departmentsResponse.data || [])

        const results = []
        for (const department of departmentsResponse.data || []) {
          try {
            const response = await generateForecast({ department_id: department.id, months_ahead: 6 })
            results.push({
              name: department.name,
              forecasted_employee_count: response.data.forecasted_employee_count,
              confidence_score: Number(response.data.confidence_score || 0),
            })
          } catch (innerErr) {
            results.push({
              name: department.name,
              forecasted_employee_count: 0,
              confidence_score: 0,
            })
          }
        }

        setForecasts(results)
        setError('')
      } catch (err) {
        setError('Unable to load forecasting data. Please check the backend connection.')
      } finally {
        setLoading(false)
      }
    }

    loadForecastData()
  }, [])

  const summary = useMemo(() => {
    if (!forecasts.length) return { averageForecast: 0, totalForecast: 0 }
    const totalForecast = forecasts.reduce((sum, item) => sum + Number(item.forecasted_employee_count || 0), 0)
    const averageForecast = totalForecast / forecasts.length
    return { averageForecast, totalForecast }
  }, [forecasts])

  if (loading) return <div className="page-shell"><div className="panel"><p>Loading forecast data...</p></div></div>
  if (error) return <div className="page-shell"><div className="panel"><p className="error-text">{error}</p></div></div>

  return (
    <div className="page-shell">
      <div className="metric-grid">
        <div className="metric-card navy">
          <span className="metric-label">Total Forecasted Headcount</span>
          <strong>{summary.totalForecast}</strong>
          <small>6-month horizon</small>
        </div>
        <div className="metric-card blue">
          <span className="metric-label">Average Forecast</span>
          <strong>{summary.averageForecast.toFixed(1)}</strong>
          <small>Per department</small>
        </div>
      </div>

      <div className="panel-grid two-columns">
        <div className="panel">
          <div className="panel-header">
            <h3>Department Forecast</h3>
            <span className="panel-tag">Linear regression</span>
          </div>
          <div style={{ width: '100%', height: 280 }}>
            <ResponsiveContainer>
              <BarChart data={forecasts}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5edf7" />
                <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                <YAxis allowDecimals={false} />
                <Tooltip />
                <Bar dataKey="forecasted_employee_count" radius={[8, 8, 0, 0]} fill="#123a5a" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="panel">
          <div className="panel-header">
            <h3>Forecast Quality</h3>
            <span className="panel-tag">Confidence</span>
          </div>
          <div className="info-stack">
            {forecasts.map((item) => (
              <div className="info-row" key={item.name}>
                <span>{item.name}</span>
                <strong>{(item.confidence_score * 100).toFixed(0)}%</strong>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
