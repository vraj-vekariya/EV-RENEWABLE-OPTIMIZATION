from pydantic import BaseModel
from datetime import datetime

class StationBase(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    base_price_per_kwh: float
    plug_power_kw: float
    available_plugs: int

    class Config:
        from_attributes = True

class GridConditionBase(BaseModel):
    id: int
    time_slot: datetime
    renewable_percentage: float
    carbon_intensity_g_kwh: float
    price_multiplier: float

    class Config:
        from_attributes = True

from typing import List, Optional

class UserRequest(BaseModel):
    current_battery_pct: float
    target_battery_pct: float
    battery_capacity_kwh: float
    departure_deadline: datetime
    current_lat: float
    current_lon: float
    simulation_start_time: datetime

class ChargingOption(BaseModel):
    station_id: int
    station_name: str
    start_time: datetime
    end_time: datetime
    travel_distance_km: float
    travel_time_hours: float
    travel_energy_kwh: float
    charging_energy_kwh: float
    estimated_cost: float
    co2_impact_g: float
    co2_saved_g: float
    renewable_percentage: float
    green_charging_score: float
    explanation: str

class OptimizationResponse(BaseModel):
    options: List[ChargingOption]
    message: Optional[str] = None
