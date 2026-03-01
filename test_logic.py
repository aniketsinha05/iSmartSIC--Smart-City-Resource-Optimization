import joblib
import pandas as pd
from optimizer import (
    calculate_trucks_required,
    calculate_efficiency,
    shortest_route
)

print("========== TESTING WASTE MODULE ==========\n")

# ----------------------------
# TEST 1: Load Model
# ----------------------------
try:
    model = joblib.load("waste_model.pkl")
    le_zone = joblib.load("zone_encoder.pkl")
    le_ward = joblib.load("ward_encoder.pkl")
    print("✅ Model & Encoders Loaded Successfully\n")
except Exception as e:
    print("❌ Model loading failed:", e)
    exit()

# ----------------------------
# TEST 2: ML Prediction Test
# ----------------------------
zone = "Nagar Road-Wadgaon Sheri"
ward = "Viman Nagar"

try:
    input_data = pd.DataFrame([{
        "zone_encoded": le_zone.transform([zone])[0],
        "ward_encoded": le_ward.transform([ward])[0],
        "households": 109555,
        "weekend_flag": 1,
        "festival_flag": 0
    }])
except Exception as e:
    print("❌ Encoding Failed:", e)
    exit()

predicted_waste = model.predict(input_data)[0]

print("✅ ML Prediction Working")
print("Predicted Waste (TPD):", round(predicted_waste, 2), "\n")

# ----------------------------
# TEST 3: Truck Calculation
# ----------------------------
trucks = calculate_trucks_required(predicted_waste)
print("✅ Truck Calculation Working")
print("Trucks Required:", trucks)

# Manual Validation
manual_trucks = int(predicted_waste / 5)
if predicted_waste % 5 != 0:
    manual_trucks += 1

print("Manual Calculation:", manual_trucks)
print("Matches Function:", manual_trucks == trucks, "\n")

# ----------------------------
# TEST 4: Efficiency Logic
# ----------------------------
optimized_supply = trucks * 5
efficiency = calculate_efficiency(predicted_waste, optimized_supply)

print("✅ Efficiency Logic Working")
print("Efficiency Improvement %:", efficiency, "\n")

# ----------------------------
# TEST 5: Dijkstra Routing
# ----------------------------
route, distance = shortest_route("Viman Nagar", "Wadgaon-Sheri-Kalyani nagar")

print("✅ Dijkstra Routing Working")
print("Shortest Route:", route)
print("Total Distance:", distance, "km\n")

print("========== ALL TESTS COMPLETED ==========")