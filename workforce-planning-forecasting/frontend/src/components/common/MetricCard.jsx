export default function MetricCard({ label, value, detail, tone = 'navy' }) {
  return (
    <div className="metric-card">
      <div className="metric-header">
        <span className="metric-label">{label}</span>
        <span className={`metric-badge ${tone}`}>{detail}</span>
      </div>
      <h3>{value}</h3>
    </div>
  )
}
