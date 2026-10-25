export default function StatusBadge({ status }) {
  const normalized = String(status || '').toUpperCase()
  const tone = normalized === 'ACTIVE' ? 'success' : normalized === 'LEFT' ? 'muted' : 'neutral'
  return <span className={`status-badge ${tone}`}>{normalized}</span>
}
