# Python Script for Generating Spotify Playlists!

## Overview

A script designed to generate a Spotify playlist in your Spotify account, given a short description.

## Credit

This project was heavily based off of https://github.com/aikozim/applemusic-playlist-to-spotify.  I reused and modified their configuration and build process (`requirements.txt`, `README`, and `config.template.py`).  I also used their `SpotifyAuth` class, and used their main methods as a starting point for mine.

Additional References:  
* https://medium.com/analytics-vidhya/build-your-own-playlist-generator-with-spotifys-api-in-python-ceb883938ce4
* https://developer.spotify.com/documentation/web-api

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

5. Start the script using `python3 main_v2.py` in the terminal.