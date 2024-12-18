from flask import Flask, render_template, request, redirect, url_for, flash
import Spotify
import youtube as yt
from googleapiclient.discovery import build

app = Flask(__name__)
app.secret_key = "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"  # Replace with your secret key

# Global variables for session data
spotify_tracks = []
youtube_playlist_id = None


@app.route("/")
def home():
    return render_template("home.html")

@app.route('/callback')
def callback():
    token_info = sp_oauth.get_access_token(request.args['code'])
    sp = spotipy.Spotify(auth=token_info['access_token'])
    # Now you can call sp.current_user_playlists() and other Spotify API methods
    return redirect('/spotify_playlists')



@app.route("/spotify_playlists", methods=["GET", "POST"])
def spotify_playlists():
    playlist_mapping = Spotify.get_spotify_playlists()

    if request.method == "POST":
        try:
            chosen_playlist_number = int(request.form["playlist_number"])
            if chosen_playlist_number in playlist_mapping:
                chosen_playlist = playlist_mapping[chosen_playlist_number]
                chosen_playlist_id = chosen_playlist["id"]
                playlist_name = chosen_playlist["name"]

                global spotify_tracks
                spotify_tracks = Spotify.get_spotify_playlist_tracks(chosen_playlist_id)
                return redirect(url_for("transfer_status", playlist_name=playlist_name))
            else:
                flash("Invalid playlist selection. Please try again.")
        except (ValueError, KeyError):
            flash("An error occurred. Please select a valid playlist.")

    return render_template("spotify_playlists.html", playlists=playlist_mapping)


@app.route("/transfer_status/<playlist_name>", methods=["GET", "POST"])
def transfer_status(playlist_name):
    if not playlist_name:
        flash("Playlist name not provided. Please try again.")
        return redirect(url_for("spotify_playlists"))

    if request.method == "POST":
        youtube_instance = yt.authenticate_youtube()
        global youtube_playlist_id
        youtube_playlist_id = create_youtube_playlist(youtube_instance, playlist_name)

        for track in spotify_tracks:
            track_name = track["name"]
            artist_names = track["artists"]
            video_id = search_youtube_track(youtube_instance, track_name, artist_names)
            if video_id:
                add_video_to_playlist(youtube_instance, youtube_playlist_id, video_id)

        return render_template("transfer_complete.html", youtube_playlist_id=youtube_playlist_id)

    return render_template("transfer_status.html", playlist_name=playlist_name, tracks=spotify_tracks)


@app.route("/transfer_complete")
def transfer_complete():
    return render_template("transfer_complete.html", youtube_playlist_id=youtube_playlist_id)


# Helper functions (YouTube interaction)
def search_youtube_track(youtube, track_name, artist_names):
    query = f"{track_name} {' '.join(artist_names)}"
    request = youtube.search().list(q=query, part="snippet", maxResults=1, type="video")
    response = request.execute()
    items = response.get("items", [])
    return items[0]["id"]["videoId"] if items else None


def create_youtube_playlist(youtube, playlist_name, description="Spotify Playlist"):
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": playlist_name,
                "description": description,
                "tags": ["Music", "Spotify", "Playlist"],
                "defaultLanguage": "en",
            },
            "status": {"privacyStatus": "private"},
        },
    )
    response = request.execute()
    return response["id"]


def add_video_to_playlist(youtube, playlist_id, video_id):
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {"kind": "youtube#video", "videoId": video_id},
            }
        },
    )
    return request.execute()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)  # Replace host and port as needed
