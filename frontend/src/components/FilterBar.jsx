import React from 'react';

export default function FilterBar({ 
  tenantOrg, 
  setTenantOrg, 
  reasonFilter, 
  setReasonFilter, 
  onRefresh 
}) {
  return (
    <div className="controls" style={{ marginBottom: '1rem', padding: '1rem', background: '#f5f5f5', borderRadius: '4px' }}>
      <label style={{ marginRight: '1rem' }}>
        <strong>Tenant (Org ID): </strong>
        <input 
          type="text" 
          value={tenantOrg} 
          onChange={(e) => setTenantOrg(e.target.value)} 
          placeholder="e.g., ORG-1"
          style={{ padding: '0.5rem' }}
        />
      </label>

      <label style={{ marginRight: '1rem' }}>
        <strong>Filter by Reason: </strong>
        <select 
          value={reasonFilter} 
          onChange={(e) => setReasonFilter(e.target.value)}
          style={{ padding: '0.5rem' }}
        >
          <option value="ALL">All Discrepancies</option>
          <option value="MISSING_IN_SYSTEM_B">Missing in System B</option>
          <option value="ORPHAN_IN_SYSTEM_B">Orphan in System B</option>
          <option value="DUPLICATE_IN_SYSTEM_B">Duplicate in System B</option>
          <option value="VALUE_MISMATCH">Value Mismatch</option>
        </select>
      </label>
      
      <button onClick={onRefresh} style={{ padding: '0.5rem 1rem' }}>Refresh</button>
    </div>
  );
}