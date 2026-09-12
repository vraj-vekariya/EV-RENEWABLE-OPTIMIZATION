import React from 'react';

const RecommendationCard = ({ option }) => {
  if (!option) return null;

  const startTime = new Date(option.start_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  const endTime = new Date(option.end_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  return (
    <div className="glass-panel" style={{ padding: '2rem', border: '1px solid #00ff88' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <h2 style={{ color: '#00ff88', marginTop: 0 }}>Top Recommendation</h2>
          <h3 style={{ fontSize: '1.5rem', margin: '0.5rem 0' }}>{option.station_name}</h3>
          <p style={{ color: '#94a3b8' }}>{startTime} - {endTime}</p>
        </div>
        <div style={{ textAlign: 'right' }}>
          <div style={{ fontSize: '2.5rem', fontWeight: 'bold', color: '#00ff88' }}>
            {option.green_charging_score.toFixed(1)}<span style={{ fontSize: '1rem', color: '#94a3b8' }}>/100</span>
          </div>
          <div style={{ fontSize: '0.9rem', color: '#94a3b8' }}>Green Score</div>
        </div>
      </div>
      
      <div style={{ margin: '1.5rem 0', padding: '1rem', background: 'rgba(0,255,136,0.1)', borderRadius: '8px', borderLeft: '4px solid #00ff88' }}>
        <i>{option.explanation}</i>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '1rem' }}>
        <div style={boxStyle}>
          <div style={labelStyle}>Renewables</div>
          <div style={valStyle}>{option.renewable_percentage.toFixed(1)}%</div>
        </div>
        <div style={boxStyle}>
          <div style={labelStyle}>Est. Cost</div>
          <div style={valStyle}>₹{option.estimated_cost.toFixed(2)}</div>
        </div>
        <div style={boxStyle}>
          <div style={labelStyle}>CO2 Saved</div>
          <div style={{...valStyle, color: option.co2_saved_g >= 0 ? '#00ff88' : '#ff6b6b' }}>
            {option.co2_saved_g > 0 ? '+' : ''}{(option.co2_saved_g / 1000).toFixed(2)} kg
          </div>
        </div>
        <div style={boxStyle}>
          <div style={labelStyle}>Distance</div>
          <div style={valStyle}>{option.travel_distance_km.toFixed(1)} km</div>
        </div>
      </div>
    </div>
  );
};

const boxStyle = {
  background: 'rgba(255,255,255,0.05)',
  padding: '1rem',
  borderRadius: '8px'
};

const labelStyle = {
  fontSize: '0.85rem',
  color: '#94a3b8',
  marginBottom: '0.5rem'
};

const valStyle = {
  fontSize: '1.25rem',
  fontWeight: '600'
};

export default RecommendationCard;
