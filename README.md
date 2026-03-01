
# Smart City Resource Optimization – ML Microservice

## Overview

This project implements a Machine Learning–based microservice for a Smart City Resource Optimization system. 
The service predicts and optimizes electricity consumption and water supply and sends structured JSON data 
to a centralized backend for dashboard visualization.

The system separates predictive intelligence (demand forecasting) from prescriptive intelligence 
(resource optimization logic).


## System Architecture

ML Microservice (Python)
→ Prediction and Optimization
→ REST API Communication
→ Node.js Backend (Port 5000)
→ Frontend Dashboard

The ML service runs independently and transmits processed results to the backend for storage and visualization.


## Electricity Module

### Prediction

Model: Linear Regression

Inputs:
- Circle Name
- Year

Output:
- Predicted electricity consumption (Lakh Units)

Example:
Circle: Ganeshkhind Urban Circle
Year: 2019
Predicted Consumption: 43767.77 Lakh Units

Unit Definition:
1 Lakh Unit = 100,000 kWh


### Optimization

A smart-grid efficiency simulation is applied after prediction.

- 12% reduction applied to predicted consumption
- Calculates optimized usage
- Computes estimated savings
- Computes reduction percentage
- Compares with historical average

This represents prescriptive logic built on top of ML predictions.


## Water Module

### Prediction

Method: 3-day moving average forecasting

Output:
- Predicted total supply (MLD – Million Liters per Day)


### Optimization

A leakage reduction simulation is applied.

- 15% efficiency improvement
- Calculates optimized supply
- Computes water saved (MLD)
- Computes efficiency gain percentage


## API Communication

The ML service sends structured JSON payloads to:

POST /api/city/electricity
POST /api/city/water

Backend runs on port 5000.

Example JSON structure:

{
  "predicted": { ... },
  "optimized": { ... }
}


## Dashboard KPIs

Electricity:
- Predicted Consumption (Lakh Units)
- Optimized Consumption
- Estimated Savings
- Reduction Percentage

Water:
- Predicted Demand (MLD)
- Optimized Supply
- Water Saved (MLD)
- Efficiency Gain Percentage


## How to Run

1. Install Dependencies:
   pip install pandas scikit-learn joblib requests

2. Ensure backend server is running on port 5000.

3. Execute:
   python main.py

The script performs prediction, applies optimization logic, and sends results to the backend API.


## Technologies Used

- Python
- Pandas
- Scikit-learn
- Joblib
- Requests
- Node.js
- Express
- React


## Academic Scope

This project demonstrates:
- Demand forecasting using regression
- Statistical time-series smoothing
- Optimization simulation logic
- RESTful API integration
- Microservice-based system design
- Smart resource allocation for urban infrastructure
