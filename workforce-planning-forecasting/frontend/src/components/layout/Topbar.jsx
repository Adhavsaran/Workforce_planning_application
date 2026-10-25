export default function Topbar({ title = 'Workforce Planning Dashboard' }) {
  return (
    <header className="topbar">
      <div>
        <p className="eyebrow">Overview</p>
        <h1>{title}</h1>
      </div>
      <div className="topbar-actions">
        <button type="button" className="ghost-button">
          Export Report
        </button>
        <button type="button" className="primary-button">
          HR Admin
        </button>
      </div>
    </header>
  )
}
