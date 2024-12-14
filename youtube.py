import google_auth_oauthlib.flow
import googleapiclient.discovery


YOUTUBE_CLIENT_SECRETS_FILE = 'client_secrets.json'
SCOPES = ['https://www.googleapis.com/auth/youtube']


def authenticate_youtube():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        YOUTUBE_CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=8080)
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)
    return youtube


