from fastapi import FastAPI
from pydantic import BaseModel
import requests

# ELECTRICITY
from src.electricity.predict import predict_consumption
from src.electricity.optimize import simulate_allocation

# WATER
from src.water.predict import predict_water
from src.water.optimize import optimize_water

app = FastAPI()

BACKEND_BASE_URL = "http://192.168.137.49:5000/api/city"


# ================================
# ELECTRICITY API
# ================================

class ElectricityRequest(BaseModel):
    circle: str
    year: int


@app.post("/electricity")
def electricity_api(request: ElectricityRequest):

    prediction = predict_consumption(request.circle, request.year)
    optimization = simulate_allocation(request.circle, request.year)

    combined_data = {
        "predicted": prediction,
        "optimized": optimization
    }

    # Send to main backend
    try:
        response = requests.post(
            f"{BACKEND_BASE_URL}/electricity",
            json=combined_data
        )
        backend_response = response.json()
    except Exception as e:
        backend_response = {"error": str(e)}

    return {
        "local_result": combined_data,
        "backend_response": backend_response
    }


# ================================
# WATER API
# ================================

class WaterRequest(BaseModel):
    source: str


@app.post("/water")
def water_api(request: WaterRequest):

    prediction = predict_water(1)
    optimization = optimize_water(request.source)

    combined_data = {
        "predicted": prediction,
        "optimized": optimization
    }

    # Send to main backend
    try:
        response = requests.post(
            f"{BACKEND_BASE_URL}/water",
            json=combined_data
        )
        backend_response = response.json()
    except Exception as e:
        backend_response = {"error": str(e)}

    return {
        "local_result": combined_data,
        "backend_response": backend_response
    }


@app.get("/")
def home():
    return {"message": "Smart City Resource Optimization API is running"}