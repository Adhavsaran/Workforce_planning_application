import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000',
  timeout: 15000,
})

export const getHealth = () => api.get('/health')
export const getDashboardSummary = () => api.get('/api/analytics/summary')
export const getWorkforceGap = () => api.get('/api/workforce-gap')
export const getAttritionSummary = () => api.get('/api/attrition')
export const getRecommendations = () => api.get('/api/recommendations')
export const getWorkforceHistory = (params = {}) => api.get('/api/workforce-history', { params })
export const importWorkforceHistory = (file) => {
  const formData = new FormData()
  formData.append('file', file)
  return api.post('/api/workforce-history/import', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

export const getEmployees = (params = {}) => api.get('/api/employees', { params })
export const getEmployee = (employeeId) => api.get(`/api/employees/${employeeId}`)
export const createEmployee = (payload) => api.post('/api/employees', payload)
export const updateEmployee = (employeeId, payload) => api.put(`/api/employees/${employeeId}`, payload)
export const deleteEmployee = (employeeId) => api.delete(`/api/employees/${employeeId}`)
export const importEmployees = (file) => {
  const formData = new FormData()
  formData.append('file', file)
  return api.post('/api/employees/import', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

export const getDepartments = () => api.get('/api/departments')
export const getDepartment = (id) => api.get(`/api/departments/${id}`)
export const createDepartment = (payload) => api.post('/api/departments', payload)
export const updateDepartment = (id, payload) => api.put(`/api/departments/${id}`, payload)
export const deleteDepartment = (id) => api.delete(`/api/departments/${id}`)
export const getDepartmentEmployees = (id) => api.get(`/api/departments/${id}/employees`)

export const generateForecast = (payload = {}) => api.post('/api/forecast', payload)
export const getForecasts = () => api.get('/api/forecast')
export const getDepartmentForecast = (departmentId) => api.get(`/api/forecast/${departmentId}`)

export default api
