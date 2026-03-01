import json
import pandas as pd
import os

# Define paths
RAW_PATH = "data/raw/electricity.json"
PROCESSED_PATH = "data/processed/electricity_clean.csv"

def clean_electricity_data():
    # Load raw JSON
    with open(RAW_PATH) as f:
        raw = json.load(f)

    # Extract column names
    columns = [field["id"] for field in raw["fields"]]

    # Create DataFrame
    df = pd.DataFrame(raw["records"], columns=columns)

    # Forward fill Circle values
    df["CIRCLE"] = df["CIRCLE"].ffill()

    # Identify year columns
    year_cols = [col for col in df.columns if "FY" in col]

    # Convert year columns to numeric
    for col in year_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Remove total summary rows
    df = df[df["CIRCLE"] != "Pune City Total"]

    # Keep only TOTAL category
    df = df[df["CATEGORY"] == "TOTAL"]

    # Convert from wide to long format
    df_long = df.melt(
        id_vars=["CIRCLE", "CATEGORY"],
        value_vars=year_cols,
        var_name="Year",
        value_name="Consumption"
    )

    df_long = df_long.dropna()

    # Extract year number
    df_long["Year"] = df_long["Year"].str.extract(r"(\d+)").astype(int)

    # Save cleaned file
    os.makedirs("data/processed", exist_ok=True)
    df_long.to_csv(PROCESSED_PATH, index=False)

    print("✅ Electricity data cleaned and saved!")

if __name__ == "__main__":
    clean_electricity_data()