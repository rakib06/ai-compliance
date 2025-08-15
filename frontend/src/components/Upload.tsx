import React, { useState } from 'react'
import { Box, Button, List, ListItem, ListItemText, Typography } from '@mui/material'

export default function Upload({ onUploaded }: { onUploaded?: () => void }) {
  const [file, setFile] = useState<File | null>(null)
  const [busy, setBusy] = useState(false)
  const [entities, setEntities] = useState<{ label: string, text: string }[]>([])

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
    <Box>
      <Typography variant="h5" gutterBottom>Upload KYC Document</Typography>
      <Box component="form" onSubmit={onSubmit} sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
        <input type="file" accept=".png,.jpg,.jpeg,.pdf" onChange={e => setFile(e.target.files?.[0] || null)} />
        <Button type="submit" variant="contained" disabled={!file || busy}>{busy ? 'Processing...' : 'Upload'}</Button>
      </Box>
      {entities.length > 0 && (
        <Box mt={2}>
          <Typography variant="subtitle1">Extracted Entities:</Typography>
          <List dense>
            {entities.map((e, i) => (
              <ListItem key={i} disablePadding>
                <ListItemText primary={`${e.label} — ${e.text}`} />
              </ListItem>
            ))}
          </List>
        </Box>
      )}
    </Box>
  )
}
