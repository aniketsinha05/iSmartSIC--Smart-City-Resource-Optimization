import pandas as pd
import joblib
import json
import requests
from datetime import datetime
from optimizer import (
    calculate_trucks_required,
    calculate_efficiency,
    shortest_route
)

# ---------------- LOAD MODEL ---------------- #
model = joblib.load("waste_model.pkl")
le_zone = joblib.load("zone_encoder.pkl")
le_ward = joblib.load("ward_encoder.pkl")

# ---------------- LOAD DATASET ---------------- #
df = pd.read_csv("data/processed_pune_waste_dataset.csv")

# Ensure date column exists and is datetime
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# ---------------- REDUCE TO 2 TIMESTAMPS PER WARD ---------------- #
reduced_rows = []

for ward, group in df.groupby("ward"):

    weekday_record = group[group["weekend_flag"] == 0].head(1)
    weekend_record = group[group["weekend_flag"] == 1].head(1)

    if not weekday_record.empty:
        reduced_rows.append(weekday_record)

    if not weekend_record.empty:
        reduced_rows.append(weekend_record)

reduced_df = pd.concat(reduced_rows).reset_index(drop=True)

print("Original rows:", len(df))
print("Reduced rows (2 per ward):", len(reduced_df))

# ---------------- GENERATE OUTPUT ---------------- #

results = []

for _, row in reduced_df.iterrows():

    zone = row["zone"]
    ward = row["ward"]

    zone_encoded = le_zone.transform([zone])[0]
    ward_encoded = le_ward.transform([ward])[0]

    input_data = pd.DataFrame([{
        "zone_encoded": zone_encoded,
        "ward_encoded": ward_encoded,
        "households": row["households"],
        "weekend_flag": row["weekend_flag"],
        "festival_flag": row["festival_flag"]
    }])

    # Prediction
    predicted_waste = model.predict(input_data)[0]

    # Optimization
    truck_capacity = 5
    trucks_required = calculate_trucks_required(predicted_waste)
    optimized_allocation = trucks_required * truck_capacity
    static_allocation = 15

    static_wastage = static_allocation - predicted_waste
    optimized_wastage = optimized_allocation - predicted_waste
    efficiency = calculate_efficiency(predicted_waste, optimized_allocation)

    # Routing
    destination = "Wadgaon-Sheri-Kalyani nagar"
    route, distance = shortest_route(ward, destination)

    result_json = {
        "status": "success",
        "city": "Pune",
        "timestamp": row["date"].isoformat(),
        "prediction": {
            "zone": zone,
            "ward": ward,
            "predicted_waste_tpd": round(float(predicted_waste), 2)
        },
        "allocation": {
            "truck_capacity_tpd": truck_capacity,
            "trucks_required": trucks_required,
            "optimized_allocation_tpd": optimized_allocation,
            "static_allocation_tpd": static_allocation
        },
        "efficiency_metrics": {
            "static_wastage_tpd": round(float(static_wastage), 2),
            "optimized_wastage_tpd": round(float(optimized_wastage), 2),
            "efficiency_improvement_percent": round(float(efficiency), 2)
        },
        "routing": {
            "destination_ward": destination,
            "optimized_route": route,
            "total_distance_km": distance
        }
    }

    results.append(result_json)

# ---------------- FINAL BIG JSON ---------------- #

final_output = {
    "status": "success",
    "city": "Pune",
    "generated_at": datetime.now().isoformat(),
    "total_records": len(results),
    "results": results
}

# Save locally
with open("reduced_single_big_output.json", "w") as f:
    json.dump(final_output, f, indent=4)

print("\nReduced big JSON generated successfully.")
print("Saved as: reduced_single_big_output.json")

# ---------------- SEND TO FRIEND ---------------- #

FRIEND_URL = "http://192.168.137.49:5000/api/waste"

response = requests.post(FRIEND_URL, json=final_output)

print("Sent to friend → Status Code:", response.status_code)