import requests
import os
from spotify_pipeline.resources.spotify_auth import SpotifyAuth
from spotify_pipeline.models.spotify_models import SessionLocal, Track
import logging
import pandas as pd


# set up logging config

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s  - %(message)s")

class SpotifyData:
    BASE_URL = "https://api.spotify.com/v1/me/player/recently-played"

    def __init__(self):
        """initialise with authentication"""
        self.auth = SpotifyAuth()
        self.access_token = self.auth.access_token


    def get_recently_played(self, limit=50, max_tracks=10000):
        """
        :param limit: Number of tracks to fetch
        :return: JSON response containing track data
        """
        
        all_tracks = []

        if not self.auth.is_token_valid():
            logging.info("Refreshing expired token before fetching tracks....")
            self.access_token = self.auth.refresh_access_token


        headers = {"Authorization": f"Bearer {self.access_token}"}
        params = {"limit": limit}
        next_url = self.BASE_URL

        logging.info("Fetching recently played tracks with pagination....")

        while next_url and len(all_tracks) < max_tracks:
            try:
                response = requests.get(self.BASE_URL, headers=headers, params=params)

                if response.status_code == 200:
                    data = response.json()
                    fetched_tracks = data["items"]
                    all_tracks.extend(fetched_tracks)


                    logging.info(f"Fetched {len(fetched_tracks)} tracks. Total so far: {len(all_tracks)}.")

                    next_url = data.get("next")

                    #stop fetching after 10000 tracks

                    if len(all_tracks) >= max_tracks:
                        logging.info("Reached track limit. Stopping Pagination")
                        break

                    #next_url = data.get("next")

                    if not next_url:
                        logging.info("No more pages to fetch. Pagination complete")

                else:
                    logging.error(f"Error fetching data: {response.status_code} - {response.text}")
                    break


            except requests.exceptions.RequestException as e:
                logging.error(f"Request failed: {e}")
                break

        logging.info(f"Finished fetching tracks. Total retrieved: {len(all_tracks)}.")

        # convert to data_frame

        df = self.store_tracks_in_dataframe(all_tracks)
        return df



    def store_tracks_in_dataframe(self, tracks):
        """
        convert fetched tracks into a pandas dataframe
        """

        if not tracks:
            logging.warning("No tracks available to store in Dataframe.")
            return pd.DataFrame()
        
        # convert track data into a structured data

        track_data = [
            {
                "track_id": track["track"]["id"],
                "track_name": track["track"]["name"],
                "artist_name": track["track"]["artists"][0]["name"],
                "album_name": track["track"]["album"]["name"],
                "played_at": track["played_at"]

            }
            for track in tracks
        ]

        df = pd.DataFrame(track_data)

        logging.info(f"Total records fetched: {len(df)}")

        # Check for missing values
        missing_values = df.isnull().sum().sum()
        if missing_values > 0:
            logging.warning(f"Missing value found: {missing_values}")

        # Check for duplicates on track_id + played_at
        duplicate_count= df.duplicated(subset=["track_id", "played_at"]).sum()
        if duplicate_count > 0:
            logging.warning(f"Duplicate records found: {duplicate_count}")

        # Display summary stats
        logging.info(f"Unique tracks: {df['track_id'].nunique()}")
        logging.info(f"Top 5 artists:\n{df['artist_name'].value_counts().head()}")

        # Show first 5 records
        logging.info(f"Displaying first 5 records:\n{df.head()}")

        return df


    # def get_audio_features(self, track_id):
    #     """
    #     Fetch audio features of the tacks such as energy, dancability etc
    #     """

    #     url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    #     headers = {"Authorization": f"Bearer {self.access_token}"}

    #     response = requests.get(url, headers=headers)

    #     if response.status_code == 200:
    #         return response.json()
        
    #     else:
    #         logging.error(f"Error fetching audio features for {track_id}: {response.status_code}")
            
    #         return None
        
    def save_track_data(self, df):
        """
        saves tracks into database
        """

        session = SessionLocal()

        for _, row in df.iterrows():
            track_obj = Track(
                id=row["track_id"],
                name=row["track_name"],
                artist=row["artist_name"],
                album=row["album_name"],
                played_at=row["played_at"]
            )
            session.merge(track_obj)   #avoids duplicates
        session.commit
        session.close()
        logging.info(f" {len(df)} tracks saved to database.")


    # def save_audio_features(self, track_id, features):
    #     """
    #     save audio features into database
    #     """

    #     session = SessionLocal()
    #     feature_obj = AudioFeature(
    #         track_id=track_id,
    #         danceability=features["danceability"],
    #         energy=features["energy"],
    #         valence=features["valence"],
    #         tempo=features["tempo"]

    #     )
    #     session.merge(feature_obj)
    #     session.commit()
    #     session.close()
    #     logging.info(f" Audio features saved for track {track_id}.")