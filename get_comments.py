#!/usr/bin/python

from utils import *
import utils

def store_comment_to_db(comments):
    conn = utils.conn
    cur = conn.cursor()
    for comment in comments:
        text = u''.join(comment[2]).encode('utf-8').strip()
        text = base64.b64encode(text)
        add_row = 'INSERT INTO COMMENTS (ID, VIDEO_ID, COMMENT) values ("{0}", "{1}", "{2}");'.format(comment[0], comment[1], text)
        cur.execute(add_row)
    conn.commit()
    
def get_comments(json_comments):
    comments = []
    for comment_snippet in json_comments:
        comments.append((comment_snippet['id'], comment_snippet['snippet']['videoId'], comment_snippet['snippet']['topLevelComment']['snippet']['textDisplay']))
    return comments

def store_comments_from_video_id(ID):
    Pages = Queue.Queue()
    Pages.put("")
    i = 0
    while not Pages.empty():

        # load comments from url
        PAGE_TOKEN=Pages.get()
        url='{0}?part=snippet&videoId={1}&pageToken={2}&key={3}'.format(COMMENT_URL, ID, PAGE_TOKEN, API_KEY)
        contents=urllib2.urlopen(url).read()
        json_obj = json.loads(contents)

        # add next page
        if json_obj.get('nextPageToken'):
             Pages.put(json_obj['nextPageToken'])

        # sotre to db
        store_comment_to_db(get_comments(json_obj['items']))
        print "ADDED COMMENTS"
        time.sleep(1)

        i = i + 1
        if i > 5:
           break

if __name__ == "__main__":

    load_db()
    store_comments_from_video_id("vKxKCHM9kx8")
    close_db()
