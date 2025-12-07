# 📦 AI Supply Chain Optimizer

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95-009688)
![Streamlit](https://img.shields.io/badge/Streamlit-1.22-FF4B4B)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED)
![Prophet](https://img.shields.io/badge/ML-Facebook%20Prophet-orange)
![Render](https://img.shields.io/badge/Deployment-Render-black)

An end-to-end **Inventory Optimization System** that uses Machine Learning to predict demand and automate inventory decisions. This tool helps supply chain managers prevent **stockouts** and reduce **overstock** by calculating dynamic Safety Stock levels and Reorder Points based on probabilistic forecasts.

---

## 🚀 Features

* **Demand Forecasting:** Uses **Facebook Prophet** to predict future sales based on historical data, accounting for seasonality and trends.
* **Inventory Optimization Engine:** Implements probabilistic logic to calculate:
    * **Safety Stock:** Buffer inventory needed to mitigate supply chain risk (95% Service Level).
    * **Reorder Point (ROP):** The exact inventory level that triggers a new order.
* **Interactive Dashboard:** A **Streamlit** UI for visualizing forecasts and receiving real-time "Order Now" / "Healthy" alerts.
* **REST API:** A **FastAPI** backend that serves predictions and optimization logic to any frontend or ERP system.
* **Cloud Native:** Fully containerized with **Docker** for consistent deployment across environments.

---

## 🛠️ Tech Stack

* **Language:** Python 3.9+
* **Machine Learning:** Facebook Prophet, Pandas, Scikit-Learn
* **Backend:** FastAPI, Uvicorn
* **Frontend:** Streamlit, Plotly
* **DevOps:** Docker, Render (Cloud Hosting)
* **Database:** SQLite (Development), PostgreSQL (Production-ready)

---

## 📂 Project Structure

```bash
supply-chain-optimizer/
├── dashboard/
│   └── app.py              # Streamlit Frontend
├── data/
│   └── .gitignore          # Ignores large CSV files to prevent Git errors
├── models/
│   └── forecast_model.pkl  # Trained ML Model
├── src/
│   ├── db_setup.py         # Database initialization script
│   ├── train_model.py      # ML Training pipeline
│   ├── optimization.py     # Business logic (Safety Stock/ROP math)
│   └── main.py             # FastAPI Backend
├── Dockerfile              # Docker configuration for Render deployment
├── requirements.txt        # Python Dependencies
└── README.md
