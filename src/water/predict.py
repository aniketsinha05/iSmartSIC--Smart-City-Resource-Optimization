import pandas as pd

DATA_PATH = "data/processed/water_clean.csv"

def predict_water(day_index):
    df = pd.read_csv(DATA_PATH)

    # Use last 3-day moving average
    recent_data = df["Total M.L.D"].tail(3)
    prediction = recent_data.mean()

    return {
        "resource": "water",
        "day_index": int(day_index),
        "predicted_total_mld": round(float(prediction), 2)
    }

if __name__ == "__main__":
    df = pd.read_csv(DATA_PATH)
    next_day = df["Day_Index"].max() + 1
    print(predict_water(next_day))

