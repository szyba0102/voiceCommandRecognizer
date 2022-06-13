import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_SECRET = '6c2fc5c27b0842af8fe97cc7ea26d944'
CLIENT_ID = '15dae62072ae4c4aae6c5bedc0e8f223'
REDIRECT_URI = 'http://localhost:8080'
# REDIRECT_URI = 'http://localhost'
ME = '31qiybto2ysdm2nlzlutsdud4nuq'
FILIP = '214dqcdo3i2h54jy3mwvztriy'

from spotipy.oauth2 import SpotifyClientCredentials

# auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID,client_secret=CLIENT_SECRET)
# sp = spotipy.Spotify(auth_manager=auth_manager)

# user = sp.user(FILIP)
# print(user)
# playlists = sp.user_playlists(FILIP)
#
# while playlists:
#     for i, playlist in enumerate(playlists['items']):
#         print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
#     if playlists['next']:
#         playlists = sp.next(playlists)
#     else:
#         playlists = None

# scope = "user-read-playback-state"
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URI))

# scope = "streaming"
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URI))

scope = ["user-read-playback-state","user-modify-playback-state","app-remote-control","streaming"]
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URI))

# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URI))
#
curr = sp.current_playback()
#
artist_id = curr['item']['artists'][0]['id']
print(curr['item']['album']['name'])
#
print(sp.artist(artist_id)['name'])

# sp.next_track()
# print(sp.search("Sundress",type='track')['tracks']['items'])

# print(sp.search("Sundress",type='track')['tracks']['items'][0]['uri'])


#
# # sp.add_to_queue('2aPTvyE09vUCRwVvj0I8WK')
# sp.next_track()
# sp.previous_track()
arg = "H"
# for p in sp.current_user_playlists()['items']:
#     if p['name'] == arg:
#         print(p['id'])

# print(sp.current_user_playlists()['items'])

curr = sp.current_playback()
print(curr['item']['id'])