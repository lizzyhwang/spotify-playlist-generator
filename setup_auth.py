import webbrowser
from urllib.parse import urlencode
import config

webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(config.auth_headers))