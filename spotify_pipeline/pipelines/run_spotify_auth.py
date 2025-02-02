import logging

from spotify_pipeline.resources.spotify_auth import SpotifyAuth


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s  - %(message)s")


def main():
    try:
        # create the authentication object
        auth = SpotifyAuth()

        #retrieve access token
        access_token = auth.get_access_token()

        #print and log access token
        logging.info(f"Spotify Acess Token: {access_token}")


    except Exception as e: 
        logging.error(f"Error occure while fetching Spotify access token: {e}")




if __name__ == "__main__":
    main()


