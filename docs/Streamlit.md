# 📈 Streamlit Dashboard Documentation

## 📌 Overview
The Streamlit dashboard provides **interactive visualizations** of Spotify listening history. It loads data from a **SQLite database** and presents insights into listening habits, most played artists, session durations, and more.

---

## 🚀 How to Run the Streamlit Dashboard

### 1️⃣ Ensure Dependencies Are Installed
Before running Streamlit, ensure that the required dependencies are installed:
```bash
pip install -r requirements.txt
```
### 2️⃣ Run the Dashboard
```bash
streamlit run spotify_pipeline/visualization/streamlit_app.py
```
✅ This will start a local web server and open the dashboard in your browser at http://localhost:8501
---

## 📊 Available Visualizations

### 🎧 **Top 10 Most Played Artists**
- Displays the **most frequently played artists**.
- Helps analyze **listening preferences** over time.

### 🎼 **Top 10 Most Played Songs**
- Highlights the **most played tracks**.
- Identifies **repeat listening behavior**.

### 📈 **Daily Listening Trends**
- Shows **how many tracks** were played each day.
- Useful for spotting **listening patterns over time**.

### 🔥 **Listening Heatmap** (Time of Day vs. Days of Week)
- Reveals **when you listen the most** during the day.
- Helps identify **peak listening hours**.

### 🕒 **Listening Habits by Hour of Day**
- Tracks **what time of day you listen to music most**.
- Uses a **line chart** for better trend analysis.

### 📅 **Weekly Listening Trends**
- Displays listening frequency across **different days of the week**.
- Helps in understanding **weekday vs. weekend habits**.

### ⏳ **Listening Session Length Distribution**
- Shows how long your **listening sessions** last.
- Helps track **short vs. long music sessions**.