import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

def get_writable_path(relative_path):
    """
    Ensures files are saved in the same directory as the .exe when bundled,
    or the project directory when running in an editor.
    """
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(base_path, relative_path)

class SpotifyControl:
    def __init__(self):
        cache_path = get_writable_path(".spotify_cache")
        
        load_dotenv(get_writable_path(".env"))
        
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        
        self.redirect_uri = "http://127.0.0.1:8888/callback"
        self.scope = "user-modify-playback-state user-read-playback-state"

        if self.client_id and self.client_secret:
            try:
                self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                    client_id=self.client_id,
                    client_secret=self.client_secret,
                    redirect_uri=self.redirect_uri,
                    scope=self.scope,
                    cache_path=cache_path,
                    open_browser=True
                ))
            except Exception as e:
                print(f"Authentication Error: {e}")
                self.sp = None
        else:
            self.sp = None

    def play_song(self, song_name: str):
        """Searches for a song on Spotify and plays it."""
        if not self.sp: 
            return "Spotify credentials are missing, Sir."
        
        try:
            results = self.sp.search(q=song_name, limit=1, type='track')
            if results['tracks']['items']:
                track_uri = results['tracks']['items'][0]['uri']
                track_title = results['tracks']['items'][0]['name']
                self.sp.start_playback(uris=[track_uri])
                return f"Playing {track_title} now, Sir."
            return "I couldn't find that track in the archives."
        except Exception as e:
            error_msg = str(e).lower()
            if "device" in error_msg:
                return "I found the song, but no active device is detected. Please open Spotify on your PC."
            if "premium" in error_msg:
                return "I'm afraid playback control requires a Spotify Premium account, Sir."
            return f"Spotify error: {str(e)}"

    def pause_music(self):
        """Pauses the currently playing track."""
        if not self.sp: return "Spotify offline."
        try:
            self.sp.pause_playback()
            return "Playback paused, Sir."
        except:
            return "No active session found to pause."

    def next_track(self):
        """Skips to the next track."""
        if not self.sp: return "Spotify offline."
        try:
            self.sp.next_track()
            return "Skipping to the next track."
        except:
            return "Unable to skip. Is the queue empty?"