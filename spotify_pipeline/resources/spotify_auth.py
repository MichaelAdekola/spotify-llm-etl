import os
import requests
import webbrowser
import logging
from dotenv import load_dotenv, set_key


load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s  - %(message)s")


class SpotifyAuth:
    AUTH_URL = "https://accounts.spotify.com/api/token"
    AUTH_REDIRECT_URI = "http://localhost:8888/callback"
    ENV_FILE = ".env"

    def __init__(self):
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.access_token = os.getenv("SPOTIFY_ACCESS_TOKEN")
        self.refresh_token = os.getenv("SPOTIFY_REFRESH_TOKEN")

        #check if token has expired (returns None)
        if not self.access_token or not self.is_token_valid():
            logging.info("Access token expired. Refreshing token...")
            self.access_token = self.refresh_access_token()

    
    def is_token_valid(self):

        """
        checks if the current access token is valid 
        """

        test_url = "https://api.spotify.com/v1/me"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(test_url, headers= headers)

        if response.status_code == 401:
            logging.warning("Access token is expired.")
            return False
        return True

        

    def get_auth_url(self):

        """
        Generates a url for authorization (OAuth2)
        """
        scope = "user-read-recently-played user-top-read"
        auth_url = (
            f"https://accounts.spotify.com/authorize"
            f"?client_id={self.client_id}"
            f"&response_type=code"
            f"&redirect_uri={self.AUTH_REDIRECT_URI}"
            f"&scope={scope}"
        )
        return auth_url
    
    def request_user_token(self, auth_code):

        """
        Exchange auth code for access token
        """

        response = requests.post(
            self.AUTH_URL,
            data={
                "grant_type": "authorization_code",
                "code": auth_code,
                "redirect_uri": self.AUTH_REDIRECT_URI,
                "client_id": self.client_id,
                "client_secret": self.client_secret
            },
        )
        response_data = response.json()
        if response.status_code == 200:
            self.access_token = response_data["access_token"]
            self.refresh_token = response_data["refresh_token"]

            #store token in .env file
            set_key(self.ENV_FILE, "SPOTIFY_ACCESS_TOKEN", self.access_token)
            set_key(self.ENV_FILE, "SPOTIFY_REFRESH_TOKEN", self.refresh_token)


            return self.access_token
        else: 
            logging.error(f"Error fetching access token: {response_data}")

            return None
        


    def refresh_access_token(self):
        """
        Refresh the access token once expired
        """

        if not self.refresh_token: 
            logging.error("No refresh token found. Please re-authenticate")
            return None
        


        response = requests.post(
            self.AUTH_URL,
            data={
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token,
                "redirect_uri": self.AUTH_REDIRECT_URI,
                "client_id": self.client_id,
                "client_secret": self.client_secret
            },

        )


        response_data = response.json()

        if response.status_code == 200:
            self.access_token = response_data["access_token"]
            set_key(self.ENV_FILE, "SPOTIFY_ACCESS_TOKEN", self.access_token)
            logging.info("Spotify access token refreshed successfully")
            return self.access_token
        
        else:
            logging.error(f"Error refreshing access token: {response_data}")
            
            return None


    