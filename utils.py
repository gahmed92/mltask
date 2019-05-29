#!/usr/bin/python

import time, json, urllib2, Queue, sqlite3, base64

conn = None

API_KEY="AIzaSyBk3XuAl4KWCf-2bNsiLl6_lcxanunJG60"
COMMENT_URL="https://www.googleapis.com/youtube/v3/commentThreads"
SEARCH_URL="https://www.googleapis.com/youtube/v3/search"

def load_db():
    global conn
    conn = sqlite3.connect('youtube.sqlite')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS VIDEOS(ID TEXT PRIMARY KEY NOT NULL, TITLE TEXT);')
    cur.execute('CREATE TABLE IF NOT EXISTS COMMENTS(ID TEXT PRIMARY KEY NOT NULL, VIDEO_ID TEXT NOT NULL, COMMENT TEXT);')
    cur.execute('CREATE TABLE IF NOT EXISTS COMMENTS_CLASSES(ID TEXT PRIMARY KEY NOT NULL, SENTIMENT INTEGER);')
    conn.commit()

def close_db():
    global conn
    conn.close()
