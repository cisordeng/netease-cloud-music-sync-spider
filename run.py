# -*- coding: utf-8 -*- #

from config import *
import user
import conn

# lists = user.get_user_lists(NID)
# total = len(lists)
# lists.reverse()
# for i, l in enumerate(lists):
#     print("写入歌单>>[ " + l['name'] + " ]<<  " + str(i + 1) + "/" + str(len(lists)))
#     conn.insert_list(nid=int(l['id']), name=l['name'], avatar=l['pic'])


lists = user.get_user_lists(NID)
lists.reverse()
if RESET_TABLE:
    conn.reset_table()
for li, l in enumerate(lists):
    print("写入歌单>>[ " + l['name'] + " ]<<  " + str(li + 1) + "/" + str(len(lists)))
    list_id = conn.insert_list(nid=int(l['id']), name=l['name'], avatar=l['pic'])

    songs = user.get_list_songs(l['id'])
    songs.reverse()
    for si, s in enumerate(songs):
        print("写入单曲>>[ " + s['name'] + " ]<<  " + str(si + 1) + "/" + str(len(songs)))
        song_id = conn.insert_song(nid=int(s['id']), name=s['name'], avatar=s['pic'], url=s['url'], lyric=s['lyric']['lyric'], translated_lyric=s['lyric'].get('tlyric', ''), singer_name=s['singer'])
        conn.insert_list_song(list_id, song_id)


# song['singer'] = '/'.join([si['name'] for si in s['artists']])
# song['name'] = s['name']
# song['id'] = s['id']
# song['url'] = get_song_url(s['id'])
# song['lyric'] = get_song_lyric(s['id'])
# song['pic'] = s['album']['picUrl']
