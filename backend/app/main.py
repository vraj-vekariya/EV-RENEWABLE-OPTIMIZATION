from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app import models, schemas
from typing import List

# Ensure tables are created
Base.metadata.create_all(bind=engine)

app = FastAPI(title="EV Charging Network API")

# Configure CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for the hackathon
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/stations", response_model=List[schemas.StationBase])
def get_stations(db: Session = Depends(get_db)):
    stations = db.query(models.Station).all()
    return stations

@app.get("/api/grid-conditions", response_model=List[schemas.GridConditionBase])
def get_grid_conditions(db: Session = Depends(get_db)):
    conditions = db.query(models.GridCondition).order_by(models.GridCondition.time_slot).all()
    return conditions

from app.services.optimization import optimize_charging

@app.post("/api/optimize", response_model=schemas.OptimizationResponse)
def optimize_route(request: schemas.UserRequest, db: Session = Depends(get_db)):
    return optimize_charging(db, request)
