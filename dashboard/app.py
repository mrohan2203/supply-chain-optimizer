import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# 1. Page Configuration (Must be first)
st.set_page_config(
    page_title="Supply Chain AI",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS for "SaaS" Look
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #0E1117;
    }
    
    /* Card Styling for Metrics */
    div[data-testid="metric-container"] {
        background-color: #262730;
        border: 1px solid #464B5C;
        padding: 5% 5% 5% 10%;
        border-radius: 10px;
        color: white;
        overflow-wrap: break-word;
    }

    /* Custom Status Indicators */
    .status-box {
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
        font-weight: bold;
        font-size: 24px;
    }
    .status-critical {
        background-color: #FF4B4B; 
        color: white;
        border: 1px solid #FF4B4B;
    }
    .status-healthy {
        background-color: #00CC96; 
        color: white;
        border: 1px solid #00CC96;
    }
</style>
""", unsafe_allow_html=True)

# 3. Sidebar
st.sidebar.header("🎛️ Control Panel")
st.sidebar.markdown("---")
curr_stock = st.sidebar.number_input("Current Stock Level", value=50, step=5)
lead_time = st.sidebar.slider("Lead Time (Days)", 1, 14, 5)

st.sidebar.markdown("### Model Info")
st.sidebar.info("Model: Prophet (Meta)\nAccuracy: ~85%")

# 4. Main Title
st.title("📦 AI Supply Chain Optimizer")
st.markdown("Real-time inventory intelligence and forecasting.")

if st.sidebar.button("Analyze Inventory", type="primary"):
    # Try to get the URL from Streamlit Secrets first, then os.getenv, then default
    if "BACKEND_URL" in st.secrets:
        base_url = st.secrets["BACKEND_URL"]
    else:
        base_url = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
    st.write(f"DEBUG: Connecting to {base_url}")
    # Call the API
    try:
        response = requests.get(
            f"http://127.0.0.1:8000/predict?current_stock={curr_stock}&lead_time={lead_time}"
        )
        data = response.json()
        
        # --- UI LAYOUT ---
        
        # A. Status Banner
        status = data['status']
        css_class = "status-critical" if status == "ORDER NOW" else "status-healthy"
        status_icon = "⚠️" if status == "ORDER NOW" else "✅"
        
        st.markdown(f"""
            <div class="status-box {css_class}">
                {status_icon} RECOMMENDATION: {status}
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📊 Key Metrics")
        
        # B. Metric Cards (3 Columns)
        col1, col2, col3 = st.columns(3)
        
        # Use delta to show "vs target" or difference (optional visual flare)
        col1.metric(
            "Predicted Demand", 
            value=f"{data['metrics']['forecast_lead_time']} units",
            delta="Next 5 Days"
        )
        
        col2.metric(
            "Safety Stock Buffer", 
            value=f"{data['metrics']['safety_stock']} units",
            help="Extra stock kept to mitigate risk of stockouts."
        )
        
        col3.metric(
            "Reorder Point", 
            value=f"{data['metrics']['reorder_point']} units",
            help="Order when stock hits this level."
        )
        
        st.markdown("---")

        # C. Professional Chart
        st.markdown("### 📈 Demand Forecast (Next 30 Days)")
        
        chart_data = pd.DataFrame(data['plot_data'])
        chart_data['ds'] = pd.to_datetime(chart_data['ds'])
        
        # Create a sleek Area Chart using Plotly Graph Objects
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=chart_data['ds'], 
            y=chart_data['yhat'],
            mode='lines',
            name='Forecast',
            line=dict(color='#00CC96', width=3),
            fill='tozeroy',  # Fill area under line
            fillcolor='rgba(0, 204, 150, 0.2)' # Transparent green fill
        ))

        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', # Transparent background
            plot_bgcolor='rgba(0,0,0,0)',
            template="plotly_dark",
            margin=dict(l=20, r=20, t=30, b=20),
            hovermode="x unified",
            xaxis=dict(showgrid=False), # Remove vertical grid lines
            yaxis=dict(showgrid=True, gridcolor='#444'), # Subtle horizontal grid
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error connecting to API. Is the backend running? \n\nDetails: {e}")

else:
    st.info("👈 Adjust parameters in the sidebar and click **Analyze Inventory** to start.")