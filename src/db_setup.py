import pandas as pd
from sqlalchemy import create_engine

def init_db():
    print("Loading data... this might take a minute.")
    # Load only a subset to keep it fast (First 50k rows)
    df = pd.read_csv("data/train.csv", parse_dates=['date'])
    df = df.iloc[:50000] 

    # Create SQLite database engine
    engine = create_engine('sqlite:///supply_chain.db')

    # Write data to SQL table 'sales'
    df.to_sql('sales', engine, if_exists='replace', index=False)
    print("Database 'supply_chain.db' created successfully!")

if __name__ == "__main__":
    init_db()