import { useEffect, useState } from 'react'

const emptyForm = { name: '', description: '' }

export default function DepartmentForm({ initialData = null, onSubmit, onCancel, submitLabel = 'Save Department' }) {
  const [form, setForm] = useState(emptyForm)

  useEffect(() => {
    if (initialData) {
      setForm({
        name: initialData.name || '',
        description: initialData.description || '',
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
    onSubmit(form)
  }

  return (
    <form className="form-card" onSubmit={handleSubmit}>
      <div className="form-grid single-column">
        <label>
          Department Name
          <input name="name" value={form.name} onChange={handleChange} required />
        </label>
        <label>
          Description
          <textarea name="description" value={form.description} onChange={handleChange} rows="3" />
        </label>
      </div>

      <div className="form-actions">
        <button type="button" className="ghost-button" onClick={onCancel}>Cancel</button>
        <button type="submit" className="primary-button">{submitLabel}</button>
      </div>
    </form>
  )
}
