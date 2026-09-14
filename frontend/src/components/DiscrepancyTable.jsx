import React, { useState } from 'react';

export default function DiscrepancyTable({ items }) {
  const [sortAsc, setSortAsc] = useState(true);

  if (!items || items.length === 0) {
    return <p>No discrepancies found for this filter/tenant combination.</p>;
  }

  const sortedItems = [...items].sort((a, b) => {
    const valA = parseFloat(a.val_a || a.val_b || 0);
    const valB = parseFloat(b.val_a || b.val_b || 0);
    return sortAsc ? valA - valB : valB - valA;
  });

  return (
    <div>
      <button onClick={() => setSortAsc(!sortAsc)} style={{ marginBottom: '1rem' }}>
        Sort by Value ({sortAsc ? 'Ascending' : 'Descending'})
      </button>
      
      <table border="1" cellPadding="8" style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
        <thead style={{ backgroundColor: '#f0f0f0' }}>
          <tr>
            <th>Reason</th>
            <th>Record ID / Ref</th>
            <th>Location</th>
            <th>Org</th>
            <th>System A Value</th>
            <th>System B Value</th>
          </tr>
        </thead>
        <tbody>
          {sortedItems.map((row, idx) => (
            <tr key={idx}>
              <td><strong>{row.reason}</strong></td>
              <td>{row.record_id}</td>
              <td>{row.location_id}</td>
              <td>{row.org_id}</td>
              <td>{row.val_a ?? '—'}</td>
              <td>{row.val_b ?? '—'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}