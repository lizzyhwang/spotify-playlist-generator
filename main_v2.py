from auth import SpotifyAuth
import requests
import json
import config
import random
import base64
import pinterest

# main_v2.py
# goal: better, more cohesive playlist because we take multiple songs from the same playlist
# searches for 10 playlists (presumably the top 10), divides each into groups of 10 songs.
# from each group of 10 songs, choose one song at random.
# add all of the randomly gathered songs to a playlist in your Spotify account
# prints out the final playlist
# returns the link to your new playlist!

def main():
    # Get Spotify authetication
    spAuth = SpotifyAuth()
    spAuth.get_new_token()

    # welcome message
    print("WELCOME TO EZ PLAYLIST GENERATOR V2")
    searchTerm = input("Enter 1-3 words to describe the vibe for your playlist. > ").lower()
    
    try:
        print(f'Searching through {searchTerm} playlists...')
        r = requests.get(f'https://api.spotify.com/v1/search?q={searchTerm}&type=playlist&limit=10', headers={'Authorization': f'Bearer {spAuth.token}'}) 
    except:
        print(f'\033[31m Internal error while searching for playlists relating to: {searchTerm}')

    # save the request in a json
    data = r.json()

    # for each playlist, choose a random song
    song_uris = [] # list of list of song_uris
    print('Generating songs...')
    for p in data["playlists"]["items"]:
        song_uris.append(getRandomSongsFromSpotifyPlaylist(p["id"], spAuth))

    # initialize new playlist
    new_playlist_id = createSpotifyPlaylist(searchTerm, spAuth)

    # commenting out: spotify api is not liking playlist cover calls
    addPlaylistCover(searchTerm, new_playlist_id, spAuth)
    if new_playlist_id != "":
        # add all randomly chosen songs to playlist
        addSongsToSpotifyPlaylist(spAuth, new_playlist_id, song_uris)

    print(listNameandArtistFromSpotifyPlaylist(new_playlist_id, spAuth))

    # end message
    print(f'Congratulations, you just generated a new', searchTerm, 'playlist!')
    print(f'https://open.spotify.com/playlist/{new_playlist_id}')

# returns a string containing the list of all song titles with the artist.
def listNameandArtistFromSpotifyPlaylist(playlist_id: str, spAuth: SpotifyAuth):
    endpoint_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    r = requests.get(url = endpoint_url, headers={'Authorization': f'Bearer {spAuth.token}'})
    data = r.json()

    n = int(data["total"])
    songs = ""
    if n < 100:
        for i in range (0,n):
            name = data["items"][i]["track"]["name"]
            artist = data["items"][i]["track"]["artists"][0]["name"]
            songs += f'{i+1}. {name} - {artist}\n'
    else:
        return("This playlist is huge! Click the link to view the whole playlist.")
    
    return songs

# returns a list of random song uris (strings) from a given playlist
def getRandomSongsFromSpotifyPlaylist(playlist_id: str, spAuth: SpotifyAuth):
    endpoint_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    r = requests.get(url = endpoint_url, headers={'Authorization': f'Bearer {spAuth.token}'})
    data = r.json()

    n = int(data["total"])
    playlist_chunks = [data["items"][i:i+10] for i in range(0, n, 10)]

    chosen_songs = [] # list of song_uris (string)
    for song_list in playlist_chunks:
        s = max(len(song_list) - 1, 0)
        if s != 0:
            idx = random.randint(0,s)
            chosen_songs.append(song_list[idx]["track"]["uri"])

    return chosen_songs


# return the playlist id (string) of new playlist
def createSpotifyPlaylist(keyword: str, spAuth: SpotifyAuth):
    # create the playlist
    endpoint_url = f"https://api.spotify.com/v1/users/{config.usrId}/playlists"
    request_body = json.dumps({
            "name": "EZ PLAYLIST: " + keyword,
            "description": "Programmatically generated " + keyword + " playlist!",
            "public": False # let's keep it between us - for now
            })
    r = requests.post(url = endpoint_url, data = request_body, headers={'Content-Type':'application/json', 'Authorization': f'Bearer {spAuth.token}'})
    if r.status_code != 201:
        print("Error creating playlist:", r.status_code)
        return ""

    #return playlist id
    return r.json()['id']

def addPlaylistCover(searchTerm: str, playlistId: str, spAuth: SpotifyAuth):
    pinterest.getPlaylistCoverImage(searchTerm)
    endpoint_url = f"https://api.spotify.com/v1/playlists/{playlistId}/images"
    print(endpoint_url)
    filename = searchTerm.replace(" ", "_") + "_playlist_cover.jpeg"
    print(filename)
    filepath = "images/" + filename
    with open(filepath, "rb") as f:
        data = base64.b64encode(f.read().strip())
    r = requests.put(url=endpoint_url, data=data, headers={'Content-Type':'image/jpeg', 'Authorization': f'Bearer {spAuth.token}'})
    if r.status_code != 202:
            print("Error uploading playlist cover:", r.status_code)

# adds the list of songs (list of list of song_uris) to the given playlist
def addSongsToSpotifyPlaylist(auth: SpotifyAuth, target_playlist_id: str, song_uris: list): 
    r = requests.put(f'https://api.spotify.com/v1/playlists/{target_playlist_id}/tracks',
                headers={
                    "Authorization": f'Bearer {auth.token}',
                    "Content-Type": "application/json"
                    }, 
                data=json.dumps({'uris': song_uris[0]}))
    
    for i in range(1,10):
        r = requests.post(f'https://api.spotify.com/v1/playlists/{target_playlist_id}/tracks',
                    headers={
                        "Authorization": f'Bearer {auth.token}',
                        "Content-Type": "application/json"
                        }, 
                    data=json.dumps({'uris': song_uris[i]}))
    
    # Check if the request was successful and Print the output
    if(r.status_code == 201):
        print('Playlist complete!')



main()