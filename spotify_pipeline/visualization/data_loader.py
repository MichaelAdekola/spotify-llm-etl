import sqlite3
import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_data(db_path="spotify_data.db"):
    """
    Load Spotify track data from SQLite into a Pandas DataFrame.
    :param db_path: Path to SQLite database file.
    :return: Pandas DataFrame containing track data.
    """
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        
        # Load track data into a DataFrame
        query = """
        SELECT id, name, artist, album, played_at 
        FROM tracks
        """
        df = pd.read_sql(query, conn)
        
        # Close the database connection
        conn.close()
        
        logging.info(f"✅ Successfully loaded {len(df)} records from database.")
        return df
    except Exception as e:
        logging.error(f"❌ Error loading data from database: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of failure

# Test loading data
if __name__ == "__main__":
    df = load_data()
    print(df.head())