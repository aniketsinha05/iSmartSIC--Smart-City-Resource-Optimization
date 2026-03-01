import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "water_clean.csv")

def optimize_water(source: str):
    """
    Simulates smart water allocation using:
    - Source-based supply averages
    - Leakage reduction simulation (15%)
    """

    df = pd.read_csv(DATA_PATH)

    if source not in df.columns:
        raise ValueError("Invalid water source column name")

    # Current average supply from source
    current_supply = df[source].mean()

    # Simulate 15% leakage reduction
    optimized_supply = current_supply * 0.85

    savings = current_supply - optimized_supply
    reduction_percent = 15.0

    return {
        "resource": "water",
        "source": source,
        "current_supply_mld": round(current_supply, 2),
        "optimized_supply_mld": round(optimized_supply, 2),
        "water_saved_mld": round(savings, 2),
        "efficiency_gain_percent": reduction_percent
    }