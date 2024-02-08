# Python Script for Generating Spotify Playlists!

## Overview

A script designed to generate a Spotify playlist in your Spotify account, given a short description.

## Setup

To use the script, follow the steps below:

1. Install dependencies with `pip install -r requirements.txt`.

2. Create a `config.py` file in the root directory. You clone the `config.template.py` file to do so.

3. Create your own Spotify application at https://developer.spotify.com/dashboard and set the Callback URL to `http://localhost:8080` (or another local port of your choice). Then fill in the `client_id` and `client_secret` from your new application into the `config.py` file.
``` python
# https://developer.spotify.com/dashboard
client_id = 'xxx'
client_secret = 'xxx'
```

4. Get your own refresh token using your application and this tutorial:  https://benwiz.com/blog/create-spotify-refresh-token/ and add it to the `refresh_token` in `config.py`. Make sure to set the $SCOPE during the tutorial to `playlist-modify-private`.

``` python
# https://benwiz.com/blog/create-spotify-refresh-token/
refresh_token = 'xxx'
```

5. Create the Spotify playlists you want to mirror and fill in the information in `config.py`.
``` python
# https://open.spotify.com/playlist/4C0kEXdGkLuIDaBSVRjwpr?...
#                                           ^ This is the playlist id
playlists = [
    {
        'applemusic_playlist_url': 'https://music.apple.com/us/playlist/xxx/pl.xxx',
        'spotify_playlist_id': 'xxx',
    },
    {
        'applemusic_playlist_url': 'https://music.apple.com/us/playlist/xxx/pl.xxx',
        'spotify_playlist_id': 'xxx',
    },
]
```

6. Start the script using `python3 main.py` in the terminal. The application will start mirroring all the playlists once. If you want to do this regularly, you can set up a scheduler like cron to run the script.

7. Feel free to enable debug mode in the config if you want to see why songs are not matching.
 ``` python
debug = True
```   


## ToDo (Please Send a PR, in case you anything)

The following tasks still need to be completed:

1. Cloning of image and description of playlists
