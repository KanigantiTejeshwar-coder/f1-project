# 🏎️ Production-Grade Formula 1 Telemetry Engine

A full-stack, data-driven web application that pulls live motorsport data streams, processes fine-grained timeline mechanics, and exposes an interactive data visualization layout for racing engineers and analysts.

🔗 **[Launch Live Interactive Dashboard](https://f1-project-gfkrn8wb7xudaye5h9sjpt.streamlit.app/)**

---

## 📊 Core Features

### 1. Lap-by-Lap Telemetry Analysis
* Compares head-to-head lap data for any two selected drivers during a Grand Prix weekend.
* Synchronizes multiple time-series graphs (**Speed, Throttle position, and Brake applications**) across a single, unified distance baseline.
* Implements client-side crosshair tracking for micro-second precision corner analysis.

### 2. Predictive Tyre Degradation Engine
* Pulls continuous lap times throughout individual race stints.
* Executes a **NumPy linear regression modeling sequence** to calculate the precise degradation slope coefficient in seconds lost per lap.

### 3. Track Evolution Profile
* Evaluates historical timing sheets chronologically across Q1, Q2, and Q3 segments.
* Tracks circuit optimization dynamics and grip progression as rubber sets into the track surface.

---

## 🛠️ Tech Stack & Architecture

* **Language Layer:** Python 3 (Optimized for vector math arrays)
* **Data Processing Pipeline:** `pandas` (DataFrame aggregation), `numpy` (Statistical modeling), `FastF1` (API telemetry synchronization wrapper)
* **Web UI Runtime Engine:** Streamlit Framework
* **Visualization Layer:** Plotly.js (Client-side interactive vector graphics)

### System Data Flow Layout
```text
[FastF1 API Streams] ──> [Local File Caching] ──> [Pandas Matrix Vectorization] 
                                                               │
[Interactive Plotly.js Component] <── [WebSocket State Sync] ──┘
