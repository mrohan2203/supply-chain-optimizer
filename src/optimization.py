import numpy as np

def calculate_metrics(forecast, lead_time=5, service_level_z=1.65):
    """
    Returns: (forecast_demand, safety_stock, reorder_point)
    """
    # 1. Forecast Demand during Lead Time
    # We sum the predicted sales for the next X days (Lead Time)
    lead_time_demand = forecast.head(lead_time)['yhat'].sum()
    
    # 2. Safety Stock Logic
    # We estimate error as 20% of demand (simplified for MVP)
    # Formula: Z * std_dev * sqrt(Lead Time)
    daily_volatility = lead_time_demand * 0.2 
    safety_stock = service_level_z * daily_volatility * np.sqrt(lead_time)
    
    # 3. Reorder Point
    reorder_point = lead_time_demand + safety_stock
    
    return int(lead_time_demand), int(safety_stock), int(reorder_point)