from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv(dotenv_path="app/.env")

# Spotify OAuth setup
sp_oauth = SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    scope="user-top-read playlist-modify-public playlist-modify-private",
    show_dialog=True,
    cache_handler=None
)


def get_auth_url():
    return sp_oauth.get_authorize_url()


def get_access_token(code: str):
    token_info = sp_oauth.get_access_token(code, check_cache=False)
    return token_info["access_token"]



