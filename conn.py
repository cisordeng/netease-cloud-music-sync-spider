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

def reset_table():
    drop_sql = "drop table if exists rhythm_rhythm, rhythm_rhythm_set, rhythm_rhythm_set_rhythm;"
    new_sql = '''create table rhythm_rhythm(id int auto_increment primary key, nid bigint default 0 not null, name varchar(255) default '' not null, avatar varchar(255) default '' not null, url varchar(255) default '' not null, lyric longtext not null, translated_lyric longtext not null, singer_name varchar(255) default '' not null, played_count int default 0 not null, created_at datetime default CURRENT_TIMESTAMP not null);create table rhythm_rhythm_set(id int auto_increment primary key, nid bigint default 0 not null, name varchar(255) default '' not null, avatar varchar(255) default '' not null, played_count int default 0 not null, created_at datetime default CURRENT_TIMESTAMP not null, `index` int default 0 not null);create table rhythm_rhythm_set_rhythm(id int auto_increment primary key, rhythm_set_id int default 0 not null, rhythm_id int default 0 not null, created_at datetime default CURRENT_TIMESTAMP not null, `index` int default 0 not null)'''
    try:
        cursor = conn.cursor()
        cursor.execute(drop_sql)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(e)
        print("error rollback!")
    try:
        cursor = conn.cursor()
        for sql in new_sql.split(';'):
            sql = sql.strip()
            if len(sql) > 0:
                cursor.execute(sql)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(e)
        print("error rollback!")

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

