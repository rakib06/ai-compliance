import React, { useEffect, useState } from 'react'
import { Box, Button, Table, TableBody, TableCell, TableHead, TableRow, Typography } from '@mui/material'

type CaseRow = {
  case_id: number
  tx_id: number
  customer_id: string
  amount: number
  currency: string
  country: string
  description: string
  reason: string
  semantic_score: number
}

export default function Cases({ refreshKey }: { refreshKey: number }) {
  const [rows, setRows] = useState<CaseRow[]>([])

  const fetchCases = async () => {
    const res = await fetch('/api/cases')
    const js = await res.json()
    setRows(js.cases || [])
  }

  useEffect(() => {
    fetchCases()
  }, [refreshKey])

  const seedTx = async () => {
    await fetch('/api/transactions/ingest', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify([
        { customer_id: 'C001', amount: 15000, currency: 'USD', country: 'US', description: 'series of cash deposits near threshold' },
        { customer_id: 'C002', amount: 2500, currency: 'USD', country: 'IR', description: 'wire transfer to overseas partner' },
        { customer_id: 'C003', amount: 500, currency: 'USD', country: 'BD', description: 'regular utility payment' }
      ])
    })
    alert('Seeded 3 transactions. Now run the Airflow DAG or call the batch job.')
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
        <Typography variant="h5" sx={{ flexGrow: 1 }}>Flagged Cases</Typography>
        <Button onClick={fetchCases} variant="outlined">Refresh</Button>
        <Button onClick={seedTx} variant="outlined">Seed Sample Transactions</Button>
      </Box>
      <Table sx={{ mt: 2 }}>
        <TableHead>
          <TableRow>
            <TableCell>Case</TableCell>
            <TableCell>Tx</TableCell>
            <TableCell>Customer</TableCell>
            <TableCell align="right">Amount</TableCell>
            <TableCell>Country</TableCell>
            <TableCell>Reason</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((r) => (
            <TableRow key={r.case_id}>
              <TableCell>#{r.case_id}</TableCell>
              <TableCell>#{r.tx_id}</TableCell>
              <TableCell>{r.customer_id}</TableCell>
              <TableCell align="right">{r.amount.toLocaleString()} {r.currency}</TableCell>
              <TableCell>{r.country}</TableCell>
              <TableCell>{r.reason}</TableCell>
            </TableRow>
          ))}
          {rows.length === 0 && (
            <TableRow>
              <TableCell colSpan={6} sx={{ p: 2, opacity: 0.7 }}>
                No cases yet. Seed transactions and run the Airflow DAG.
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </Box>
  )
}
