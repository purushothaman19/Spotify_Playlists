from bs4 import BeautifulSoup
import requests
import spotify
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import json
from spotipy.oauth2 import SpotifyOAuth

date = input('Enter the date you wanna travel to (YYYY-MM-DD): ')
response = requests.get(f'https://www.billboard.com/charts/hot-100/{date}')
website = response.text

''' Getting the songs name using BeautifulSoup '''

soup = BeautifulSoup(website, 'html.parser')
# print(soup)

songs = [song.text for song in soup.find_all(class_="chart-element__information__song text--truncate color--primary")]
print(songs)

USERNAME = 'YOUR USERNAME'
SPOTIFY_CLIENT_ID = 'YOUR CLIENT ID'
SPOTIFY_CLIENT_SECRET = 'YOUR CLIENT SECRET'
REDIRECT_URI = 'http://example.com'
SCOPE = 'playlist-modify-public'
ACCESS_KEY = 'YOUR ACCESS KEY'


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        show_dialog=True,
        cache_path=".cache-XXX"
    )
)

''' Attaining the Song URIs '''

user_id = sp.current_user()["id"]
# print(user_id)

song_uris = []
year = date.split("-")[0]

for song in songs:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        # print(f"{song} doesn't exist in Spotify. Skipped.")
        pass

print(song_uris)

playlist = sp.user_playlist_create(user_id, name=f'{date} Top Songs', description='By python')

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
