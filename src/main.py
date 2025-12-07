from fastapi import FastAPI
import joblib
import pandas as pd
from src.optimization import calculate_metrics

app = FastAPI()

# Load model once at startup
model = joblib.load('models/forecast_model.pkl')

@app.get("/predict")
def predict(current_stock: int, lead_time: int = 5):
    # 1. Generate Forecast (next 30 days)
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)
    
    # Filter for future dates only
    future_forecast = forecast.tail(30)
    
    # 2. Apply Optimization Math
    demand, safety_stock, rop = calculate_metrics(future_forecast, lead_time)
    
    # 3. Determine Action
    status = "ORDER NOW" if current_stock <= rop else "HEALTHY"
    
    return {
        "status": status,
        "metrics": {
            "forecast_lead_time": demand,
            "safety_stock": safety_stock,
            "reorder_point": rop,
            "current_stock": current_stock
        },
        "plot_data": future_forecast[['ds', 'yhat']].to_dict(orient='records')
    }