import React, { useState } from 'react'

export default function Upload({ onUploaded }: { onUploaded?: () => void }) {
  const [file, setFile] = useState<File | null>(null)
  const [busy, setBusy] = useState(false)
  const [entities, setEntities] = useState<{label: string, text: string}[]>([])

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!file) return
    setBusy(true)
    const fd = new FormData()
    fd.append('file', file)
    const res = await fetch('/api/upload_doc', { method: 'POST', body: fd })
    const js = await res.json()
    setEntities(js.entities || [])
    setBusy(false)
    onUploaded?.()
  }

  return (
    <section>
      <h2>Upload KYC Document</h2>
      <form onSubmit={onSubmit}>
        <input type="file" accept=".png,.jpg,.jpeg,.pdf" onChange={e => setFile(e.target.files?.[0] || null)} />
        <button disabled={!file || busy} style={{ marginLeft: 12 }}>{busy ? 'Processing...' : 'Upload'}</button>
      </form>
      {entities.length > 0 && (
        <div style={{ marginTop: 12 }}>
          <strong>Extracted Entities:</strong>
          <ul>
            {entities.map((e, i) => <li key={i}><code>{e.label}</code> — {e.text}</li>)}
          </ul>
        </div>
      )}
    </section>
  )
}
