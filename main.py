from auth import SpotifyAuth
import requests
import json
import config
import random

def main():
    # Get Spotify authetication
    spAuth = SpotifyAuth()
    spAuth.get_new_token()

    # welcome message
    print("WELCOME TO EZ PLAYLIST GENERATOR")
    searchTerm = input("Enter 1-3 words to describe the vibe for your playlist. > ").lower().capitalize()
    
    try:
        print(f'Searching for {searchTerm} playlists...')
        r = requests.get(f'https://api.spotify.com/v1/search?q={searchTerm}&type=playlist&limit=50', headers={'Authorization': f'Bearer {spAuth.token}'}) 
    except:
        print(f'\033[31m Internal error while searching for playlists for: {searchTerm}')

    # save the request in a json
    data = r.json()

    # for each playlist, choose a random song
    song_uris = []
    print('Generating songs...')
    for p in data["playlists"]["items"]:
        song_uris.append(getRandomSpotifySongFromPlaylist(p["id"], spAuth))

    # initialize new playlist
    new_playlist_id = createSpotifyPlaylist(searchTerm, spAuth)
    # add all randomly chosen songs to playlist
    addSongsToSpotifyPlaylist(spAuth, new_playlist_id, song_uris)

    # end message
    print(f'Congratulations you just generated a new', searchTerm, 'playlist!')
    print(f'https://open.spotify.com/playlist/{new_playlist_id}')


# returns a random song uri (string) from a given playlist
def getRandomSpotifySongFromPlaylist(playlist_id: str, spAuth: SpotifyAuth):
    endpoint_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    r = requests.get(url = endpoint_url, headers={'Authorization': f'Bearer {spAuth.token}'})
    data = r.json()
    n = int(data["total"])
    idx = random.randint(0,n-1)

    # 100 limit on Spotify API
    if idx > 99:
        idx = 99

    return data["items"][idx]["track"]["uri"]


# return the playlist id (string)
def createSpotifyPlaylist(keyword: str, spAuth: SpotifyAuth):
    endpoint_url = f"https://api.spotify.com/v1/users/{config.usrId}/playlists"
    request_body = json.dumps({
            "name": "EZ PLAYLIST: " + keyword.capitalize(),
            "description": "Programmatically generated " + keyword.lower() + " playlist!",
            "public": False # let's keep it between us - for now
            })
    r = requests.post(url = endpoint_url, data = request_body, headers={'Content-Type':'application/json', 'Authorization': f'Bearer {spAuth.token}'})
    if r.status_code != 201:
        print("Error:", r.status_code)
    
    #return playlist id
    return r.json()['id']

# adds the list of songs to the given playlist
def addSongsToSpotifyPlaylist(auth: SpotifyAuth, target_playlist_id: str, song_uris: list): 
    num_added_songs = 0
    r = requests.put(f'https://api.spotify.com/v1/playlists/{target_playlist_id}/tracks',
                headers={
                    "Authorization": f'Bearer {auth.token}',
                    "Content-Type": "application/json"
                    }, 
                data=json.dumps({'uris': song_uris}))
    
    # Check if the request was successful and Print the output
    if(r.status_code == 201):
        num_added_songs += len(song_uris)

    # it should never get to this place
    if(len(song_uris) - num_added_songs > 0):
        print(f'\033[32m Could not find uris for {len(song_uris) - num_added_songs} songs')

main()