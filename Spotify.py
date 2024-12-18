import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import platform
from flask import redirect, request, session, url_for

# Spotify API credentials
SPOTIFY_CLIENT_ID = '770c44471ebe4c33828d0386301a5d70'
SPOTIFY_CLIENT_SECRET = '1e75e0fed7a643cfadd422c4960bdc75'
SPOTIFY_REDIRECT_URI = 'https://playlistswap-1.onrender.com/callback'  # Ensure this is the same URI in Spotify dashboard

# Define a unique cache path based on the device name
device_cache_path = f".cache-{platform.node()}"  # Unique cache for each device

# Set up Spotify authentication manager
sp_oauth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="playlist-read-private user-library-read",
    cache_path=device_cache_path
)

sp = spotipy.Spotify(auth_manager=sp_oauth)


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


# Flask routes to handle authentication
from flask import Flask, redirect, request, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For session handling, replace with a strong key

@app.route('/spotify_playlists')
def spotify_playlists():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    # This route will be hit when Spotify redirects back
    token_info = sp_oauth.get_access_token(request.args['code'])
    sp = spotipy.Spotify(auth=token_info['access_token'])

    # Store the access token in the session for future use
    session['token_info'] = token_info

    # Now you can use 'sp' to interact with Spotify API
    playlists = get_spotify_playlists()
    return render_template('playlists.html', playlists=playlists)

if __name__ == "__main__":
    app.run(debug=True)
