import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os

DATA_PATH = "data/processed/electricity_clean.csv"
MODEL_PATH = "models/electricity_model.pkl"

def train_model():
    df = pd.read_csv(DATA_PATH)

    # Encode Circle as numbers
    df["Circle_Code"] = df["CIRCLE"].astype("category").cat.codes

    X = df[["Circle_Code", "Year"]]
    y = df["Consumption"]

    model = LinearRegression()
    model.fit(X, y)

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print("✅ Model trained and saved!")

if __name__ == "__main__":
    train_model()
    