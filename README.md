# 🗑 Pune Smart Waste Optimization Module

## 📌 Project: iSmartSIC – Smart City Resource Optimization  
Branch: niranjan  
City: Pune  

---

# 🚀 Project Overview

This module implements AI-based waste demand forecasting and optimization for Pune city wards.

The system replaces static waste collection scheduling with dynamic, demand-based truck allocation and shortest-route optimization.

---

# 🧠 Problem Statement

Traditional waste systems:
- Fixed trucks per ward
- Static daily schedules
- No demand prediction
- Inefficient routing

Our system:
- Predicts waste generation per ward
- Allocates trucks dynamically
- Calculates efficiency improvement
- Uses Dijkstra’s algorithm for route optimization

---

# 📊 Dataset Structure

## Raw Dataset
Ward-level data:
- Zone
- Ward
- Households
- Waste (TPD)

## Processed Dataset
Time-series engineered:
- zone
- ward
- date
- households
- weekend_flag
- festival_flag
- waste_tpd

---

# 🔄 Preprocessing Steps

1. Removed duplicates
2. Handled missing values
3. Converted date to datetime
4. Extracted day_of_week and month
5. Applied IQR-based outlier removal
6. Generated processed dataset

---

# 🤖 Machine Learning Model

Model Used:
- RandomForestRegressor

Features:
- zone_encoded
- ward_encoded
- households
- weekend_flag
- festival_flag

Target:
- waste_tpd

Evaluation Metrics:
- R2 Score
- MAE

---

# 🚛 Optimization Logic

Truck Capacity:
5 Tonnes per truck

Dynamic Allocation:
ceil(predicted_waste / 5)

Efficiency Comparison:
Static Allocation vs Smart Allocation

---

# 🧮 Graph & DSA Component

We implemented Dijkstra’s algorithm using NetworkX.

Nodes:
- Wards

Edges:
- Distance (km)

Output:
- Shortest Route
- Total Distance

---

# 🌐 Flask API

Endpoint:
POST /predict-waste

Request:
{
  "zone": "Nagar Road-Wadgaon Sheri",
  "ward": "Viman Nagar",
  "households": 109555,
  "weekend_flag": 1,
  "festival_flag": 0
}

Response:
{
  "prediction": {},
  "allocation": {},
  "efficiency_metrics": {},
  "routing": {}
}

---

# 📈 System Architecture

Raw Data  
↓  
Preprocessing  
↓  
ML Model  
↓  
Optimization Logic  
↓  
Flask API  
↓  
Node Backend  
↓  
React Dashboard  

---

# 🎯 Innovation Highlights

- AI-driven demand prediction
- Demand-based truck allocation
- Route optimization using DSA
- Efficiency improvement metric
- Modular microservice architecture

---

# 👨‍💻 Developer

Niranjan – Waste ML & Optimization Engineer
