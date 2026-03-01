import pandas as pd
import joblib

DATA_PATH = "data/processed/electricity_clean.csv"
MODEL_PATH = "models/electricity_model.pkl"

def predict_consumption(circle_name, year):
    # Load data (for encoding reference)
    df = pd.read_csv(DATA_PATH)
    model = joblib.load(MODEL_PATH)

    # Recreate encoding
    df["Circle_Code"] = df["CIRCLE"].astype("category").cat.codes
    circle_mapping = dict(enumerate(df["CIRCLE"].astype("category").cat.categories))

    # Reverse mapping
    circle_to_code = {v: k for k, v in circle_mapping.items()}

    if circle_name not in circle_to_code:
        raise ValueError("Circle not found")

    circle_code = circle_to_code[circle_name]

    prediction = model.predict([[circle_code, year]])

    return {
        "circle": circle_name,
        "year": year,
        "predicted_consumption_lakh_units": round(float(prediction[0]), 2)
    }


if __name__ == "__main__":
    # Example test
    result = predict_consumption("Ganeshkhind Urban Circle", 2019)
    print(result)