import pyttsx3 as tts
import speech_recognition as sr
from thefuzz import fuzz
import time
import spotifyParser

import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_SECRET = '6c2fc5c27b0842af8fe97cc7ea26d944'
CLIENT_ID = '15dae62072ae4c4aae6c5bedc0e8f223'
REDIRECT_URI = 'http://localhost:8080'
# REDIRECT_URI = 'http://localhost'
ME = '31qiybto2ysdm2nlzlutsdud4nuq'

BASE_PROB = 80
UNRECOGNISED = 'unrecognised'


def stop():
    sp.pause_playback()
    print('stop')
    pass


def start():
    sp.start_playback()
    print('start')
    pass


def skip():
    print('skip')
    sp.next_track()
    pass


def prev():
    sp.previous_track()
    print('prev')
    pass


def author():
    curr = sp.current_playback()
    artist_id = curr['item']['artists'][0]['id']
    print(sp.artist(artist_id)['name'])
    pass


def album():
    curr = sp.current_playback()
    print(curr['item']['album']['name'])
    pass


def suggest():
    sp.shuffle(True)
    print('suggest')
    pass


def toPlaylist(arg):
    id = None
    for p in sp.current_user_playlists()['items']:
        if p['name'] == arg:
            id = p['id']

    if id == None:
        print("There's no such playlist")
        return

    curr = sp.current_playback()
    song_id = curr['item']['id']
    sp.playlist_add_items(id, song_id, position=None)
    print("add to playlist " + arg)
    pass


def toQueue(arg):
    uri = sp.search(arg, type='track')['tracks']['items'][0]['uri']
    sp.add_to_queue(uri)
    print("add to queue " + arg)
    pass


def removeFromPlaylist(arg):
    id = None
    for p in sp.current_user_playlists()['items']:
        if p['name'] == arg:
            id = p['id']

    if id == None:
        print("There's no such playlist")
        return

    curr = sp.current_playback()
    song_id = curr['item']['id']
    sp.playlist_remove_all_occurrences_of_items(id, song_id)
    print("remove from playlist " + arg)
    pass


def removeFromQueue(arg):
    print("remove from queue " + arg)
    pass


def lookFor(arg):
    names = [sp.search(arg, type='track')['tracks']['items'][i]['name'] for i in range(min(5,len(sp.search(arg, type='track')['tracks']['items'])))]
    for t in names:
        print(t)
        TTS.say(t)
    pass


def lookForBest(arg):
    print("look for best from " + arg)
    pass


def createPlaylist(arg):
    user_id = sp.me()['id']
    sp.user_playlist_create(user_id, arg, public=True, collaborative=False, description='Nowa playlista')
    print("create playlist " + arg)
    pass


def follow(arg):
    print("follow " + arg)
    pass


def unfollow(arg):
    artist_id = sp.search(arg, type='artist')['artists']['items'][0]['id']
    sp.user_unfollow_artists(id)
    print("unfollow " + arg)
    pass


def showDevices():
    devices = [sp.devices()['devices'][i]['name'] for i in range(len(sp.devices()['devices']))]
    for d in devices:
        print(d)
        TTS.say(d)
    pass


def suggestArtists():
    pass


to_func = {
    'stop': stop,
    'start': start,
    'skip': skip,
    'prev': prev,
    'author': author,
    'album': album,
    'suggest': suggest,
    "add to playlist": toPlaylist,
    "add to queue": toQueue,
    "remove from playlist": removeFromPlaylist,
    "remove from queue": removeFromQueue,
    "look for song": lookFor,
    "look for best songs": lookForBest,
    "create playlist": createPlaylist,
    "follow": follow,
    "unfollow": unfollow,
    "devices": showDevices,
    "suggest artists": suggestArtists
}

def parser(command):
    dict = {
        'zatrzymaj': 'stop', 'stop': 'stop', 'pauza': 'stop', 'pausa': 'stop',
        'start': 'start', 'graj': 'start', 'załącz muzyke': 'start', 'włącz muzyke': 'start',
        'skip': 'skip', 'przewiń': 'skip', 'skipnij': 'skip', 'następna piosenka': 'skip', 'następny utwór': 'skip','puść następną': 'skip','następne': 'skip', 'następna': 'skip',
        'prev': 'prev', 'poprzednia piosenka': 'prev', 'cofnij': 'prev', 'cofnij piosenkę': 'prev','cofnij utwór': 'prev',
        'author': 'author', 'kto śpiewa': 'author', 'autor': 'author', 'wykonawca': 'author','podaj wykonawcę': 'author',
        'album': 'album', 'jaki to album': 'album', 'podaj album': 'album', 'z jakiego album': 'album',
        'suggest': 'suggest', 'graj podobne utwory': 'suggest', 'zaproponuj piosenki': 'suggest', 'mixuj': 'suggest','mix': 'suggest','sugeruj':'suggest',
        'urządzenia': 'devices', 'jakie są dostępne urządzenia': 'devices','podaj moje urządzenia':'devices',
        'zaproponuj podobnych artystów': "suggest artists", "kto ma podobne piosenki": "suggest artists","podobni wykonawcy": "suggest artists","podobni": "suggest artists",
    }


    prob = 0
    which = UNRECOGNISED

    for key in dict:
        this_prob = fuzz.token_set_ratio(key, command)
        if this_prob >= BASE_PROB:
            if this_prob > prob:
                prob = this_prob
                which = key

    if which != UNRECOGNISED: return dict[which]
    return UNRECOGNISED

def asystent(command):
    task = parser(command)
    if task != UNRECOGNISED:
        to_func[task]()
    else:
        task,arg = spotifyParser.give_result(command)
        if task != UNRECOGNISED:
            to_func[task](arg)
        else: print('Niestety nie znam odpowiedzi')

    return "Już się robi szefie, zaraz wykonam " + command

def main():
    global TTS
    TTS = tts.init()
    TTS.setProperty('volume', 0.7)
    TTS.setProperty('rate', 190)

    STT = sr.Recognizer()

    print('''Napisz pytanie i naciśnij Enter albo naciśnij Enter i zadaj pytanie.''')
    while True:
        tekst = input(">>")
        if len(tekst) > 0:
            odp = asystent(tekst)
            # TTS.say(odp)
            TTS.runAndWait()

        else:
            with sr.Microphone() as source:
                print("slucham ...")
                audio = STT.listen(source)
                try:
                    tekst = STT.recognize_google(audio, language='pl_PL')
                    print(tekst)
                    odp = asystent(tekst)
                    TTS.say(odp)
                    TTS.runAndWait()

                except sr.UnknownValueError:
                    print('nie rozumiem')
                except sr.RequestError as e:
                    print('error:', e)


if __name__ == '__main__':
    scope = ["user-read-playback-state", "user-modify-playback-state", "app-remote-control", "streaming"]
    TTS = None
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=CLIENT_ID, client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URI))

    main()
