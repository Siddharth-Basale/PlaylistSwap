import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import platform

# Spotify API credentials
SPOTIFY_CLIENT_ID = '770c44471ebe4c33828d0386301a5d70'
SPOTIFY_CLIENT_SECRET = '1e75e0fed7a643cfadd422c4960bdc75'
SPOTIFY_REDIRECT_URI = 'https://playlistswap-1.onrender.com'

# Define a unique cache path based on the device name
device_cache_path = f".cache-{platform.node()}"  # Unique cache for each device

# Clear the existing cache file to force re-authentication
if os.path.exists(device_cache_path):
    os.remove(device_cache_path)

# Set up Spotify authentication manager
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="playlist-read-private",
    cache_path=device_cache_path
))

# Function to get Spotify playlists for the authenticated user
def get_spotify_playlists():
    playlists = sp.current_user_playlists()
    playlist_mapping = {}
    for idx, playlist in enumerate(playlists['items'], start=1):
        playlist_mapping[idx] = {"id": playlist['id'], "name": playlist['name']}
    print("\nDebug: Fetched Playlists from Spotify API")  # Debug print
    print(playlist_mapping)  # Debug print
    return playlist_mapping

# Function to get tracks from a specific playlist
def get_spotify_playlist_tracks(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = []
    for item in results['items']:
        track = item['track']
        song_name = track['name']
        artists = [artist['name'] for artist in track['artists']]
        tracks.append({"name": song_name, "artists": artists})       
    return tracks

# New function to get the name of a specific playlist
def get_playlist_name(playlist_id):
    playlist = sp.playlist(playlist_id)
    return playlist['name']


if __name__ == "__main__":
    # Ensure user is logged in and playlists are fetched
    print("Authenticating Spotify...")
    playlists = get_spotify_playlists()
    print("Available Playlists:")
    for idx, playlist in playlists.items():
        print(f"{idx}: {playlist['name']}")

    # Further code to handle playlist selection, etc.
