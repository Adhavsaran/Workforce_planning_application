import { useEffect, useState } from 'react'

const emptyForm = {
  employee_id: '',
  name: '',
  department_id: '',
  job_role: '',
  age: '',
  gender: 'M',
  experience_years: '',
  joining_date: '',
  salary: '',
  performance_score: '',
  satisfaction_score: '',
  employment_type: 'FULL_TIME',
  location: '',
  attrition_status: 'ACTIVE',
}

export default function EmployeeForm({ departments = [], initialData = null, onSubmit, onCancel, submitLabel = 'Save Employee' }) {
  const [form, setForm] = useState(emptyForm)

  useEffect(() => {
    if (initialData) {
      setForm({
        employee_id: initialData.employee_id || '',
        name: initialData.name || '',
        department_id: initialData.department?.id || initialData.department_id || '',
        job_role: initialData.job_role || '',
        age: initialData.age ?? '',
        gender: initialData.gender || 'M',
        experience_years: initialData.experience_years ?? '',
        joining_date: initialData.joining_date || '',
        salary: initialData.salary ?? '',
        performance_score: initialData.performance_score ?? '',
        satisfaction_score: initialData.satisfaction_score ?? '',
        employment_type: initialData.employment_type || 'FULL_TIME',
        location: initialData.location || '',
        attrition_status: initialData.attrition_status || 'ACTIVE',
      })
    } else {
      setForm(emptyForm)
    }
  }, [initialData])

  const handleChange = (event) => {
    const { name, value } = event.target
    setForm((current) => ({ ...current, [name]: value }))
  }

  const handleSubmit = (event) => {
    event.preventDefault()
    onSubmit({ ...form, department_id: Number(form.department_id) })
  }

  return (
    <form className="form-card" onSubmit={handleSubmit}>
      <div className="form-grid">
        <label>
          Employee ID
          <input name="employee_id" value={form.employee_id} onChange={handleChange} required />
        </label>
        <label>
          Name
          <input name="name" value={form.name} onChange={handleChange} required />
        </label>
        <label>
          Department
          <select name="department_id" value={form.department_id} onChange={handleChange} required>
            <option value="">Select department</option>
            {departments.map((department) => (
              <option key={department.id} value={department.id}>
                {department.name}
              </option>
            ))}
          </select>
        </label>
        <label>
          Job Role
          <input name="job_role" value={form.job_role} onChange={handleChange} required />
        </label>
        <label>
          Age
          <input name="age" type="number" min="18" max="100" value={form.age} onChange={handleChange} required />
        </label>
        <label>
          Gender
          <select name="gender" value={form.gender} onChange={handleChange}>
            <option value="M">M</option>
            <option value="F">F</option>
            <option value="OTHER">OTHER</option>
          </select>
        </label>
        <label>
          Experience (Years)
          <input name="experience_years" type="number" step="0.1" min="0" value={form.experience_years} onChange={handleChange} required />
        </label>
        <label>
          Joining Date
          <input name="joining_date" type="date" value={form.joining_date} onChange={handleChange} required />
        </label>
        <label>
          Salary
          <input name="salary" type="number" min="0" value={form.salary} onChange={handleChange} required />
        </label>
        <label>
          Performance Score
          <input name="performance_score" type="number" min="0" max="100" value={form.performance_score} onChange={handleChange} required />
        </label>
        <label>
          Satisfaction Score
          <input name="satisfaction_score" type="number" step="0.1" min="0" max="10" value={form.satisfaction_score} onChange={handleChange} required />
        </label>
        <label>
          Employment Type
          <select name="employment_type" value={form.employment_type} onChange={handleChange}>
            <option value="FULL_TIME">FULL_TIME</option>
            <option value="PART_TIME">PART_TIME</option>
            <option value="CONTRACT">CONTRACT</option>
            <option value="INTERN">INTERN</option>
          </select>
        </label>
        <label>
          Location
          <input name="location" value={form.location} onChange={handleChange} required />
        </label>
        <label>
          Attrition Status
          <select name="attrition_status" value={form.attrition_status} onChange={handleChange}>
            <option value="ACTIVE">ACTIVE</option>
            <option value="LEFT">LEFT</option>
          </select>
        </label>
      </div>

      <div className="form-actions">
        <button type="button" className="ghost-button" onClick={onCancel}>Cancel</button>
        <button type="submit" className="primary-button">{submitLabel}</button>
      </div>
    </form>
  )
}
