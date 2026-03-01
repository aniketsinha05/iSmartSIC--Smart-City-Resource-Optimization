import pandas as pd
import os
from src.electricity.predict import predict_consumption

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "electricity_clean.csv")


def simulate_allocation(circle: str, year: int):

    df = pd.read_csv(DATA_PATH)

    # Historical average
    historical_avg = df[df["CIRCLE"] == circle]["Consumption"].mean()

    # Get prediction dictionary
    predicted_dict = predict_consumption(circle, year)

    # Extract numeric value
    predicted = predicted_dict["predicted_consumption_lakh_units"]

    # 12% reduction
    optimized_usage = predicted * 0.88

    reduction_percent = ((predicted - optimized_usage) / predicted) * 100

    return {
        "resource": "electricity",
        "circle": circle,
        "year": year,
        "current_usage": round(predicted, 2),
        "historical_average": round(historical_avg, 2),
        "optimized_usage": round(optimized_usage, 2),
        "estimated_savings": round(predicted - optimized_usage, 2),
        "reduction_percent": round(reduction_percent, 2)
    }