import requests

url = "http://127.0.0.1:5000/api/waste"

data = {
    "zone": "Nagar Road-Wadgaon Sheri",
    "ward": "Viman Nagar",
    "households": 109555,
    "weekend_flag": 1,
    "festival_flag": 0
}

response = requests.post(url, json=data)

print("Status Code:", response.status_code)
print("Response JSON:", response.json())