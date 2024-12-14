import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify API credentials
SPOTIFY_CLIENT_ID = '770c44471ebe4c33828d0386301a5d70'
SPOTIFY_CLIENT_SECRET = '1e75e0fed7a643cfadd422c4960bdc75'
SPOTIFY_REDIRECT_URI = 'http://localhost:8080/callback'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="playlist-read-private"
))

def get_spotify_playlists():
    playlists = sp.current_user_playlists()
    playlist_mapping = {}
    print("\nAvailable Playlists:")
    for idx, playlist in enumerate(playlists['items'], start=1):
        print(f"{idx}. {playlist['name']} - {playlist['id']}")
        playlist_mapping[idx] = playlist['id']
    return playlist_mapping

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