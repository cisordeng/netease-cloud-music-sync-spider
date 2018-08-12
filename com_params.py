# 由user id获取lists id
def user_list(userid):
    url = 'https://music.163.com/weapi/user/playlist'
    first_param = '{"uid":"%s","wordwrap":"7","offset":"0","total":"true","limit":"36","csrf_token":""}' %userid
    return url, first_param

# 由list id获取songs id
def list_song(listid):
    url = 'https://music.163.com/weapi/playlist/detail'
    first_param = '{"id":"%s", "csrf_token":""}' %listid
    return url, first_param

# 由song id获取urls
def song_url(songid):
    url = 'https://music.163.com/weapi/song/enhance/player/url'
    first_param = '{ids:"%s",br:128000,csrf_token:""}' %songid
    return url, first_param

def song_lyric(songid):
    url = 'https://music.163.com/weapi/song/lyric'
    first_param = '{"id":%s,"lv":-1,"tv":-1,"csrf_token":""}' %songid
    return url, first_param
