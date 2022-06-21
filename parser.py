# import thefuzz as df
# from thefuzz import fuzz
# from thefuzz import process
#
# BASE_PROB = 85
# UNRECOGNISED = 'unrecognised'
#
#
# def parser(command):
#     dict = {
#         'zatrzymaj': 'stop', 'stop': 'stop', 'pauza': 'stop', 'pausa': 'stop',
#         'start': 'start', 'graj': 'start', 'załącz muzyke': 'start', 'włącz muzyke': 'start',
#         'skip': 'skip', 'przewiń': 'skip', 'skipnij': 'skip', 'następna piosenka': 'skip', 'następny utwór': 'skip',
#         'następne': 'skip', 'następna': 'skip',
#         'prev': 'prev', 'poprzednia piosenka': 'prev', 'cofnij': 'prev', 'cofnij piosenkę': 'prev',
#         'cofnij utwór': 'prev',
#         'author': 'author', 'kto śpiewa': 'author', 'autor': 'author', 'wykonawca': 'author',
#         'podaj wykonawcę': 'author',
#         'album': 'album', 'jaki to album': 'album', 'podaj album': 'album', 'z jakiego album': 'album',
#         'suggest': 'suggest', 'graj podobne utwory': 'suggest', 'zaproponuj piosenki': 'suggest', 'mixuj': 'suggest',
#         'mix': 'suggest'
#     }
#
#     # words = command.split(" ")
#
#     prob = 0
#     which = UNRECOGNISED
#
#     for key in dict:
#         # key_words = key.split(" ")
#         # if len(key_words) == 1:
#         #     search = df.process.extract(key,words,limit=1)
#         #     this_key,this_prob = search[0],search[1]
#         #     if this_prob >= BASE_PROB:
#         #         if this_prob > prob:
#         #             prob = this_prob
#         #             which = this_key
#         this_prob = fuzz.token_set_ratio(key, command)
#         if this_prob >= BASE_PROB:
#             if this_prob > prob:
#                 prob = this_prob
#                 which = key
#
#     if which != UNRECOGNISED: return dict[which]
#     return UNRECOGNISED
#
#
# test = ['zatrzymaj', 'start', 'przewiń', 'poprzednia piosenka', 'kto śpiewa ten utwór', 'przewiń to discopolo']
# for t in test: print(parser(t))
