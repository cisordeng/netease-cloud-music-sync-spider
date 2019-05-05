# -*- coding: utf-8 -*- #
import pymysql
from config import *

SONG_INDEX = 0
LIST_INDEX = 0

conn = pymysql.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    port=DB_PORT,
    charset='utf8',
)

def insert_song(nid, name, avatar, url, lyric, translated_lyric, singer_name):
    snid = str(nid)
    if not lyric:
        lyric = ''
    if not translated_lyric:
        translated_lyric = ''
    sql = "select id from rhythm_rhythm where nid='"+snid+"'"
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    count = cursor.execute(sql)
    if count != 0:
        print('exist song skip!')
        return cursor.fetchone()['id']
    else:
        sql = "insert into rhythm_rhythm(nid, name, avatar, url, lyric, translated_lyric, singer_name) values(%s, %s, %s, %s, %s, %s, %s)"
        return commit_sql(sql, (snid, name, avatar, url, lyric, translated_lyric, singer_name))


def insert_list(nid, name, avatar):
    snid = str(nid)
    sql = "insert into rhythm_rhythm_set(nid, name, avatar, `index`) values(%s, %s, %s, %s)"
    global LIST_INDEX
    LIST_INDEX += 1
    return commit_sql(sql, (nid, name, avatar, LIST_INDEX))


def insert_list_song(rhythm_set_id, rhythm_id):
    sql = "insert into rhythm_rhythm_set_rhythm(rhythm_set_id, rhythm_id, `index`) values(%s, %s, %s)"
    global LIST_INDEX
    global SONG_INDEX
    if rhythm_set_id == LIST_INDEX:
        SONG_INDEX += 1
    else:
        SONG_INDEX = 0
    return commit_sql(sql, (str(rhythm_set_id), str(rhythm_id), SONG_INDEX))


def commit_sql(sql, values):
    cursor = conn.cursor()
    try:
        cursor.execute(sql, values)
        conn.commit()

        cursor.execute("select last_insert_id();")
        data = cursor.fetchall()
        return data[0][0]
    except Exception as e:
        conn.rollback()
        print("error rollback!")
        print(e)
        print(values)
        return -1

