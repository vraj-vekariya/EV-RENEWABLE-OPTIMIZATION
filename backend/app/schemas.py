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
