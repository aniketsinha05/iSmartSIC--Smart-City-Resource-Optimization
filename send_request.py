import pandas as pd
import requests
import json
import time

# Your local ML API
LOCAL_URL = "http://127.0.0.1:5000/api/waste"

# Friend's backend
FRIEND_URL = "http://192.168.137.49:5000/api/waste"

df = pd.read_csv("data/processed_pune_waste_dataset.csv")

print("Total rows:", len(df))

for index, row in df.iterrows():

    # Step 1: Send input to YOUR ML API
    waste_input = {
        "zone": row["zone"],
        "ward": row["ward"],
        "households": int(row["households"]),
        "weekend_flag": int(row["weekend_flag"]),
        "festival_flag": int(row["festival_flag"])
    }

    try:
        # Call your ML module
        ml_response = requests.post(LOCAL_URL, json=waste_input)

        if ml_response.status_code != 200:
            print("ML failed at row", index+1)
            continue

        full_output_json = ml_response.json()

        # Step 2: Send FULL JSON to friend
        friend_response = requests.post(FRIEND_URL, json=full_output_json)

        print(f"Row {index+1} → Sent to friend → Status:",
              friend_response.status_code)

    except Exception as e:
        print("Error at row", index+1, ":", e)

    time.sleep(0.05)

print("All rows processed and sent to friend.")