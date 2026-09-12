import pytest
from datetime import datetime, timedelta
from app.schemas import UserRequest
from app.services.optimization import optimize_charging
from app.models import Station, GridCondition

class MockQuery:
    def __init__(self, data):
        self.data = data
    def all(self):
        return self.data
    def filter(self, *args, **kwargs):
        return self
    def order_by(self, *args, **kwargs):
        return self

class MockSession:
    def __init__(self, stations, grid_conditions):
        self.stations = stations
        self.grid_conditions = grid_conditions
    def query(self, model):
        if model == Station:
            return MockQuery(self.stations)
        if model == GridCondition:
            return MockQuery(self.grid_conditions)

@pytest.fixture
def mock_db():
    start_time = datetime(2026, 9, 12, 12, 0)
    stations = [
        Station(id=1, name="Station A", latitude=52.51, longitude=13.41, base_price_per_kwh=0.5, plug_power_kw=150.0, available_plugs=2),
        Station(id=2, name="Station B (Far)", latitude=53.51, longitude=14.41, base_price_per_kwh=0.5, plug_power_kw=150.0, available_plugs=2),
    ]
    gcs = [
        GridCondition(id=1, time_slot=start_time, renewable_percentage=80, carbon_intensity_g_kwh=100, price_multiplier=1.0),
        GridCondition(id=2, time_slot=start_time + timedelta(hours=1), renewable_percentage=90, carbon_intensity_g_kwh=50, price_multiplier=0.8),
    ]
    return MockSession(stations, gcs)

@pytest.fixture
def base_request():
    return UserRequest(
        current_battery_pct=20.0,
        target_battery_pct=80.0,
        battery_capacity_kwh=100.0,
        departure_deadline=datetime(2026, 9, 12, 18, 0),
        current_lat=52.50,
        current_lon=13.40,
        simulation_start_time=datetime(2026, 9, 12, 12, 0)
    )

def test_normal_feasible_charging(mock_db, base_request):
    resp = optimize_charging(mock_db, base_request)
    assert resp.options is not None
    assert len(resp.options) > 0
    assert resp.options[0].station_id == 1

def test_unreachable_station(mock_db, base_request):
    # current battery is very low
    base_request.current_battery_pct = 0.1
    resp = optimize_charging(mock_db, base_request)
    assert len(resp.options) == 0

def test_deadline_violation(mock_db, base_request):
    base_request.departure_deadline = datetime(2026, 9, 12, 12, 0)
    resp = optimize_charging(mock_db, base_request)
    assert len(resp.options) == 0
    assert "No feasible" in resp.message

def test_green_score_calculation(mock_db, base_request):
    resp = optimize_charging(mock_db, base_request)
    opt = resp.options[0]
    assert 0 <= opt.green_charging_score <= 100
    assert "Recommended because it provides exceptional" in opt.explanation

def test_co2_savings_calculation(mock_db, base_request):
    resp = optimize_charging(mock_db, base_request)
    assert resp.options[0].co2_saved_g == 3000.0

def test_cost_calculation(mock_db, base_request):
    resp = optimize_charging(mock_db, base_request)
    opt = resp.options[0]
    # 60 kWh * 0.5 base price * 0.8 multiplier = 24.0
    assert opt.estimated_cost == 24.0

def test_renewable_percentage_calculation(mock_db, base_request):
    resp = optimize_charging(mock_db, base_request)
    assert resp.options[0].renewable_percentage == 90.0
