# spotify.py
import spotipy
import time
import os

from spotipy.oauth2 import SpotifyOAuth
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI

# Create the Spotify API object with authentication
scope = "user-read-playback-state,user-modify-playback-state"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                               client_secret=SPOTIFY_CLIENT_SECRET,
                                               redirect_uri=SPOTIFY_REDIRECT_URI,
                                               scope=scope))

def open_spotify_and_play_music():
    # Open Spotify
    os.system('open -a "Spotify"')
    time.sleep(3)
    # Your Spotify track URI or playlist URI (replace with your desired track or playlist)
    # For example, a track URI: "spotify:track:6rqhFgbbKwnb9MLmUQDhG6"
    # Or a playlist URI: "spotify:playlist:37i9dQZF1DWXRqgorJj26U"
    track_uri = "spotify:track:2QophXhN2Ls2URfoPmiviC"
    selected_device_id = 'c0f2fc0c413e4f5bda3579e7eefee17d6607b3f3'
    sp.transfer_playback(device_id=selected_device_id, force_play=True)
    # Play the track or playlist
    sp.start_playback(uris=[track_uri])
    time.sleep(5)
    sp.pause_playback()