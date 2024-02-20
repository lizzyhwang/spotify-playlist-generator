# Python Script for Generating Spotify Playlists!

## Overview

A script designed to crowdsource a Spotify playlist in your Spotify account, given a short description.  It also scrapes Pinterest and adds a cover image to the new playlist.

## Credit

This project was based off of
* https://github.com/aikozim/applemusic-playlist-to-spotify
* https://github.com/robertomape/PinterestImageScraper/blob/main/pinterestscraper.py.

Additional References:  
* https://medium.com/analytics-vidhya/build-your-own-playlist-generator-with-spotifys-api-in-python-ceb883938ce4
* https://developer.spotify.com/documentation/web-api
* https://benwiz.com/blog/create-spotify-refresh-token/
* https://python.plainenglish.io/bored-of-libraries-heres-how-to-connect-to-the-spotify-api-using-pure-python-bd31e9e3d88a

## Setup

To use the script, follow the steps below:

1. Install dependencies with `pip3 install -r requirements.txt`.

2. Create a `config.py` file in the root directory. Clone `config.template.py` file to do so.

3. Create your own Spotify application at https://developer.spotify.com/dashboard and set the Callback URL to `http://localhost:8888`. Then fill in the `client_id` and `client_secret` from your new application into both your `config.py` file and the `config_env.sh` file.
``` python
# in config.py
client_id = 'xxx'
client_secret = 'xxx'
```
``` sh
# in config_env.py
export CLIENT_ID='xxx'
export CLIENT_SECRET='xxx'
```

4. Run `python3 setup_auth.py`. It should open a new browser window with a url like `http://localhost:8888/callback?code=AQDBlahBlahBlah`.  The random string after '`code=`' is your code.  Copy that part of the URL and paste it into `config_env.sh`:
```sh
# in config_env.sh
export CODE='xxx'
```

5. Run `sh config_env.sh`

6. Run `curl -d client_id=$CLIENT_ID -d client_secret=$CLIENT_SECRET -d grant_type=authorization_code -d code=$CODE -d redirect_uri=$REDIRECT_URI https://accounts.spotify.com/api/token`.  
It should return a JSON object that looks like this:
```
{
    "access_token": "$ACCESS_TOKEN",
    "token_type": "Bearer",
    "expires_in": 3600,
    "refresh_token": "$REFRESH_TOKEN",
    "scope": "playlist-modify-private ugc-image-upload"
}
```
Copy the `refresh_token` and paste it into the `config.py` file.
``` python
# in config.py
refresh_token = 'your_refresh_token'
```

7. Start the script by running `python3 main_v2.py`