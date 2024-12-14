import Spotify
import youtube as yt
from googleapiclient.discovery import build

# Step 1: Fetch Spotify playlists and allow user selection
playlist_mapping = Spotify.get_spotify_playlists()

try:
    chosen_playlist_number = int(input("\nEnter the number of the Playlist to transfer: "))
    if chosen_playlist_number in playlist_mapping:
        chosen_playlist_id = playlist_mapping[chosen_playlist_number]
        spotify_tracks = Spotify.get_spotify_playlist_tracks(chosen_playlist_id)
        print("\nTracks:")
        print(spotify_tracks)
    else:
        print("Invalid playlist number.")
        exit()
except ValueError:
    print("Please enter a valid number.")
    exit()


youtube_instance = yt.authenticate_youtube()

# Function to search for a track on YouTube
def search_youtube_track(youtube, track_name, artist_names):
    query = f"{track_name} {' '.join(artist_names)}"
    request = youtube.search().list(
        q=query,
        part="snippet",
        maxResults=1,
        type="video"
    )
    response = request.execute()
    items = response.get("items", [])
    if items:
        return items[0]["id"]["videoId"]
    else:
        print(f"Could not find a match for: {query}")
        return None

# Function to create a new YouTube playlist
def create_youtube_playlist(youtube, playlist_name, description="Spotify Playlist"):
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": playlist_name,
                "description": description,
                "tags": ["Music", "Spotify", "Playlist"],
                "defaultLanguage": "en"
            },
            "status": {
                "privacyStatus": "private"
            }
        }
    )
    response = request.execute()
    return response["id"]

# Function to add a video to the YouTube playlist
def add_video_to_playlist(youtube, playlist_id, video_id):
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }
    )
    response = request.execute()
    return response

# Main logic to transfer playlist
def transfer_playlist_to_youtube(youtube, spotify_tracks, playlist_name):
    print(f"Creating YouTube playlist: {playlist_name}")
    youtube_playlist_id = create_youtube_playlist(youtube, playlist_name)
    print(f"Created YouTube Playlist ID: {youtube_playlist_id}")

    print("\nAdding tracks to YouTube playlist...")
    for track in spotify_tracks:
        track_name = track["name"]
        artist_names = track["artists"]

        print(f"\nSearching for: {track_name} by {', '.join(artist_names)}")
        video_id = search_youtube_track(youtube, track_name, artist_names)

        if video_id:
            print(f"Found video ID: {video_id}, adding to playlist...")
            add_video_to_playlist(youtube, youtube_playlist_id, video_id)
            print(f"Added: {track_name} by {', '.join(artist_names)}")
        else:
            print(f"Skipped: {track_name} by {', '.join(artist_names)}")

    print("\nPlaylist transfer complete!")
    print(f"YouTube Playlist URL: https://www.youtube.com/playlist?list={youtube_playlist_id}")

# Fetch the Spotify playlist name
spotify_playlist_name = Spotify.get_playlist_name(chosen_playlist_id)

# Transfer Spotify playlist to YouTube
transfer_playlist_to_youtube(youtube_instance, spotify_tracks, spotify_playlist_name)