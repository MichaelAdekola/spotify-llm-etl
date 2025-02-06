import streamlit as st
import pandas as pd
from spotify_pipeline.visualization.data_loader import load_data
from spotify_pipeline.visualization.charts import (
    top_artists_chart, top_songs_chart, listening_trends_chart,
    listening_heatmap, listening_by_hour_chart, weekly_listening_trends, track_repeat_frequency, session_length_distribution)

# Set Streamlit page title and layout
st.set_page_config(page_title="Spotify Listening Trends", layout="wide")

# Load data from SQLite database
df = load_data()

# Check if data is available
if df.empty:
    st.error("No data available. Please run the ETL pipeline first.")
else:
    # Display page title
    st.title("🎵 Spotify Listening Trends Dashboard")
    
    # Show basic summary metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Tracks Played", df.shape[0])
    
    with col2:
        st.metric("Unique Artists", df['artist'].nunique())
    
    with col3:
        st.metric("Unique Albums", df['album'].nunique())
    
    # Show raw data
    st.subheader("🎼 Recently Played Tracks")
    st.dataframe(df.head(10))

    # Visualizations
    st.subheader("📊 Top 10 Most Played Artists")
    st.plotly_chart(top_artists_chart(df), use_container_width=True)
    
    st.subheader("📊 Top 10 Most Played Songs")
    st.plotly_chart(top_songs_chart(df), use_container_width=True)
    
    st.subheader("📈 Daily Listening Trends")
    st.plotly_chart(listening_trends_chart(df), use_container_width=True)

    # Advanced Visualizations
    st.subheader("🔥 Listening Heatmap (Time of Day vs. Days of Week)")
    st.plotly_chart(listening_heatmap(df), use_container_width=True)
    
    st.subheader("🕒 Listening Habits by Hour of Day")
    st.plotly_chart(listening_by_hour_chart(df), use_container_width=True)
    
    st.subheader("📅 Weekly Listening Trends")
    st.plotly_chart(weekly_listening_trends(df), use_container_width=True)
    
    st.subheader("🔁 Track Repeat Frequency")
    st.plotly_chart(track_repeat_frequency(df), use_container_width=True)

    st.subheader("⏳ Listening Session Length Distribution")
    st.plotly_chart(session_length_distribution(df), use_container_width=True)

