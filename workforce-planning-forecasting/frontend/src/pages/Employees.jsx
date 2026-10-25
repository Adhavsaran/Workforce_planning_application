import { useEffect, useMemo, useState } from 'react'
import { getDepartments, getEmployees, createEmployee, updateEmployee, deleteEmployee, importEmployees } from '../services/api'
import EmployeeForm from '../components/employees/EmployeeForm'
import CSVImportPanel from '../components/employees/CSVImportPanel'
import StatusBadge from '../components/common/StatusBadge'

const defaultFilters = {
  search: '',
  department_id: '',
  employment_type: '',
  attrition_status: '',
}

export default function EmployeesPage() {
  const [employees, setEmployees] = useState([])
  const [departments, setDepartments] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [page, setPage] = useState(1)
  const [pageSize, setPageSize] = useState(10)
  const [totalPages, setTotalPages] = useState(1)
  const [totalItems, setTotalItems] = useState(0)
  const [filters, setFilters] = useState(defaultFilters)
  const [editingEmployee, setEditingEmployee] = useState(null)
  const [showForm, setShowForm] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [importing, setImporting] = useState(false)
  const [importSummary, setImportSummary] = useState(null)

  const fetchDepartments = async () => {
    const response = await getDepartments()
    setDepartments(response.data || [])
  }

  const fetchEmployees = async (nextPage = page, nextFilters = filters, nextPageSize = pageSize) => {
    try {
      setLoading(true)
      const params = {
        page: nextPage,
        page_size: nextPageSize,
        sort_by: 'name',
        sort_order: 'asc',
      }

      if (nextFilters.search) params.search = nextFilters.search
      if (nextFilters.department_id) params.department_id = Number(nextFilters.department_id)
      if (nextFilters.employment_type) params.employment_type = nextFilters.employment_type
      if (nextFilters.attrition_status) params.attrition_status = nextFilters.attrition_status

      const response = await getEmployees(params)
      const payload = response.data || {}
      setEmployees(payload.items || [])
      setTotalItems(payload.total || 0)
      setTotalPages(payload.total_pages || 1)
      setError('')
    } catch (err) {
      setError('Unable to load employees. Please check the backend connection.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchDepartments().catch(() => setError('Unable to load departments.'))
  }, [])

  useEffect(() => {
    fetchEmployees(page, filters, pageSize)
  }, [page, pageSize, filters])

  const handleFilterChange = (event) => {
    const { name, value } = event.target
    setFilters((current) => ({ ...current, [name]: value }))
    setPage(1)
  }

  const handleResetFilters = () => {
    setFilters(defaultFilters)
    setPage(1)
  }

  const handleSubmit = async (payload) => {
    try {
      setSubmitting(true)
      if (editingEmployee) {
        await updateEmployee(editingEmployee.employee_id, payload)
      } else {
        await createEmployee(payload)
      }
      setShowForm(false)
      setEditingEmployee(null)
      await fetchEmployees(1, filters, pageSize)
    } catch (err) {
      const message = err?.response?.data?.detail || 'Unable to save employee.'
      setError(message)
    } finally {
      setSubmitting(false)
    }
  }

  const handleEdit = async (employeeId) => {
    try {
      const response = await getEmployees({ page: 1, page_size: 1000 })
      const selected = (response.data.items || []).find((item) => item.employee_id === employeeId)
      if (selected) {
        setEditingEmployee(selected)
        setShowForm(true)
      }
    } catch (err) {
      setError('Unable to load employee details.')
    }
  }

  const handleDelete = async (employeeId) => {
    const confirmed = window.confirm(`Are you sure you want to delete employee ${employeeId}?`)
    if (!confirmed) return

    try {
      await deleteEmployee(employeeId)
      await fetchEmployees(page, filters, pageSize)
    } catch (err) {
      const message = err?.response?.data?.detail || 'Unable to delete employee.'
      setError(message)
    }
  }

  const handleImport = async (file) => {
    try {
      setImporting(true)
      const response = await importEmployees(file)
      setImportSummary(response.data)
      await fetchEmployees(1, filters, pageSize)
      setError('')
    } catch (err) {
      const payload = err?.response?.data
      setImportSummary(payload || { detail: 'Import failed' })
      setError(payload?.detail || 'CSV import failed.')
    } finally {
      setImporting(false)
    }
  }

  const employeeCountLabel = useMemo(() => `${totalItems} employee${totalItems === 1 ? '' : 's'}`, [totalItems])

  return (
    <div className="page-shell">
      <div className="toolbar-row">
        <div>
          <p className="eyebrow">Employee management</p>
          <h2>Employees</h2>
        </div>
        <button type="button" className="primary-button" onClick={() => { setEditingEmployee(null); setShowForm(true) }}>
          Add Employee
        </button>
      </div>

      <CSVImportPanel onImport={handleImport} loading={importing} />

      {showForm && (
        <div className="modal-overlay" onClick={() => { setShowForm(false); setEditingEmployee(null) }}>
          <div className="modal-card" onClick={(event) => event.stopPropagation()}>
            <div className="modal-header">
              <h3>{editingEmployee ? 'Edit Employee' : 'Add Employee'}</h3>
            </div>
            <EmployeeForm
              departments={departments}
              initialData={editingEmployee}
              onSubmit={handleSubmit}
              onCancel={() => { setShowForm(false); setEditingEmployee(null) }}
              submitLabel={editingEmployee ? 'Update Employee' : 'Create Employee'}
            />
          </div>
        </div>
      )}

      <div className="panel">
        <div className="panel-header">
          <h3>Employee Directory</h3>
          <span className="panel-tag">{employeeCountLabel}</span>
        </div>

        <div className="filter-grid">
          <input name="search" placeholder="Search by employee ID, name, or role" value={filters.search} onChange={handleFilterChange} />
          <select name="department_id" value={filters.department_id} onChange={handleFilterChange}>
            <option value="">All departments</option>
            {departments.map((department) => (
              <option key={department.id} value={department.id}>{department.name}</option>
            ))}
          </select>
          <select name="employment_type" value={filters.employment_type} onChange={handleFilterChange}>
            <option value="">All employment types</option>
            <option value="FULL_TIME">FULL_TIME</option>
            <option value="PART_TIME">PART_TIME</option>
            <option value="CONTRACT">CONTRACT</option>
            <option value="INTERN">INTERN</option>
          </select>
          <select name="attrition_status" value={filters.attrition_status} onChange={handleFilterChange}>
            <option value="">All statuses</option>
            <option value="ACTIVE">ACTIVE</option>
            <option value="LEFT">LEFT</option>
          </select>
          <button type="button" className="ghost-button" onClick={handleResetFilters}>Reset</button>
        </div>

        {error && <p className="error-text">{error}</p>}

        {loading ? (
          <p>Loading employees...</p>
        ) : employees.length === 0 ? (
          <p>No employees found.</p>
        ) : (
          <div className="table-wrap">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Employee ID</th>
                  <th>Name</th>
                  <th>Department</th>
                  <th>Job Role</th>
                  <th>Experience</th>
                  <th>Performance</th>
                  <th>Salary</th>
                  <th>Employment</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {employees.map((employee) => (
                  <tr key={employee.id}>
                    <td>{employee.employee_id}</td>
                    <td>{employee.name}</td>
                    <td>{employee.department?.name || '—'}</td>
                    <td>{employee.job_role}</td>
                    <td>{employee.experience_years}</td>
                    <td>{employee.performance_score}</td>
                    <td>₹{Number(employee.salary).toLocaleString()}</td>
                    <td>{employee.employment_type}</td>
                    <td><StatusBadge status={employee.attrition_status} /></td>
                    <td>
                      <div className="row-actions">
                        <button type="button" className="inline-button" onClick={() => handleEdit(employee.employee_id)}>Edit</button>
                        <button type="button" className="inline-button danger" onClick={() => handleDelete(employee.employee_id)}>Delete</button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        <div className="pagination-row">
          <button type="button" className="ghost-button" disabled={page <= 1} onClick={() => setPage((current) => current - 1)}>
            Previous
          </button>
          <span>Page {page} of {totalPages || 1}</span>
          <button type="button" className="ghost-button" disabled={page >= totalPages} onClick={() => setPage((current) => current + 1)}>
            Next
          </button>
          <select value={pageSize} onChange={(event) => { setPageSize(Number(event.target.value)); setPage(1) }}>
            <option value={10}>10</option>
            <option value={20}>20</option>
            <option value={50}>50</option>
          </select>
        </div>
      </div>

      {importSummary && (
        <div className="panel">
          <div className="panel-header">
            <h3>Import Summary</h3>
          </div>
          <div className="summary-grid">
            <div className="summary-box"><span>Total Rows</span><strong>{importSummary.total_rows ?? 0}</strong></div>
            <div className="summary-box"><span>Successfully Imported</span><strong>{importSummary.successfully_imported ?? 0}</strong></div>
            <div className="summary-box"><span>Skipped Rows</span><strong>{importSummary.skipped_rows ?? 0}</strong></div>
            <div className="summary-box"><span>Failed Rows</span><strong>{importSummary.failed_rows ?? 0}</strong></div>
          </div>
          {Array.isArray(importSummary.errors) && importSummary.errors.length > 0 && (
            <ul className="error-list">
              {importSummary.errors.map((errorText, index) => (
                <li key={`${errorText}-${index}`}>{errorText}</li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  )
}
