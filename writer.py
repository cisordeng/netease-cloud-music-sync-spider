from user import get_netease_cloud_music

def writer(path, userid):
    print("# start get data to '"+path+"' #")
    try:
        f = open(path,'w+')
        f.write(str(get_netease_cloud_music(userid)))
        f.close()
        print("# write sucess #")
    except:
        print("# write error #")
