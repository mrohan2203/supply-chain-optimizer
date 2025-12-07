import pandas as pd
from sqlalchemy import create_engine
from prophet import Prophet
import joblib

def train():
    engine = create_engine('sqlite:///supply_chain.db')

    # 1. Fetch data for a specific Item (e.g., Item ID 1 at Store 1)
    # Prophet requires columns named 'ds' (Date) and 'y' (Target)
    # UPDATED QUERY
    query = """
        SELECT date as ds, sales as y 
        FROM sales 
        WHERE family = 'GROCERY I' AND store_nbr = 1
    """
    df = pd.read_sql(query, engine)

    if df.empty:
        print("No data found for this item/store combination.")
        return

    # 2. Train Model
    print("Training Prophet model...")
    model = Prophet()
    model.fit(df)

    # 3. Save Model
    joblib.dump(model, 'models/forecast_model.pkl')
    print("Model saved to models/forecast_model.pkl")

if __name__ == "__main__":
    train()