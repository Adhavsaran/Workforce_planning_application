import { useRef, useState } from 'react'

export default function CSVImportPanel({ onImport, loading }) {
  const fileInputRef = useRef(null)
  const [selectedFile, setSelectedFile] = useState(null)

  const handleFileChange = (event) => {
    const nextFile = event.target.files?.[0] || null
    setSelectedFile(nextFile)
  }

  const handleSubmit = () => {
    if (!selectedFile) {
      return
    }
    onImport(selectedFile)
  }

  return (
    <div className="panel">
      <div className="panel-header">
        <h3>Import Employees</h3>
        <span className="panel-tag">CSV</span>
      </div>
      <div className="file-upload-box">
        <input
          ref={fileInputRef}
          type="file"
          accept=".csv"
          onChange={handleFileChange}
        />
        <div className="upload-actions">
          <button type="button" className="ghost-button" onClick={() => fileInputRef.current?.click()}>
            Choose CSV
          </button>
          <button type="button" className="primary-button" onClick={handleSubmit} disabled={!selectedFile || loading}>
            {loading ? 'Uploading...' : 'Upload'}
          </button>
        </div>
        {selectedFile ? <p className="helper-text">Selected file: {selectedFile.name}</p> : <p className="helper-text">No file selected</p>}
      </div>
    </div>
  )
}
