import requests

# ELECTRICITY
from src.electricity.predict import predict_consumption
from src.electricity.optimize import simulate_allocation

# WATER
from src.water.predict import predict_water
from src.water.optimize import optimize_water


# ✅ Backend is on PORT 5000
BACKEND_BASE_URL = "http://192.168.137.49:5000/api/city"


# ================================
# SEND ELECTRICITY
# ================================
def send_electricity():

    circle = "Ganeshkhind Urban Circle"
    year = 2019

    prediction = predict_consumption(circle, year)
    optimization = simulate_allocation(circle, year)

    combined_data = {
        "predicted": prediction,
        "optimized": optimization
    }

    response = requests.post(
        f"{BACKEND_BASE_URL}/electricity",
        json=combined_data,
        timeout=10
    )

    print("Electricity Sent:", response.text)


# ================================
# SEND WATER
# ================================
def send_water():

    source = "Parvati       M.L.D"

    prediction = predict_water(1)
    optimization = optimize_water(source)

    combined_data = {
        "predicted": prediction,
        "optimized": optimization
    }

    response = requests.post(
        f"{BACKEND_BASE_URL}/water",
        json=combined_data,
        timeout=10
    )

    print("Water Sent:", response.text)


# ================================
# RUN EVERYTHING
# ================================
if __name__ == "__main__":

    try:
        send_electricity()
        send_water()
    except Exception as e:
        print("Error:", e)