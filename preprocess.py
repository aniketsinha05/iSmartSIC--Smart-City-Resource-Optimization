import pandas as pd
import numpy as np
import os

print("🔄 Starting Preprocessing for Pune Waste Dataset...\n")

DATA_PATH = "data/pune_waste_full_dataset.csv"

# -------------------------------
# 1️⃣ Load Dataset Safely
# -------------------------------
if not os.path.exists(DATA_PATH):
    raise FileNotFoundError("Dataset not found in data folder.")

df = pd.read_csv(DATA_PATH)

print("Original Shape:", df.shape)

# -------------------------------
# 2️⃣ Basic Cleaning
# -------------------------------

# Standardize column names
df.columns = df.columns.str.strip().str.lower()

# Remove duplicates
df = df.drop_duplicates()

print("\nColumns:", df.columns.tolist())

# Validate required columns
required_columns = ["zone", "ward", "households"]
for col in required_columns:
    if col not in df.columns:
        raise Exception(f"Missing required column: {col}")

# Identify waste column safely
if "waste_tpd" in df.columns:
    waste_column = "waste_tpd"
elif "predicted_waste_tpd" in df.columns:
    waste_column = "predicted_waste_tpd"
else:
    raise Exception("No waste column found.")

# Handle missing numeric values
numeric_cols = df.select_dtypes(include=[np.number]).columns
for col in numeric_cols:
    df[col] = df[col].fillna(df[col].median())

# Drop critical missing values
df = df.dropna(subset=["zone", "ward", waste_column])

print("\nAfter Cleaning Shape:", df.shape)

# -------------------------------
# 3️⃣ Feature Engineering
# -------------------------------

# Convert date if exists
if "date" in df.columns:
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    df["day_of_week"] = df["date"].dt.dayofweek
    df["month"] = df["date"].dt.month

    # Weekend consistency
    df["weekend_flag"] = df["day_of_week"].apply(lambda x: 1 if x >= 5 else 0)

else:
    print("⚠ No date column found — skipping time features.")

# -------------------------------
# 4️⃣ Outlier Handling (IQR)
# -------------------------------

Q1 = df[waste_column].quantile(0.25)
Q3 = df[waste_column].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

df = df[(df[waste_column] >= lower_bound) & (df[waste_column] <= upper_bound)]

print("\nAfter Outlier Removal Shape:", df.shape)

# -------------------------------
# 5️⃣ Save Processed Dataset
# -------------------------------

OUTPUT_PATH = "data/processed_pune_waste_dataset.csv"
df.to_csv(OUTPUT_PATH, index=False)

print("\n✅ Preprocessing Completed Successfully.")
print("Processed Dataset Shape:", df.shape)