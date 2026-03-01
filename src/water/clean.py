import json
import pandas as pd
import os

RAW_PATH = "data/raw/water.json"
PROCESSED_PATH = "data/processed/water_clean.csv"

def clean_water_data():
    with open(RAW_PATH) as f:
        raw = json.load(f)

    columns = [field["id"] for field in raw["fields"]]
    df = pd.DataFrame(raw["records"], columns=columns)

    # Remove TOTAL and AVERAGE rows
    df = df[~df["Date"].isin(["TOTAL", "AVERAGE"])]

    # Convert Date
    df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")

    # Convert Total M.L.D to numeric
    df["Total M.L.D"] = pd.to_numeric(df["Total M.L.D"], errors="coerce")

    df = df.dropna()

    # Create day index
    df = df.sort_values("Date")
    df["Day_Index"] = range(len(df))

    os.makedirs("data/processed", exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)

    print("✅ Water data cleaned and saved!")

if __name__ == "__main__":
    clean_water_data()