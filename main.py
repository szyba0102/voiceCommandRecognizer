import pyttsx3 as tts
import speech_recognition as sr
from thefuzz import fuzz
import time
import spotifyParser

import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_SECRET = '4517b2f9a736477c990a456b89bc66a0'
CLIENT_ID = '15dae62072ae4c4aae6c5bedc0e8f223'
REDIRECT_URI = 'http://localhost:8888'


BASE_PROB = 80
UNRECOGNISED = 'unrecognised'


def stop(): # pauzowanie
    sp.pause_playback()
    print('stop')


def start(): # odpauzowanie
    sp.start_playback()
    print('start')


def skip(): # przewinięcie
    print('skip')
    sp.next_track()


def prev(): # powrót do poprzedniej piosenki
    sp.previous_track()
    print('prev')


def author(): # podaje autora obecnie odtwarzanej piosenki
    curr = sp.current_playback()
    artist_id = curr['item']['artists'][0]['id']
    print(sp.artist(artist_id)['name'])
    TTS.say(sp.artist(artist_id)['name'])


def album(): # podaje album obecnie odtwarzanej piosenki
    curr = sp.current_playback()
    print(curr['item']['album']['name'])
    TTS.say(curr['item']['album']['name'])


def suggest(): # włącza tryb shuffle
    sp.shuffle(True)
    print('mix')


def toPlaylist(arg): # dodaje obecnie odtwarzaną piosenke do podanej plalisty
    playlist_id = None
    playlists = sp.current_user_playlists()
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            this_prob = fuzz.token_set_ratio(arg, playlist['name'])
            if this_prob >= BASE_PROB:
                playlist_id = playlist['id']

        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None

    if playlist_id is None:
        print("There's no such playlist")
        return

    curr = sp.current_playback()
    song_id = [curr['item']['id']]
    sp.playlist_add_items(playlist_id, song_id)
    print("add to playlist " + arg)


def removeFromPlaylist(arg): # usuwa obecnie odtwarzaną piosenke z podanej plalisty
    id = None
    playlists = sp.current_user_playlists()
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            this_prob = fuzz.token_set_ratio(arg, playlist['name'])
            if this_prob >= BASE_PROB:
                id = playlist['id']

        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None

    if id is None:
        print("There's no such playlist")
        return

    curr = sp.current_playback()
    song_id = [curr['item']['id']]
    sp.playlist_remove_all_occurrences_of_items(id, song_id)
    print("remove from playlist " + arg)


def lookFor(arg): # szuka piosenek o podanej nazwie
    names = [sp.search(arg, type='track')['tracks']['items'][i]['name'] for i in
             range(min(5, len(sp.search(arg, type='track')['tracks']['items'])))]
    for t in names:
        print(t)
        TTS.say(t)


def toQueue(arg): # dodaje podaną piosenkę do kolejki
    uri = sp.search(arg, type='track')['tracks']['items'][0]['uri']
    sp.add_to_queue(uri)
    print("add to queue " + arg)


def lookForBest(arg): # wyszukuje najlepsze utwory podanego artysty
    print("look for best from " + arg)
    id = sp.search(arg, type='artist')['artists']['items'][0]['id']
    tops = sp.artist_top_tracks(id,'PL')['tracks']
    for i in tops:
        print(i['name'])
        TTS.say(i['name'])


def showDevices(): # wymienia aktualnie używane urządzenia
    devices = [sp.devices()['devices'][i]['name'] for i in range(len(sp.devices()['devices']))]
    for d in devices:
        print(d)
        TTS.say(d)


def createPlaylist(arg): # tworzy playlistę o podanej nazwie
    user_id = sp.me()['id']
    sp.user_playlist_create(user_id, arg, public=True, collaborative=False, description='Nowa playlista')
    print("create playlist " + arg)


def follow(arg): # ustawia obserwowanie podanego artysty
    print("follow " + arg)
    id = [sp.search(arg, type='artist')['artists']['items'][0]['id']]
    sp.user_follow_artists(id)


def unfollow(arg): # przestaje obserwowac podanego artystę
    artist_id = [sp.search(arg, type='artist')['artists']['items'][0]['id']]
    sp.user_unfollow_artists(artist_id)
    print("unfollow " + arg)


def suggestArtists(): # wymienia pięciu podobnych artystów, do autora obecnie odtwarzanej piosenki
    curr = sp.current_playback()
    artist_id = curr['item']['artists'][0]['id']
    similar = sp.artist_related_artists(artist_id)
    print("podobni artysci: ")
    for i in similar['artists'][:5]:
        print(i['name'])
        TTS.say(i['name'])


# słownik przyporządkowujący komendzie odpowiednią funkcję
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
    "look for song": lookFor,
    "look for best songs": lookForBest,
    "create playlist": createPlaylist,
    "follow": follow,
    "unfollow": unfollow,
    "devices": showDevices,
    "suggest artists": suggestArtists
}

def parser(command): # prosty parser dla wyrażeń bez zmiennych
    dict = {
        'zatrzymaj': 'stop', 'stop': 'stop', 'pauza': 'stop', 'pausa': 'stop',
        'start': 'start', 'graj': 'start', 'załącz muzyke': 'start', 'włącz muzyke': 'start',
        'skip': 'skip', 'przewiń': 'skip', 'skipnij': 'skip', 'następna piosenka': 'skip', 'następny utwór': 'skip',
        'puść następną': 'skip', 'następne': 'skip', 'następna': 'skip',
        'prev': 'prev', 'poprzednia piosenka': 'prev', 'cofnij': 'prev', 'cofnij piosenkę': 'prev',
        'cofnij utwór': 'prev',
        'author': 'author', 'kto śpiewa': 'author', 'podaj autora': 'author', 'autor': 'author', 'wykonawca': 'author',
        'podaj wykonawcę': 'author',
        'album': 'album', 'jaki to album': 'album', 'podaj album': 'album', 'z jakiego album': 'album',
        'suggest': 'suggest artists', 'mixuj': 'suggest', 'mix': 'suggest', 'sugeruj': 'suggest artists',
        'urządzenia': 'devices', 'jakie są dostępne urządzenia': 'devices', 'podaj moje urządzenia': 'devices',
        'zaproponuj podobnych artystów': "suggest artists", "kto ma podobne piosenki": "suggest artists",
        "podobni wykonawcy": "suggest artists", "podobni": "suggest artists",
    }


    prob = 0
    which = UNRECOGNISED

    for key in dict:
        this_prob = fuzz.token_set_ratio(key, command)
        if this_prob >= BASE_PROB: # jeśli prawdopodobieństwo że słowo jest daną komendą jest wyższe niż BASE_PROB, rozpatrujemy je
            if this_prob > prob:
                prob = this_prob
                which = key

    if which != UNRECOGNISED: return dict[which]
    return UNRECOGNISED

def asystent(command): # sprawdzamy za pomocą obu parserów
    task = parser(command)
    if task != UNRECOGNISED:
        to_func[task]()
    else:
        task,arg = spotifyParser.give_result(command)
        if task != UNRECOGNISED:
            to_func[task](arg) # przyporządkowujemy funkcję
        else: print('Niestety nie znam odpowiedzi')

    return "Zaraz wykonam " + command

def main():
    global TTS
    TTS = tts.init()
    TTS.setProperty('volume', 0.7)
    TTS.setProperty('rate', 190)

    STT = sr.Recognizer()

    print('''Napisz pytanie i naciśnij Enter albo naciśnij Enter i zadaj pytanie.''')
    while True: # pętla głowna rozpoznająca tekts lub mowę
        tekst = input(">>")
        if len(tekst) > 0:
            asystent(tekst)
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
    scope = ["user-read-playback-state", "user-modify-playback-state", "app-remote-control", "streaming","playlist-read-private","user-read-private","playlist-modify-private","playlist-modify-public","user-follow-modify"]
    TTS = None
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=CLIENT_ID, client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URI)) # autentykacja z serwerem

    main()
