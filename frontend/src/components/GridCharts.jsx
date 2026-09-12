import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const GridCharts = ({ data }) => {
  if (!data || data.length === 0) return null;

  const chartData = data.map(d => {
    const time = new Date(d.time_slot);
    return {
      time: time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      Renewable: d.renewable_percentage,
      Carbon: d.carbon_intensity_g_kwh,
      PriceMult: d.price_multiplier,
    };
  });

  return (
    <div className="glass-panel" style={{ padding: '1.5rem' }}>
      <h3 style={{ marginTop: 0 }}>Grid Conditions Forecast (Renewables)</h3>
      <div style={{ height: '250px', width: '100%', marginTop: '1rem' }}>
        <ResponsiveContainer>
          <AreaChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
            <defs>
              <linearGradient id="colorRen" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#00ff88" stopOpacity={0.8}/>
                <stop offset="95%" stopColor="#00ff88" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <XAxis dataKey="time" stroke="#94a3b8" />
            <YAxis stroke="#94a3b8" />
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
            <Tooltip 
              contentStyle={{ backgroundColor: '#0a0e17', borderColor: 'rgba(255,255,255,0.1)', color: '#fff' }}
              itemStyle={{ color: '#00ff88' }}
            />
            <Area type="monotone" dataKey="Renewable" stroke="#00ff88" fillOpacity={1} fill="url(#colorRen)" name="Renewable %" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default GridCharts;
