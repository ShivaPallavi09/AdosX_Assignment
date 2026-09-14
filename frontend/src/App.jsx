import React, { useState, useEffect } from 'react';
import DiscrepancyTable from './components/DiscrepancyTable';
import FilterBar from './components/FilterBar';

export default function App() {
  const [tenantOrg, setTenantOrg] = useState('ORG-1');
  const [reasonFilter, setReasonFilter] = useState('ALL');
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchDiscrepancies = async () => {
    if (!tenantOrg) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`http://localhost:8000/api/discrepancies/?org_id=${encodeURIComponent(tenantOrg)}&reason=${encodeURIComponent(reasonFilter)}`);
      
      if (!response.ok) {
        throw new Error(`Error: ${response.status} ${response.statusText}`);
      }
      
      const result = await response.json();
      setData(result.results || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDiscrepancies();
  }, [tenantOrg, reasonFilter]);

  return (
    <div>
      <h1>Discrepancy Dashboard</h1>
      
      <FilterBar 
        tenantOrg={tenantOrg}
        setTenantOrg={setTenantOrg}
        reasonFilter={reasonFilter}
        setReasonFilter={setReasonFilter}
        onRefresh={fetchDiscrepancies}
      />

      {loading && <p>Loading data...</p>}
      {error && <p style={{color: 'red'}}>Failed to load data: {error}</p>}
      
      {!loading && !error && (
        <DiscrepancyTable items={data} />
      )}
    </div>
  );
}