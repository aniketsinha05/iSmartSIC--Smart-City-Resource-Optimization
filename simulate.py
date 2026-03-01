import joblib
import pandas as pd
from datetime import datetime
from optimizer import (
    calculate_trucks_required,
    calculate_efficiency,
    shortest_route
)

print("🚀 Running Smart Waste Simulation...\n")

# ---------------- LOAD MODEL ---------------- #

try:
    model = joblib.load("waste_model.pkl")
    le_zone = joblib.load("zone_encoder.pkl")
    le_ward = joblib.load("ward_encoder.pkl")
except Exception as e:
    print("❌ Error loading model:", e)
    exit()

# ---------------- INPUT DATA ---------------- #

zone = "Nagar Road-Wadgaon Sheri"
ward = "Viman Nagar"

households = 109555
weekend_flag = 1
festival_flag = 0

# ---------------- ENCODING ---------------- #

try:
    input_data = pd.DataFrame([{
        "zone_encoded": le_zone.transform([zone])[0],
        "ward_encoded": le_ward.transform([ward])[0],
        "households": households,
        "weekend_flag": weekend_flag,
        "festival_flag": festival_flag
    }])
except Exception as e:
    print("❌ Encoding Error:", e)
    exit()

# ---------------- PREDICTION ---------------- #

predicted_waste = model.predict(input_data)[0]

# ---------------- OPTIMIZATION ---------------- #

trucks_needed = calculate_trucks_required(predicted_waste)
optimized_allocation = trucks_needed * 5
efficiency = calculate_efficiency(predicted_waste, optimized_allocation)

# ---------------- ROUTING ---------------- #

destination = "Wadgaon-Sheri-Kalyani nagar"
route, distance = shortest_route(ward, destination)

# ---------------- STRUCTURED OUTPUT ---------------- #

response = {
    "status": "success",
    "city": "Pune",
    "timestamp": datetime.now().isoformat(),

    "prediction": {
        "zone": zone,
        "ward": ward,
        "predicted_waste_tpd": round(float(predicted_waste), 2)
    },

    "allocation": {
        "truck_capacity_tpd": 5,
        "trucks_required": trucks_needed,
        "optimized_allocation_tpd": optimized_allocation,
        "static_allocation_tpd": 15
    },

    "efficiency_metrics": {
        "efficiency_improvement_percent": efficiency
    },

    "routing": {
        "destination_ward": destination,
        "optimized_route": route,
        "total_distance_km": distance
    }
}

print("✅ Simulation Complete\n")
print(response)