#!/usr/bin/python

from utils import *
from get_comments import store_comments_from_video_id
import utils

def store_video_to_db(videos):
    conn = utils.conn
    cur = conn.cursor()
    for video in videos:
        text = u''.join(video[1]).encode('utf-8').strip()
        text = base64.b64encode(text)
        add_row = 'INSERT INTO VIDEOS (ID, TITLE) values ("{0}", "{1}");'.format(video[0], text)
        print add_row
        print "ADD COMMENTS:"
        store_comments_from_video_id(video[0])
        cur.execute(add_row)
    conn.commit()
    
def get_videos(json_videos):
    videos = []
    for video_snippet in json_videos:
        videos.append((video_snippet['id']['videoId'], video_snippet['snippet']['title']))
    return videos

def store_videos_from_search(MAX, maxPages):
    Pages = Queue.Queue()
    Pages.put("")
    i = 0
    while not Pages.empty():

        # load comments from url
        PAGE_TOKEN=Pages.get()
        url='{0}?part=snippet&maxResults={1}&order=date&regionCode=US&relevanceLanguage=en&type=video&eventType=completed&videoCategoryId=25&pageToken={2}&key={3}'.format(SEARCH_URL, MAX, PAGE_TOKEN, API_KEY)
        print url
        contents=urllib2.urlopen(url).read()
        json_obj = json.loads(contents)
        # add next page
        if json_obj.get('nextPageToken'):
             Pages.put(json_obj['nextPageToken'])

        # sotre to db
        store_video_to_db(get_videos(json_obj['items']))

        time.sleep(5)

        i = i + 1
        if i >= maxPages:
           break

if __name__ == "__main__":

    load_db()
    store_videos_from_search(50, 5)
    close_db()
