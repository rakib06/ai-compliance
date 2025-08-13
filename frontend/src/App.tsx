import React, { useState } from 'react'
import Upload from './components/Upload'
import Cases from './components/Cases'

export default function App() {
  const [refresh, setRefresh] = useState(0)
  return (
    <main style={{ fontFamily: 'sans-serif', padding: 24, maxWidth: 960, margin: '0 auto' }}>
      <h1>AI Compliance Dashboard</h1>
      <Upload onUploaded={() => setRefresh((r) => r + 1)} />
      <hr style={{ margin: '24px 0' }} />
      <Cases refreshKey={refresh} />
    </main>
  )
}
