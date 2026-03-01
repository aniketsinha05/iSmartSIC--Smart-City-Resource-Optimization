import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os

DATA_PATH = "data/processed/water_clean.csv"
MODEL_PATH = "models/water_model.pkl"

def train_model():
    df = pd.read_csv(DATA_PATH)

    X = df[["Day_Index"]]
    y = df["Total M.L.D"]

    model = LinearRegression()
    model.fit(X, y)

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print("✅ Water model trained and saved!")

if __name__ == "__main__":
    train_model()