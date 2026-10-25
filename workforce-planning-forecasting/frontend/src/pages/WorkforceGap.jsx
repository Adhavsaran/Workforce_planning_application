import { useEffect, useMemo, useState } from 'react'
import { getWorkforceGap } from '../services/api'

export default function WorkforceGapPage() {
  const [gapData, setGapData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const load = async () => {
      try {
        const response = await getWorkforceGap()
        setGapData(response.data || null)
        setError('')
      } catch (err) {
        setError('Unable to load workforce gap analysis.')
      } finally {
        setLoading(false)
      }
    }

    load()
  }, [])

  const rows = useMemo(() => gapData?.departments || [], [gapData])

  return (
    <div className="page-shell">
      <div className="panel">
        <div className="panel-header">
          <h3>Workforce Gap Analysis</h3>
          <span className="panel-tag">Gap = forecast demand − current supply</span>
        </div>

        {error && <p className="error-text">{error}</p>}

        {loading ? (
          <p>Loading gap analysis...</p>
        ) : (
          <div className="info-stack">
            <div className="info-row"><span>Overall gap</span><strong>{gapData?.overall_gap ?? 0}</strong></div>
            <div className="info-row"><span>Convention</span><strong>{gapData?.sign_convention || 'Not available'}</strong></div>
          </div>
        )}
      </div>

      <div className="panel">
        <div className="panel-header">
          <h3>Department Gap Summary</h3>
        </div>
        {rows.length === 0 ? (
          <p>No department gaps available.</p>
        ) : (
          <div className="info-stack">
            {rows.map((item) => (
              <div className="info-row" key={item.department_id}>
                <span>{item.department_name}</span>
                <strong>{item.gap >= 0 ? `Shortage ${item.gap}` : `Surplus ${Math.abs(item.gap)}`} ({item.current_supply} vs {item.forecast_demand})</strong>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
