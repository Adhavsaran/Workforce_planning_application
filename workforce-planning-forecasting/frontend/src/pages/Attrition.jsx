import { useEffect, useMemo, useState } from 'react'
import { getAttritionSummary } from '../services/api'

export default function AttritionPage() {
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const load = async () => {
      try {
        const response = await getAttritionSummary()
        setSummary(response.data || null)
        setError('')
      } catch (err) {
        setError('Unable to load attrition analysis.')
      } finally {
        setLoading(false)
      }
    }

    load()
  }, [])

  const byDepartment = useMemo(() => summary?.by_department || [], [summary])

  return (
    <div className="page-shell">
      <div className="panel">
        <div className="panel-header">
          <h3>Employee Attrition Analysis</h3>
          <span className="panel-tag">Data-driven overview</span>
        </div>

        {error && <p className="error-text">{error}</p>}

        {loading ? (
          <p>Loading attrition data...</p>
        ) : (
          <div className="info-stack">
            <div className="info-row"><span>Current attrition rate</span><strong>{summary?.attrition_rate ?? 0}%</strong></div>
            <div className="info-row"><span>Active employees</span><strong>{summary?.active_employees ?? 0}</strong></div>
            <div className="info-row"><span>Employees who left</span><strong>{summary?.employees_left ?? 0}</strong></div>
            <div className="info-row"><span>Method</span><strong>{summary?.method || 'Not available'}</strong></div>
          </div>
        )}
      </div>

      <div className="panel">
        <div className="panel-header">
          <h3>Department Attrition Rates</h3>
        </div>
        {byDepartment.length === 0 ? (
          <p>No department-level attrition data available.</p>
        ) : (
          <div className="info-stack">
            {byDepartment.map((item) => (
              <div className="info-row" key={item.department_name}>
                <span>{item.department_name}</span>
                <strong>{item.attrition_rate}% ({item.employees_left}/{item.total_employees})</strong>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
