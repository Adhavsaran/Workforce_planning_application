export default function PlaceholderPanel({ title, description, tag = 'Coming Soon' }) {
  return (
    <div className="page-shell">
      <div className="panel single-panel">
        <div className="panel-header">
          <h3>{title}</h3>
          <span className="panel-tag">{tag}</span>
        </div>
        <div className="info-box">
          <p>{description}</p>
        </div>
      </div>
    </div>
  )
}
