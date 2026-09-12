# EV Charging Network Renewable-Optimization Platform

## 1. Problem Statement
As Electric Vehicle (EV) adoption accelerates, charging sessions are frequently initiated during periods of high grid demand and low renewable energy generation. This leads to higher carbon footprints, increased strain on the power grid, and greater costs to the consumer.

## 2. Solution Overview
The **EV Charging Network Renewable-Optimization Platform** is a smart, interactive dashboard designed to align EV charging schedules with peak renewable energy availability. By capturing user constraints (such as departure deadlines and current battery states) and evaluating them against forecasted grid conditions, the platform calculates the absolute optimal time and location to charge.

## 3. Key Features
* **Smart Scheduling Engine:** Automatically identifies the greenest and most cost-effective time window to charge before your departure deadline.
* **Interactive Map:** Pick your starting location visually using OpenStreetMap and Leaflet.
* **Cost & CO2 Projections:** Real-time estimations of energy costs and carbon emissions saved.
* **Explainable AI Recommendations:** Dynamic explanations provided for *why* a particular time slot was chosen (e.g., exceptional renewable availability, low price).
* **Data Visualizations:** Interactive Recharts area graphs displaying the incoming 24-hour renewable energy "duck curve".

## 4. How the Optimization Works
When a user requests an optimized charging plan, the backend engine performs a grid-search across all available charging stations and hourly time slots:
1. **Reachability Check:** Discards stations that require more travel energy than the EV currently has.
2. **Temporal Check:** Discards charging slots that fail to complete before the user's departure deadline.
3. **Evaluation:** Calculates the exact travel time, charging duration, and overlaps this schedule against hourly grid conditions (price multiplier, carbon intensity, renewable %).
4. **Scoring:** The remaining valid options are normalized and scored from 0 to 100 based on a weighted formula.

### Green Charging Score Weights
The algorithm evaluates options using the following prioritized weights:
- **Renewable Energy Availability:** 50%
- **Charging Cost:** 25%
- **Convenience (Distance/Time):** 15%
- **CO2 Impact:** 10%

*(Note: For this prototype, **travel time** is calculated using the Haversine distance formula assuming a fixed speed of **50 km/h**, and **travel energy** assumes a fixed EV efficiency of **0.2 kWh/km**).*

## 5. Technology Stack
* **Frontend:** React + Vite, Leaflet (react-leaflet), Recharts
* **Backend:** Python + FastAPI
* **Database:** SQLite + SQLAlchemy ORM

## 6. Project Folder Structure
```text
EV-RENEWABLE-OPTIMIZATION/
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI Application Entry
│   │   ├── models.py          # SQLAlchemy Models
│   │   ├── schemas.py         # Pydantic Schemas
│   │   ├── database.py        # SQLite connection
│   │   └── services/          # Core optimization engine logic
│   ├── tests/                 # Pytest test suite
│   ├── generate_mock_data.py  # Mock data seeder
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/        # React components (Map, Cards, Charts)
│   │   ├── services/          # Axios API wrappers
│   │   ├── App.jsx            # Main view
│   │   └── index.css          # Glassmorphism aesthetic
│   └── package.json           # Node dependencies
└── README.md
```

## 7. API Endpoints
* `GET /api/health` - Basic API heartbeat.
* `GET /api/stations` - Returns all available simulated charging stations.
* `GET /api/grid-conditions` - Returns hourly forecasts of grid conditions.
* `POST /api/optimize` - Accepts a `UserRequest` payload and returns ranked `ChargingOption` recommendations.

*Disclaimer: Grid conditions and station availability are powered by **deterministic simulated data** generated via `generate_mock_data.py` for prototype stability. Real-time external APIs are not connected in this version.*

## 8. Example User Flow
1. Open the dashboard and view the interactive map.
2. Enter current battery %, target battery %, and battery capacity.
3. Set your **Departure Deadline**.
4. Click anywhere on the map to drop a pin representing your current location.
5. Click **"Find Smart Charging Plan"**.
6. The dashboard triggers the API, processes the math, and renders your top recommendation, the route on the map, and a chart highlighting the renewable energy forecast.

## 9. Setup & Run Instructions (Windows)

### Backend Setup
Open a terminal (PowerShell or CMD) in the `backend` folder:
```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# Generate the simulated SQLite data
python generate_mock_data.py

# Start the FastAPI server (Runs on port 8001 to avoid conflicts)
uvicorn app.main:app --host 127.0.0.1 --port 8001
```

### Frontend Setup
Open a separate terminal in the `frontend` folder:
```powershell
cd frontend
npm install

# Start the Vite development server
npm run dev -- --host 127.0.0.1 --port 5173
```
Navigate to `http://127.0.0.1:5173` in your browser.

## 10. Future Improvements
* Integration with real-time grid operators (e.g., ENTSO-E or WattTime API).
* Live traffic-aware routing (via Google Maps or Mapbox APIs) instead of straight-line Haversine distances.
* Personalized EV profiles containing specific charging curves and real-world efficiencies.
