import React from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline, useMapEvents } from 'react-leaflet';
import L from 'leaflet';

// Fix Leaflet's default icon path issues
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
});

const LocationMarker = ({ position, setPosition }) => {
  useMapEvents({
    click(e) {
      setPosition([e.latlng.lat, e.latlng.lng]);
    },
  });
  return position ? (
    <Marker position={position}>
      <Popup>Your Location</Popup>
    </Marker>
  ) : null;
};

const MapComponent = ({ userLocation, setUserLocation, stations, recommendedStationId }) => {
  const defaultCenter = [52.5200, 13.4050];

  const recommendedStation = stations.find(s => s.id === recommendedStationId);

  return (
    <div style={{ height: '300px', width: '100%', borderRadius: '12px', overflow: 'hidden' }}>
      <MapContainer center={defaultCenter} zoom={12} style={{ height: '100%', width: '100%' }}>
        <TileLayer
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
          attribution='&copy; CARTO'
        />
        
        <LocationMarker position={userLocation} setPosition={setUserLocation} />
        
        {stations.map(station => (
          <Marker key={station.id} position={[station.latitude, station.longitude]} opacity={station.id === recommendedStationId ? 1 : 0.6}>
            <Popup>
              <strong>{station.name}</strong><br/>
              {station.plug_power_kw}kW | ₹{station.base_price_per_kwh}/kWh
            </Popup>
          </Marker>
        ))}

        {userLocation && recommendedStation && (
          <Polyline 
            positions={[userLocation, [recommendedStation.latitude, recommendedStation.longitude]]} 
            color="#00ff88" 
            dashArray="5, 10" 
            weight={3}
          />
        )}
      </MapContainer>
    </div>
  );
};

export default MapComponent;
