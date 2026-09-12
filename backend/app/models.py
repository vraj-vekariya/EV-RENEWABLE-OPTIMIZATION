from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database import Base

class Station(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    base_price_per_kwh = Column(Float)
    plug_power_kw = Column(Float)
    available_plugs = Column(Integer)

class GridCondition(Base):
    __tablename__ = "grid_conditions"

    id = Column(Integer, primary_key=True, index=True)
    time_slot = Column(DateTime, index=True)
    renewable_percentage = Column(Float)
    carbon_intensity_g_kwh = Column(Float)
    price_multiplier = Column(Float)
