import logging
from spotify_pipeline.resources.spotify_data import SpotifyData
import pandas as pd


# set up logging config

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s  - %(message)s")

def main():
    spotify_data = SpotifyData()
    df = spotify_data.get_recently_played(limit=50)

    if not df.empty:
        logging.info(f"Storing {len(df)} tracks in database...")
        spotify_data.save_track_data(df)


        # logging.info("Fetching and storing audio features for tracks...")

        # for _, row in df.iterrows():
        #     track_id = row["track_id"]
        #     features = spotify_data.get_audio_features(track_id)


        #     if features:
        #         spotify_data.save_audio_features(track_id, features)
        #         logging.info (f"🎵 Audio features saved for {track_id}.")

        #     else:
        #         logging.warning(f" No audio features found for {track_id}.")


if __name__ == "__main__":
    main()
