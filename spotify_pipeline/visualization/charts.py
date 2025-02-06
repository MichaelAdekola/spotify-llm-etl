import streamlit as st
import pandas as pd
import plotly.express as px

# Function to generate top artists bar chart
def top_artists_chart(df):
    """
    Generate a bar chart showing the most played artists.
    """
    top_artists = df['artist'].value_counts().nlargest(10).reset_index()
    top_artists.columns = ['artist', 'play_count']
    fig = px.bar(top_artists, x='artist', y='play_count', title='Top 10 Most Played Artists',
                 labels={'artist': 'Artist', 'play_count': 'Play Count'}, color='play_count',
                 color_continuous_scale='blues')
    return fig

# Function to generate top songs bar chart
def top_songs_chart(df):
    """
    Generate a bar chart showing the most played songs.
    """
    top_songs = df.groupby(['name', 'artist']).size().nlargest(10).reset_index(name='play_count')
    fig = px.bar(top_songs, x='play_count', y='name', title='Top 10 Most Played Songs',
                 labels={'name': 'Song', 'play_count': 'Play Count'}, color='play_count',
                 color_continuous_scale='reds', orientation='h')
    return fig

# Function to generate listening trends line chart
def listening_trends_chart(df):
    """
    Generate a time-series chart showing daily listening trends.
    """
    df['played_at'] = pd.to_datetime(df['played_at'])
    daily_counts = df.groupby(df['played_at'].dt.date).size().reset_index(name='play_count')
    fig = px.line(daily_counts, x='played_at', y='play_count', title='Daily Listening Trends',
                  labels={'played_at': 'Date', 'play_count': 'Tracks Played'})
    return fig

# Function to generate a listening heatmap
def listening_heatmap(df):
    """
    Generate a heatmap showing listening patterns by hour and day of the week.
    """
    df['played_at'] = pd.to_datetime(df['played_at'])
    df['hour'] = df['played_at'].dt.hour
    df['day_of_week'] = df['played_at'].dt.day_name()
    
    heatmap_data = df.groupby(['day_of_week', 'hour']).size().reset_index(name='play_count')
    pivot_table = heatmap_data.pivot(index='day_of_week', columns='hour', values='play_count')
    pivot_table = pivot_table.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    
    fig = px.imshow(pivot_table, aspect='auto', color_continuous_scale='viridis',
                    title='Listening Heatmap: Time of Day vs. Days of the Week',
                    labels=dict(x='Hour of Day', y='Day of Week', color='Play Count'))
    return fig

# Function to generate listening habits by hour of day
def listening_by_hour_chart(df):
    """
    Generate a line chart showing the distribution of listening habits by hour of the day
    with more readable time labels.
    """
    df['played_at'] = pd.to_datetime(df['played_at'])
    df['hour'] = df['played_at'].dt.hour
    hourly_counts = df.groupby('hour').size().reset_index(name='play_count')
    
    # Convert numeric hours into readable time labels
    hour_labels = {0: '12 AM', 1: '1 AM', 2: '2 AM', 3: '3 AM', 4: '4 AM', 5: '5 AM', 6: '6 AM',
                   7: '7 AM', 8: '8 AM', 9: '9 AM', 10: '10 AM', 11: '11 AM', 12: '12 PM',
                   13: '1 PM', 14: '2 PM', 15: '3 PM', 16: '4 PM', 17: '5 PM', 18: '6 PM',
                   19: '7 PM', 20: '8 PM', 21: '9 PM', 22: '10 PM', 23: '11 PM'}
    hourly_counts['hour_label'] = hourly_counts['hour'].map(hour_labels)
    
    fig = px.line(hourly_counts, x='hour_label', y='play_count', title='Listening Habits by Hour of the Day',
                  labels={'hour_label': 'Time of Day', 'play_count': 'Tracks Played'})
    return fig

# Function to generate weekly listening trends
def weekly_listening_trends(df):
    """
    Generate a bar chart showing how listening frequency changes over the week.
    """
    df['played_at'] = pd.to_datetime(df['played_at'])
    df['day_of_week'] = df['played_at'].dt.day_name()
    weekly_counts = df['day_of_week'].value_counts().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    
    fig = px.bar(weekly_counts, x=weekly_counts.index, y=weekly_counts.values, 
                 title='Weekly Listening Trends', labels={'x': 'Day of Week', 'y': 'Tracks Played'},
                 color=weekly_counts.values, color_continuous_scale='blues')
    return fig

# Function to generate track repeat frequency
def track_repeat_frequency(df):
    """
    Generate a pie chart showing how often tracks are replayed.
    """
    repeat_counts = df['name'].value_counts().reset_index()
    repeat_counts.columns = ['track_name', 'play_count']
    top_repeats = repeat_counts.nlargest(5, 'play_count')
    
    fig = px.pie(top_repeats, names='track_name', values='play_count',
                 title='Top 5 Most Replayed Tracks',
                 color_discrete_sequence=px.colors.sequential.RdBu)
    return fig

# Function to generate listening session length distribution
def session_length_distribution(df):
    """
    Generate a histogram showing the distribution of listening session lengths.
    A session is defined as continuous listening with gaps of less than 30 minutes.
    """
    df['played_at'] = pd.to_datetime(df['played_at'])
    df = df.sort_values(by='played_at')
    
    df['time_diff'] = df['played_at'].diff().dt.total_seconds().div(60)
    df['new_session'] = df['time_diff'] > 30  # Mark sessions with >30 min gaps
    df['session_id'] = df['new_session'].cumsum()
    
    session_lengths = df.groupby('session_id')['played_at'].apply(lambda x: (x.max() - x.min()).seconds / 60)
    
    fig = px.histogram(session_lengths, nbins=20, title='Listening Session Length Distribution',
                        labels={'value': 'Session Length (Minutes)', 'count': 'Number of Sessions'},
                        color_discrete_sequence=['indigo'])
    return fig