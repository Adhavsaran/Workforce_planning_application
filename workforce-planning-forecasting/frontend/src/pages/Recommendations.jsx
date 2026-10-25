import { useEffect, useState } from 'react'
import { getRecommendations } from '../services/api'

export default function RecommendationsPage() {
  const [recommendations, setRecommendations] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const load = async () => {
      try {
        const response = await getRecommendations()
        setRecommendations(response.data || [])
        setError('')
      } catch (err) {
        setError('Unable to load HR recommendations.')
      } finally {
        setLoading(false)
      }
    }

    load()
  }, [])

  return (
    <div className="page-shell">
      <div className="panel">
        <div className="panel-header">
          <h3>HR Recommendations</h3>
          <span className="panel-tag">Explainable rules</span>
        </div>

        {error && <p className="error-text">{error}</p>}

        {loading ? (
          <p>Loading recommendations...</p>
        ) : recommendations.length === 0 ? (
          <p>No recommendation data is available yet.</p>
        ) : (
          <div className="info-stack">
            {recommendations.map((item) => (
              <div key={`${item.department_id}-${item.recommendation_type}`} className="recommendation-box">
                <h4>{item.department_name}</h4>
                <p><strong>{item.recommendation_type}</strong> · {item.priority} priority</p>
                <p>{item.recommendation_text}</p>
                <small>Supporting data: current supply {item.supporting_data.current_supply}, forecast demand {item.supporting_data.forecast_demand}, gap {item.supporting_data.gap}.</small>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
