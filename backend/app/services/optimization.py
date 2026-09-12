import math
from datetime import datetime, timedelta
from typing import List
from sqlalchemy.orm import Session
from app.models import Station, GridCondition
from app.schemas import UserRequest, ChargingOption, OptimizationResponse

# Constants
SPEED_KMH = 50.0
EV_EFFICIENCY_KWH_KM = 0.2

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0 # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def optimize_charging(db: Session, request: UserRequest) -> OptimizationResponse:
    # 1. Required charging energy
    charging_energy_kwh = request.battery_capacity_kwh * (request.target_battery_pct - request.current_battery_pct) / 100.0
    if charging_energy_kwh <= 0:
        return OptimizationResponse(options=[], message="Target battery is already reached.")
    
    current_battery_energy_kwh = request.battery_capacity_kwh * (request.current_battery_pct / 100.0)
    
    stations = db.query(Station).all()
    grid_conditions = db.query(GridCondition).filter(GridCondition.time_slot >= request.simulation_start_time).order_by(GridCondition.time_slot).all()
    
    raw_options = []
    
    for station in stations:
        # 2. Distance
        distance_km = haversine_distance(request.current_lat, request.current_lon, station.latitude, station.longitude)
        
        # 3. Travel time
        travel_time_hours = distance_km / SPEED_KMH
        
        # 4. Travel energy
        travel_energy_kwh = distance_km * EV_EFFICIENCY_KWH_KM
        
        # 5. Reject if unreachable
        if travel_energy_kwh > current_battery_energy_kwh:
            continue
            
        # 6. Charging duration
        charging_duration_hours = charging_energy_kwh / station.plug_power_kw
        
        arrival_time = request.simulation_start_time + timedelta(hours=travel_time_hours)
        
        # 7. Evaluate hourly time slots
        for gc in grid_conditions:
            start_time = max(arrival_time, gc.time_slot)
            end_time = start_time + timedelta(hours=charging_duration_hours)
            
            # 9. Must finish before deadline
            if end_time > request.departure_deadline:
                continue
                
            # If start_time is way past the grid condition time slot we don't start in this slot.
            if start_time >= gc.time_slot + timedelta(hours=1):
                continue
            
            # Average conditions for the duration [start_time, end_time]
            overlapping_gcs = [g for g in grid_conditions if g.time_slot < end_time and (g.time_slot + timedelta(hours=1)) > start_time]
            
            if not overlapping_gcs:
                continue
                
            avg_price_mult = sum(g.price_multiplier for g in overlapping_gcs) / len(overlapping_gcs)
            avg_carbon = sum(g.carbon_intensity_g_kwh for g in overlapping_gcs) / len(overlapping_gcs)
            avg_renewable = sum(g.renewable_percentage for g in overlapping_gcs) / len(overlapping_gcs)
            
            # 10. Estimated cost
            estimated_cost = charging_energy_kwh * station.base_price_per_kwh * avg_price_mult
            
            # 11. CO2
            co2_impact_g = charging_energy_kwh * avg_carbon
            
            # Total time spent from simulation start to end of charging
            total_time_spent = (end_time - request.simulation_start_time).total_seconds() / 3600.0
            
            raw_options.append({
                "station": station,
                "start_time": start_time,
                "end_time": end_time,
                "travel_distance_km": distance_km,
                "travel_time_hours": travel_time_hours,
                "travel_energy_kwh": travel_energy_kwh,
                "charging_energy_kwh": charging_energy_kwh,
                "estimated_cost": estimated_cost,
                "co2_impact_g": co2_impact_g,
                "renewable_percentage": avg_renewable,
                "total_time_spent": total_time_spent
            })

    if not raw_options:
        return OptimizationResponse(options=[], message="No feasible charging options found that meet your deadline and battery constraints.")

    # Find MAX values for normalization
    MAX_POSSIBLE_COST = max((opt["estimated_cost"] for opt in raw_options), default=1)
    if MAX_POSSIBLE_COST == 0: MAX_POSSIBLE_COST = 1
    
    MAX_TOLERABLE_TIME = max((opt["total_time_spent"] for opt in raw_options), default=1)
    if MAX_TOLERABLE_TIME == 0: MAX_TOLERABLE_TIME = 1
    
    MAX_POSSIBLE_CO2 = max((opt["co2_impact_g"] for opt in raw_options), default=1)
    if MAX_POSSIBLE_CO2 == 0: MAX_POSSIBLE_CO2 = 1

    # Baseline CO2 for earliest feasible option
    earliest_opt = min(raw_options, key=lambda x: x["end_time"])
    baseline_co2 = earliest_opt["co2_impact_g"]

    options: List[ChargingOption] = []
    
    for opt in raw_options:
        # Normalize
        norm_renewable = max(0.0, min(1.0, opt["renewable_percentage"] / 100.0))
        norm_cost = max(0.0, min(1.0, 1.0 - (opt["estimated_cost"] / MAX_POSSIBLE_COST)))
        norm_convenience = max(0.0, min(1.0, 1.0 - (opt["total_time_spent"] / MAX_TOLERABLE_TIME)))
        norm_co2 = max(0.0, min(1.0, 1.0 - (opt["co2_impact_g"] / MAX_POSSIBLE_CO2)))
        
        score = (norm_renewable * 50) + (norm_cost * 25) + (norm_convenience * 15) + (norm_co2 * 10)
        
        co2_saved_g = baseline_co2 - opt["co2_impact_g"]
        
        # Explanation logic
        components = {
            "renewable availability": norm_renewable,
            "charging cost": norm_cost,
            "convenience": norm_convenience,
            "CO2 reduction": norm_co2
        }
        best_feature = max(components.items(), key=lambda x: x[1])[0]
        
        explanation = f"Recommended because it provides exceptional {best_feature}, yielding a Green Score of {score:.1f}/100."
        
        options.append(ChargingOption(
            station_id=opt["station"].id,
            station_name=opt["station"].name,
            start_time=opt["start_time"],
            end_time=opt["end_time"],
            travel_distance_km=opt["travel_distance_km"],
            travel_time_hours=opt["travel_time_hours"],
            travel_energy_kwh=opt["travel_energy_kwh"],
            charging_energy_kwh=opt["charging_energy_kwh"],
            estimated_cost=opt["estimated_cost"],
            co2_impact_g=opt["co2_impact_g"],
            co2_saved_g=co2_saved_g,
            renewable_percentage=opt["renewable_percentage"],
            green_charging_score=score,
            explanation=explanation
        ))
        
    # Sort descending
    options.sort(key=lambda x: x.green_charging_score, reverse=True)
    
    return OptimizationResponse(options=options)
