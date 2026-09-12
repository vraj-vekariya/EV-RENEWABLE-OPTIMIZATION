import React, { useState, useEffect } from 'react';
import './App.css';
import { fetchStations, fetchGridConditions, optimizeCharging } from './services/api';
import InputPanel from './components/InputPanel';
import RecommendationCard from './components/RecommendationCard';
import AlternativeOptions from './components/AlternativeOptions';
import GridCharts from './components/GridCharts';

function App() {
  const [stations, setStations] = useState([]);
  const [gridData, setGridData] = useState([]);
  
  const [formData, setFormData] = useState({
    current_battery_pct: 20,
    target_battery_pct: 80,
    battery_capacity_kwh: 60,
    departure_deadline: '2026-09-12T18:00',
    simulation_start_time: '2026-09-12T12:00:00'
  });
  const [userLocation, setUserLocation] = useState(null);
  
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchStations().then(setStations).catch(console.error);
    fetchGridConditions().then(setGridData).catch(console.error);
  }, []);

  const handleOptimize = async () => {
    if (!userLocation) return;
    
    setIsLoading(true);
    setError(null);
    setResults(null);
    
    try {
      const payload = {
        ...formData,
        current_battery_pct: parseFloat(formData.current_battery_pct),
        target_battery_pct: parseFloat(formData.target_battery_pct),
        battery_capacity_kwh: parseFloat(formData.battery_capacity_kwh),
        departure_deadline: formData.departure_deadline,
        simulation_start_time: formData.simulation_start_time,
        current_lat: userLocation[0],
        current_lon: userLocation[1]
      };
      
      const response = await optimizeCharging(payload);
      setResults(response);
    } catch (err) {
      console.error(err);
      setError("Failed to communicate with optimization engine.");
    } finally {
      setIsLoading(false);
    }
  };

  const topOption = results?.options?.[0];
  const alternatives = results?.options?.slice(1, 5);

  return (
    <div className="app-container">
      <header className="header">
        <h1>EV Renewable Optimization</h1>
        <p>Charge at the smartest time.</p>
      </header>
      
      <main className="main-grid">
        <aside>
          <InputPanel 
            formData={formData} 
            setFormData={setFormData} 
            userLocation={userLocation} 
            setUserLocation={setUserLocation} 
            stations={stations}
            recommendedStationId={topOption?.station_id}
            onOptimize={handleOptimize}
            isLoading={isLoading}
          />
        </aside>
        
        <section className="results-section">
          {error && <div className="error-message">{error}</div>}
          
          {isLoading && (
            <div className="loading-state">
              <div className="spinner"></div>
              <div>Calculating optimal routes...</div>
            </div>
          )}
          
          {!isLoading && results && results.options.length === 0 && (
            <div className="glass-panel" style={{ padding: '2rem', textAlign: 'center' }}>
              <h3 style={{ color: '#ff6b6b' }}>No Feasible Options</h3>
              <p>{results.message || "We couldn't find any charging options that meet your criteria."}</p>
            </div>
          )}

          {!isLoading && topOption && (
            <>
              <RecommendationCard option={topOption} />
              <GridCharts data={gridData} />
              {alternatives && alternatives.length > 0 && (
                <AlternativeOptions options={alternatives} />
              )}
            </>
          )}
          
          {!isLoading && !results && !error && (
            <div className="glass-panel" style={{ padding: '4rem 2rem', textAlign: 'center', color: 'var(--text-muted)' }}>
              <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>⚡</div>
              <h3>Ready to Optimize</h3>
              <p>Set your location on the map and click find to discover the smartest charging window.</p>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
