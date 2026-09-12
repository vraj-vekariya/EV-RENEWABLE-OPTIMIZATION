import React from 'react';

const AlternativeOptions = ({ options }) => {
  if (!options || options.length === 0) return null;

  return (
    <div className="glass-panel" style={{ padding: '1.5rem' }}>
      <h3 style={{ marginTop: 0 }}>Alternative Feasible Options</h3>
      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '1rem' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.1)', color: '#94a3b8', textAlign: 'left' }}>
              <th style={{ padding: '10px' }}>Station</th>
              <th style={{ padding: '10px' }}>Time</th>
              <th style={{ padding: '10px' }}>Score</th>
              <th style={{ padding: '10px' }}>Cost</th>
              <th style={{ padding: '10px' }}>Renewable</th>
            </tr>
          </thead>
          <tbody>
            {options.map((opt, i) => (
              <tr key={i} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                <td style={{ padding: '12px 10px', fontWeight: '500' }}>{opt.station_name}</td>
                <td style={{ padding: '12px 10px' }}>{new Date(opt.start_time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</td>
                <td style={{ padding: '12px 10px', color: '#00ff88', fontWeight: 'bold' }}>{opt.green_charging_score.toFixed(1)}</td>
                <td style={{ padding: '12px 10px' }}>₹{opt.estimated_cost.toFixed(2)}</td>
                <td style={{ padding: '12px 10px' }}>{opt.renewable_percentage.toFixed(1)}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default AlternativeOptions;
