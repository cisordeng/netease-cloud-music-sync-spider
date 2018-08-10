import json
from spider import main
from com_params import *

def get_netease_cloud_music(userid):
    user = {}
    js = json.loads(main(user_list(userid)))['playlist'][0]['creator']
    user['nickname'] = js['nickname']
    user['pic']      = js['avatarUrl']
    user['list']     = get_user_lists(userid)
    for song in user['list']:
        song['song'] = get_list_songs(song['id'])

    return user

# 用户歌单信息过滤
def get_user_lists(userid):
    playlist = json.loads(main(user_list(userid)))['playlist']
    lists = []
    # 仅获取用户歌单createTime，playCount，id
    for l in playlist:
        list = {} # 重新初始化申请内存，避免每次添加的list均为最后一项
        list['createTime'] = l['createTime']
        list['playCount']  = l['playCount']
        list['name']       = l['name']
        list['pic']        = l['coverImgUrl']
        list['id']         = l['id']
        lists.append(list)
    return lists

def get_list_songs(listid):
    detail = json.loads(main(list_song(listid)))['result']['tracks']
    songs = []
    #仅获取歌单createTime，playCount，id
    for s in detail:
        song = {} # 重新初始化申请内存，避免每次添加的song均为最后一项
        song['singer'] = '/'.join([si['name'] for si in s['artists']])
        song['name']   = s['name']
        song['id']     = s['id']
        song['url']    = get_song_url(s['id'])
        song['pic']    = s['album']['picUrl']
        songs.append(song)
    return songs

def get_song_url(songid):
    return json.loads(main(song_url([songid])))['data'][0]['url']
