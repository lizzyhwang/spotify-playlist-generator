import webbrowser
from urllib.parse import urlencode

# https://developer.spotify.com/dashboard
client_id = 'your_client_id'
client_secret = 'your_client_secret'

# spotify username
usrId = 'your_spotify_username'

auth_headers = {
    "client_id": client_id,
    "response_type": "code",
    "redirect_uri": "http://localhost:8888/callback",
    "scope": "playlist-modify-private ugc-image-upload"
}

# https://benwiz.com/blog/create-spotify-refresh-token/
refresh_token = 'your_refresh_token'