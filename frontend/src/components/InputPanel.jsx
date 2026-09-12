import React from 'react';
import MapComponent from './MapComponent';

const InputPanel = ({ 
  formData, 
  setFormData, 
  userLocation, 
  setUserLocation, 
  stations,
  recommendedStationId,
  onOptimize,
  isLoading
}) => {
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  return (
    <div className="glass-panel input-section">
      <h3 style={{ marginTop: 0 }}>Trip Parameters</h3>
      
      <div className="input-group">
        <label>Current Battery (%) : {formData.current_battery_pct}%</label>
        <input 
          type="range" 
          name="current_battery_pct" 
          min="1" max="100" 
          value={formData.current_battery_pct} 
          onChange={handleChange} 
        />
      </div>

      <div className="input-group">
        <label>Target Battery (%) : {formData.target_battery_pct}%</label>
        <input 
          type="range" 
          name="target_battery_pct" 
          min="1" max="100" 
          value={formData.target_battery_pct} 
          onChange={handleChange} 
        />
      </div>

      <div className="input-group">
        <label>Battery Capacity (kWh)</label>
        <input 
          type="number" 
          name="battery_capacity_kwh" 
          value={formData.battery_capacity_kwh} 
          onChange={handleChange} 
        />
      </div>

      <div className="input-group">
        <label>Departure Deadline</label>
        <input 
          type="datetime-local" 
          name="departure_deadline" 
          value={formData.departure_deadline} 
          onChange={handleChange} 
        />
      </div>

      <div className="input-group" style={{ marginTop: '1rem' }}>
        <label>Select Current Location (Click Map)</label>
        <MapComponent 
          userLocation={userLocation} 
          setUserLocation={setUserLocation} 
          stations={stations}
          recommendedStationId={recommendedStationId}
        />
      </div>

      <button 
        className="btn-primary" 
        onClick={onOptimize}
        disabled={isLoading || !userLocation}
        style={{ marginTop: '1rem' }}
      >
        {isLoading ? 'Optimizing...' : 'Find Smart Charging Plan'}
      </button>
    </div>
  );
};

export default InputPanel;
