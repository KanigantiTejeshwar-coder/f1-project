import streamlit as st
import fastf1
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import warnings

warnings.filterwarnings('ignore')

# 1. Setup Web Page Layout
st.set_page_config(page_title="F1 Analysis Tool", layout="wide")
st.title("🏎️ Production-Grade Formula 1 Telemetry Engine")

fastf1.Cache.enable_cache('./cache')

# 2. Sidebar Global Controls
st.sidebar.header("Global Settings")
selected_year = st.sidebar.selectbox("Select Year", [2025, 2024, 2023, 2022])
selected_track = st.sidebar.selectbox("Select Track", [
    'Bahrain', 'Saudi Arabia', 'Australia', 'Japan', 'Miami', 
    'Imola', 'Monaco', 'Canada', 'Spain', 'Austria', 
    'Silverstone', 'Hungary', 'Spa', 'Zandvoort', 'Monza', 
    'Baku', 'Singapore', 'Austin', 'Mexico', 'Brazil', 
    'Las Vegas', 'Qatar', 'Abu Dhabi'
])

driver_list = ['VER', 'NOR', 'LEC', 'SAI', 'HAM', 'RUS', 'PIA', 'PER', 'ALO', 'STR', 'TSU', 'RIC', 'HUL', 'MAG', 'BOT', 'ZHO', 'ALB', 'SAR', 'GAS', 'OCO']

st.sidebar.markdown("---")
st.sidebar.write(f"**Target Event:** {selected_year} {selected_track}")

tab1, tab2, tab3 = st.tabs(["Lap-by-Lap Telemetry", "Tyre Degradation Engine", "Track Evolution Profile"])

# --- TAB 1: ADVANCED TELEMETRY (SPEED, THROTTLE, BRAKE) ---
with tab1:
    st.header(f"Driver Input Analysis: {selected_track} Qualifying")
    
    col1, col2 = st.columns(2)
    with col1: driver1 = st.selectbox("Select Driver 1", driver_list, index=0)
    with col2: driver2 = st.selectbox("Select Driver 2", driver_list, index=1)
    
    if st.button("Generate Telemetry", key="tel_btn"):
        with st.spinner(f"Fetching {selected_year} {selected_track} Data..."):
            try:
                session = fastf1.get_session(selected_year, selected_track, 'Q')
                session.load()
                
                d1_lap = session.laps.pick_drivers(driver1).pick_fastest()
                d2_lap = session.laps.pick_drivers(driver2).pick_fastest()
                d1_tel = d1_lap.get_car_data().add_distance()
                d2_tel = d2_lap.get_car_data().add_distance()
                
                st.markdown("### 📊 Session Statistics")
                kpi1, kpi2, kpi3, kpi4 = st.columns(4)
                
                d1_time = d1_lap['LapTime'].total_seconds()
                d2_time = d2_lap['LapTime'].total_seconds()
                time_delta = round(d1_time - d2_time, 3)
                
                kpi1.metric(label=f"{driver1} Lap Time", value=f"{d1_time:.3f}s", delta=f"{time_delta}s vs {driver2}", delta_color="inverse")
                kpi2.metric(label=f"{driver2} Lap Time", value=f"{d2_time:.3f}s")
                kpi3.metric(label=f"{driver1} Max Speed", value=f"{d1_tel['Speed'].max()} km/h")
                kpi4.metric(label=f"{driver2} Max Speed", value=f"{d2_tel['Speed'].max()} km/h")
                
                st.markdown("### 🏎️ Telemetry Traces")
                fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.05,
                                    subplot_titles=("Speed (km/h)", "Throttle (%)", "Brake Application"))
                
                fig.add_trace(go.Scatter(x=d1_tel['Distance'], y=d1_tel['Speed'], mode='lines', name=driver1, line=dict(color='#1f77b4')), row=1, col=1)
                fig.add_trace(go.Scatter(x=d2_tel['Distance'], y=d2_tel['Speed'], mode='lines', name=driver2, line=dict(color='#ff7f0e')), row=1, col=1)
                
                fig.add_trace(go.Scatter(x=d1_tel['Distance'], y=d1_tel['Throttle'], mode='lines', line=dict(color='#1f77b4'), showlegend=False), row=2, col=1)
                fig.add_trace(go.Scatter(x=d2_tel['Distance'], y=d2_tel['Throttle'], mode='lines', line=dict(color='#ff7f0e'), showlegend=False), row=2, col=1)
                
                fig.add_trace(go.Scatter(x=d1_tel['Distance'], y=d1_tel['Brake'], mode='lines', line=dict(color='#1f77b4'), showlegend=False), row=3, col=1)
                fig.add_trace(go.Scatter(x=d2_tel['Distance'], y=d2_tel['Brake'], mode='lines', line=dict(color='#ff7f0e'), showlegend=False), row=3, col=1)
                
                fig.update_layout(height=750, hovermode="x unified", margin=dict(l=50, r=50, t=40, b=40))
                fig.update_xaxes(title_text="Track Distance (meters)", row=3, col=1)
                
                st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error("Error mapping telemetry data. Ensure these drivers set valid lap times.")

# --- TAB 2: INTERACTIVE TYRE DEGRADATION ENGINE ---
with tab2:
    st.header(f"Stint Degradation Modeling: {selected_track} Race")
    col_deg, col_stint = st.columns(2)
    with col_deg: deg_driver = st.selectbox("Select Driver", driver_list, index=0, key="deg")
    with col_stint: stint_num = st.number_input("Select Stint Number", min_value=1, max_value=6, value=1)
    
    if st.button("Calculate Degradation Slope", key="deg_btn"):
        with st.spinner("Executing statistical regression..."):
            try:
                session = fastf1.get_session(selected_year, selected_track, 'R')
                session.load()
                laps = session.laps.pick_drivers(deg_driver).pick_quicklaps()
                stint = laps[laps['Stint'] == stint_num]
                
                if stint.empty: 
                    st.warning(f"No clean racing laps found for {deg_driver} in Stint {stint_num}.")
                else:
                    x = stint['TyreLife']
                    y = stint['LapTime'].dt.total_seconds()
                    m, b = np.polyfit(x, y, 1)
                    
                    st.metric(label="Calculated Degradation Rate", value=f"+{m:.3f} s/lap", help="Average time lost per lap due to compound wear.")
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=x, y=y, mode='markers', name='Actual Laps', marker=dict(color='#1f77b4', size=10)))
                    fig.add_trace(go.Scatter(x=x, y=m*x + b, mode='lines', name=f'Regression Slope (+{m:.3f}s)', line=dict(color='red', dash='dash')))
                    
                    fig.update_layout(xaxis_title="Tyre Age (Laps)", yaxis_title="Lap Time (Seconds)", hovermode="closest", height=500)
                    st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error("Error calculating degradation profile.")

# --- TAB 3: INTERACTIVE TRACK EVOLUTION ---
with tab3:
    st.header(f"Track Evolution Mapping: {selected_track} Qualifying")
    if st.button("Analyze Circuit Progression", key="evo_btn"):
        with st.spinner("Mapping timing sheets across Q1, Q2, and Q3..."):
            try:
                session = fastf1.get_session(selected_year, selected_track, 'Q')
                session.load()
                top_5 = session.results.head(5)
                
                fig = go.Figure()
                for index, driver in top_5.iterrows():
                    times = [driver['Q1'].total_seconds(), driver['Q2'].total_seconds(), driver['Q3'].total_seconds()]
                    fig.add_trace(go.Scatter(x=['Q1', 'Q2', 'Q3'], y=times, mode='lines+markers', name=driver['Abbreviation'], marker=dict(size=8)))
                
                fig.update_layout(xaxis_title="Qualifying Phase", yaxis_title="Lap Time (Seconds)", hovermode="x unified", height=500)
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error("Error loading track evolution patterns.")