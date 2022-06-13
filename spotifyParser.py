import thefuzz as df
from thefuzz import process

key_word_playlist = ["playlista", "składanka", "lista"]
key_word_song = ["piosenka", "utwór", "kawałek"]
key_word_author = ["artysta", "autor", "wykonawca"]
trash = ["o nazwie", "pod tytułem","nazwa","tytuł"]

UNRECOGNISED = 'unrecognised'

def give_result(example):
    sentence_words = example.split(" ")  # podzielenie polecenia na pojedyncze słowa
    if len(sentence_words) == 0:
        print("Brak argumentów")
        return

    playlist = -1
    song = -1
    #author = -1

    start_inx = -1
    i = 0

    name = ""
    command = UNRECOGNISED
    while i < len(sentence_words):
        temp = df.process.extract(sentence_words[i], key_word_playlist, limit=1)
        if temp[0][1] >= 80 and len(sentence_words[i]) > 1:
            playlist = 1
            sentence_words = sentence_words[0:i] + sentence_words[(i + 1):]
            start_inx = i
            continue

        temp = df.process.extract(sentence_words[i], key_word_song, limit=1)
        if temp[0][1] >= 80 and len(sentence_words[i]) > 1:
            song = 1
            sentence_words = sentence_words[0:i] + sentence_words[(i + 1):]
            start_inx = i
            continue

        temp = df.process.extract(sentence_words[i], key_word_author, limit=1)
        if temp[0][1] >= 80 and len(sentence_words[i]) > 1:
            #author = 1
            sentence_words = sentence_words[0:i] + sentence_words[(i + 1):]
            start_inx = i
            continue
        i += 1

    if start_inx == -1:
        name = "no name given"  # no key word
        command = UNRECOGNISED
        return command, name

    # creating name of song / playlist / author
    if start_inx + 2 < len(sentence_words):
        temp = sentence_words[start_inx] + " " + sentence_words[start_inx + 1]
        if df.process.extract(temp, trash, limit=1)[0][1] >= 80 and len(df.process.extract(temp, trash, limit=1)[0][0]) > 5:
            sentence_words = sentence_words[:start_inx] + sentence_words[start_inx + 2:]
        elif df.process.extract(temp, trash, limit=1)[0][1] >= 80:
            sentence_words = sentence_words[:start_inx] + sentence_words[start_inx + 1:]
    name_tab = sentence_words[start_inx:]
    for i in name_tab:
        name += " " + i
    sentence_words = sentence_words[:start_inx]


    # w tym miejscu ustawienie formatu output
    # name -> nazwa utworu / artysty / playlisty
    # z kontekstu polecenia można wywnioskować czego nazwy potrzebujemy
    # wiem że troche brute force ale nie wiem jak inaczej to sensowanie zrobic XD

    if df.process.extract("dodaj", sentence_words, limit=1)[0][1] >= 70:
        if playlist != -1:
            command = "add to playlist"
        elif df.process.extract("kolejka", sentence_words, limit=1)[0][1] >= 70:
            command = "add to queue"
    elif df.process.extract("usuń", sentence_words, limit=1)[0][1] >= 70:
        if playlist != -1:
            command = "remove from playlist"
        elif df.process.extract("kolejka", sentence_words, limit=1)[0][1] >= 70:
            command = "remove from queue"
    elif df.process.extract("wyszukaj", sentence_words, limit=1)[0][1] >= 70:
        if song != -1:
            command = "look for song"
    elif df.process.extract("najlepsze", sentence_words, limit=1)[0][1] >= 70:
        command = "look for best songs"
    elif df.process.extract("stwórz", sentence_words, limit=1)[0][1] >= 70:
        if playlist != -1:
            command = "create playlist"
    elif df.process.extract("obserwuj", sentence_words, limit=1)[0][1] >= 60:
        if df.process.extract("przestań", sentence_words, limit=1)[0][1] >= 80:
            command = "unfollow"
        else:
            command = "follow"
    else:
        command = UNRECOGNISED

    return command, name


if __name__ == '__main__':
    prev = ''

    arg = open('args.txt', "r", encoding='utf8')
    for line in arg:
        print(line.strip() + ":")
        print(give_result(line.strip()))
        print()
