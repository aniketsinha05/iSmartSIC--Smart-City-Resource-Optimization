import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score, mean_absolute_error
import joblib

print("Loading FULL dataset...")

# Load FULL processed dataset
df = pd.read_csv("data/processed_pune_waste_dataset.csv")

print("Dataset shape:", df.shape)

# Encode ALL zones and wards from full dataset
le_zone = LabelEncoder()
le_ward = LabelEncoder()

df["zone_encoded"] = le_zone.fit_transform(df["zone"])
df["ward_encoded"] = le_ward.fit_transform(df["ward"])

X = df[
    [
        "zone_encoded",
        "ward_encoded",
        "households",
        "weekend_flag",
        "festival_flag"
    ]
]

y = df["waste_tpd"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor(
    n_estimators=300,
    random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("R2:", round(r2_score(y_test, predictions), 3))
print("MAE:", round(mean_absolute_error(y_test, predictions), 3))

# Save updated model + encoders
joblib.dump(model, "waste_model.pkl")
joblib.dump(le_zone, "zone_encoder.pkl")
joblib.dump(le_ward, "ward_encoder.pkl")

print("Model retrained and saved successfully.")