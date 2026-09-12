import os
import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Use the same database URL as in the app
SQLALCHEMY_DATABASE_URL = "sqlite:///../data/charging_network.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.models import Base, Station, GridCondition

def generate_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Clear existing data
    db.query(Station).delete()
    db.query(GridCondition).delete()

    # Deterministic generation
    random.seed(42)

    # Configurable simulation start time (we will use this for the grid conditions)
    # Using 2026-09-12 12:00:00 as a fixed reproducible start time for the hackathon
    simulation_start_time = datetime(2026, 9, 12, 12, 0, 0)
    
    # Generate Stations around a city center (e.g., Berlin)
    center_lat = 52.5200
    center_lon = 13.4050
    
    stations_data = [
        {"name": "Central Plaza Fast Chargers", "lat_offset": 0.01, "lon_offset": 0.01, "power": 150.0, "price": 0.45},
        {"name": "Mall of Berlin Supercharge", "lat_offset": -0.015, "lon_offset": 0.02, "power": 250.0, "price": 0.50},
        {"name": "Westside Eco Station", "lat_offset": 0.03, "lon_offset": -0.02, "power": 50.0, "price": 0.35},
        {"name": "East End Standard", "lat_offset": -0.02, "lon_offset": 0.04, "power": 22.0, "price": 0.30},
        {"name": "Highway Exit Ultra", "lat_offset": 0.05, "lon_offset": -0.05, "power": 350.0, "price": 0.55},
        {"name": "Tech Park Hub", "lat_offset": 0.02, "lon_offset": -0.04, "power": 100.0, "price": 0.40},
        {"name": "Airport Quick Charge", "lat_offset": -0.04, "lon_offset": -0.03, "power": 150.0, "price": 0.45},
    ]

    for sd in stations_data:
        station = Station(
            name=sd["name"],
            latitude=center_lat + sd["lat_offset"],
            longitude=center_lon + sd["lon_offset"],
            base_price_per_kwh=sd["price"],
            plug_power_kw=sd["power"],
            available_plugs=random.randint(1, 4)
        )
        db.add(station)

    # Generate 48 hours of grid conditions
    for hour_offset in range(48):
        slot_time = simulation_start_time + timedelta(hours=hour_offset)
        hour_of_day = slot_time.hour
        
        # Simulate Duck Curve: High renewables midday (10-15)
        if 10 <= hour_of_day <= 15:
            renewable_pct = random.uniform(60, 95)
            price_mult = random.uniform(0.7, 0.9)
            carbon = random.uniform(50, 150)
        # Evening Peak (18-22)
        elif 18 <= hour_of_day <= 22:
            renewable_pct = random.uniform(10, 30)
            price_mult = random.uniform(1.2, 1.6)
            carbon = random.uniform(300, 500)
        # Night/Morning
        else:
            renewable_pct = random.uniform(30, 50)
            price_mult = random.uniform(0.9, 1.1)
            carbon = random.uniform(150, 300)

        condition = GridCondition(
            time_slot=slot_time,
            renewable_percentage=round(renewable_pct, 1),
            carbon_intensity_g_kwh=round(carbon, 1),
            price_multiplier=round(price_mult, 2)
        )
        db.add(condition)

    db.commit()
    db.close()
    print("Simulated data successfully generated.")

if __name__ == "__main__":
    generate_data()
