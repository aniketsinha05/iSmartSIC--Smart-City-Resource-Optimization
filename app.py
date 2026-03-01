from flask import Flask, request, jsonify
from datetime import datetime
import joblib
import pandas as pd
from optimizer import (
    calculate_trucks_required,
    calculate_efficiency,
    shortest_route
)

# Create Flask app FIRST
app = Flask(__name__)

# Load model & encoders
model = joblib.load("waste_model.pkl")
le_zone = joblib.load("zone_encoder.pkl")
le_ward = joblib.load("ward_encoder.pkl")


@app.route("/")
def home():
    return "Waste Optimization API is running 🚀"


@app.route("/api/waste", methods=["POST"])
def predict_waste():
    try:
        data = request.get_json()

        zone = data.get("zone")
        ward = data.get("ward")
        households = data.get("households")
        weekend_flag = data.get("weekend_flag")
        festival_flag = data.get("festival_flag")

        input_data = pd.DataFrame([{
            "zone_encoded": le_zone.transform([zone])[0],
            "ward_encoded": le_ward.transform([ward])[0],
            "households": households,
            "weekend_flag": weekend_flag,
            "festival_flag": festival_flag
        }])

        predicted_waste = model.predict(input_data)[0]

        trucks_needed = calculate_trucks_required(predicted_waste)
        optimized_allocation = trucks_needed * 5
        static_allocation = 15

        static_wastage = static_allocation - predicted_waste
        optimized_wastage = optimized_allocation - predicted_waste

        efficiency = calculate_efficiency(predicted_waste, optimized_allocation)

        route, distance = shortest_route(ward, "Wadgaon-Sheri-Kalyani nagar")

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
                "static_allocation_tpd": static_allocation
            },
            "efficiency_metrics": {
                "static_wastage_tpd": round(float(static_wastage), 2),
                "optimized_wastage_tpd": round(float(optimized_wastage), 2),
                "efficiency_improvement_percent": efficiency
            },
            "routing": {
                "destination_ward": "Wadgaon-Sheri-Kalyani nagar",
                "optimized_route": route,
                "total_distance_km": distance
            }
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)