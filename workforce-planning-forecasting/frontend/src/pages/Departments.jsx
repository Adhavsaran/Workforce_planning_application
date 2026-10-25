import { useEffect, useState } from 'react'
import DepartmentForm from '../components/departments/DepartmentForm'
import { createDepartment, deleteDepartment, getDepartmentEmployees, getDepartments, updateDepartment } from '../services/api'

export default function DepartmentsPage() {
  const [departments, setDepartments] = useState([])
  const [selectedDepartment, setSelectedDepartment] = useState(null)
  const [departmentEmployees, setDepartmentEmployees] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [editingDepartment, setEditingDepartment] = useState(null)

  const fetchDepartments = async () => {
    try {
      setLoading(true)
      const response = await getDepartments()
      setDepartments(response.data || [])
      setError('')
    } catch (err) {
      setError('Unable to load departments.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchDepartments()
  }, [])

  const loadDepartmentEmployees = async (departmentId) => {
    try {
      const response = await getDepartmentEmployees(departmentId)
      setDepartmentEmployees(response.data || [])
      const matched = departments.find((department) => department.id === departmentId)
      setSelectedDepartment(matched || null)
    } catch (err) {
      setError('Unable to load department employees.')
    }
  }

  const handleSubmit = async (payload) => {
    try {
      if (editingDepartment) {
        await updateDepartment(editingDepartment.id, payload)
      } else {
        await createDepartment(payload)
      }
      setShowForm(false)
      setEditingDepartment(null)
      await fetchDepartments()
    } catch (err) {
      const message = err?.response?.data?.detail || 'Unable to save department.'
      setError(message)
    }
  }

  const handleDelete = async (departmentId) => {
    const confirmed = window.confirm('Delete this department?')
    if (!confirmed) return

    try {
      await deleteDepartment(departmentId)
      await fetchDepartments()
      if (selectedDepartment && selectedDepartment.id === departmentId) {
        setSelectedDepartment(null)
        setDepartmentEmployees([])
      }
    } catch (err) {
      setError(err?.response?.data?.detail || 'Unable to delete department.')
    }
  }

  return (
    <div className="page-shell">
      <div className="toolbar-row">
        <div>
          <p className="eyebrow">Organization setup</p>
          <h2>Departments</h2>
        </div>
        <button type="button" className="primary-button" onClick={() => { setEditingDepartment(null); setShowForm(true) }}>
          Add Department
        </button>
      </div>

      {showForm && (
        <div className="modal-overlay" onClick={() => { setShowForm(false); setEditingDepartment(null) }}>
          <div className="modal-card" onClick={(event) => event.stopPropagation()}>
            <div className="modal-header">
              <h3>{editingDepartment ? 'Edit Department' : 'Add Department'}</h3>
            </div>
            <DepartmentForm
              initialData={editingDepartment}
              onSubmit={handleSubmit}
              onCancel={() => { setShowForm(false); setEditingDepartment(null) }}
              submitLabel={editingDepartment ? 'Update Department' : 'Create Department'}
            />
          </div>
        </div>
      )}

      <div className="panel-grid two-columns">
        <div className="panel">
          <div className="panel-header">
            <h3>Department List</h3>
            <span className="panel-tag">{departments.length}</span>
          </div>

          {error && <p className="error-text">{error}</p>}

          {loading ? (
            <p>Loading departments...</p>
          ) : departments.length === 0 ? (
            <p>No departments found.</p>
          ) : (
            <div className="department-list">
              {departments.map((department) => (
                <div key={department.id} className="department-card">
                  <div>
                    <h4>{department.name}</h4>
                    <p>{department.description || 'No description provided.'}</p>
                  </div>
                  <div className="department-meta">
                    <span>{(department.employee_count || 0)} employees</span>
                    <div className="row-actions">
                      <button type="button" className="inline-button" onClick={() => { setEditingDepartment(department); setShowForm(true) }}>Edit</button>
                      <button type="button" className="inline-button" onClick={() => loadDepartmentEmployees(department.id)}>View</button>
                      <button type="button" className="inline-button danger" onClick={() => handleDelete(department.id)}>Delete</button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="panel">
          <div className="panel-header">
            <h3>{selectedDepartment ? selectedDepartment.name : 'Department Employees'}</h3>
          </div>
          {selectedDepartment ? (
            <div>
              {departmentEmployees.length === 0 ? (
                <p>No employees assigned to this department.</p>
              ) : (
                <ul className="employee-list">
                  {departmentEmployees.map((employee) => (
                    <li key={employee.employee_id} className="employee-item">
                      <div>
                        <strong>{employee.name}</strong>
                        <span>{employee.job_role}</span>
                      </div>
                      <span>{employee.employment_type}</span>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          ) : (
            <p>Select a department to view employees.</p>
          )}
        </div>
      </div>
    </div>
  )
}
