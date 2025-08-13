import React, { useEffect, useState } from 'react'

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

  useEffect(() => { fetchCases() }, [refreshKey])

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
    <section>
      <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
        <h2 style={{ margin: 0 }}>Flagged Cases</h2>
        <button onClick={fetchCases}>Refresh</button>
        <button onClick={seedTx}>Seed Sample Transactions</button>
      </div>
      <table style={{ width: '100%', marginTop: 12, borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th style={{ textAlign: 'left', borderBottom: '1px solid #ddd' }}>Case</th>
            <th style={{ textAlign: 'left', borderBottom: '1px solid #ddd' }}>Tx</th>
            <th style={{ textAlign: 'left', borderBottom: '1px solid #ddd' }}>Customer</th>
            <th style={{ textAlign: 'right', borderBottom: '1px solid #ddd' }}>Amount</th>
            <th style={{ textAlign: 'left', borderBottom: '1px solid #ddd' }}>Country</th>
            <th style={{ textAlign: 'left', borderBottom: '1px solid #ddd' }}>Reason</th>
          </tr>
        </thead>
        <tbody>
          {rows.map(r => (
            <tr key={r.case_id}>
              <td>#{r.case_id}</td>
              <td>#{r.tx_id}</td>
              <td>{r.customer_id}</td>
              <td style={{ textAlign: 'right' }}>{r.amount.toLocaleString()} {r.currency}</td>
              <td>{r.country}</td>
              <td>{r.reason}</td>
            </tr>
          ))}
          {rows.length === 0 && (
            <tr><td colSpan={6} style={{ padding: 12, opacity: 0.7 }}>No cases yet. Seed transactions and run the Airflow DAG.</td></tr>
          )}
        </tbody>
      </table>
    </section>
  )
}
