import React, { useState } from 'react'
import Upload from './components/Upload'
import Cases from './components/Cases'
import { Container, Divider, Typography } from '@mui/material'

export default function App() {
  const [refresh, setRefresh] = useState(0)
  return (
    <Container sx={{ py: 3 }}>
      <Typography variant="h4" component="h1" gutterBottom>AI Compliance Dashboard</Typography>
      <Upload onUploaded={() => setRefresh((r) => r + 1)} />
      <Divider sx={{ my: 3 }} />
      <Cases refreshKey={refresh} />
    </Container>
  )
}
