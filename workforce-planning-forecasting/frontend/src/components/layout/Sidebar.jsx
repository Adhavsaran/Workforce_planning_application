import { NavLink } from 'react-router-dom'

const navItems = [
  { label: 'Dashboard', path: '/' },
  { label: 'Employees', path: '/employees' },
  { label: 'Departments', path: '/departments' },
  { label: 'Analytics', path: '/analytics' },
  { label: 'Forecasting', path: '/forecasting' },
  { label: 'Attrition', path: '/attrition' },
  { label: 'Workforce Gap', path: '/workforce-gap' },
  { label: 'Recommendations', path: '/recommendations' },
]

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="brand-block">
        <div className="brand-mark">WF</div>
        <div>
          <p className="eyebrow">HR Analytics</p>
          <h2>Workforce Planner</h2>
        </div>
      </div>

      <nav className="nav-menu">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            end={item.path === '/'}
            className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}
          >
            {item.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  )
}
