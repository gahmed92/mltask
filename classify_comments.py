#!/usr/bin/python
from utils import *
import utils

from nltk import word_tokenize
from keras.datasets import imdb
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Embedding
from keras.layers import LSTM

model = None
max_features = 20000
maxlen = 80
INDEX_FROM = 3

word_to_id = imdb.get_word_index()
word_to_id = {k:(v+INDEX_FROM) for k,v in word_to_id.items()}
word_to_id["<PAD>"] = 0
word_to_id["<START>"] = 1
word_to_id["<UNK>"] = 2

def word_to_id2(word):
    try:
        i = word_to_id[word]
        if i >= max_features:
            i = 2
        return i
    except:
        return 2

def load_comments():
    conn = utils.conn
    cur = conn.cursor()
    cur.execute("SELECT * FROM COMMENTS")
    rows = cur.fetchall()
    return [base64.b64decode((row[2])) for row in rows]


def load_model():
    global model
    model = Sequential()
    model.add(Embedding(max_features, 128))
    model.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2))
    model.add(Dense(1, activation='sigmoid'))
    model.load_weights("imdb.mdl.hdf5")


if __name__ == "__main__":

    load_db()
    comments = load_comments()
    close_db()

    load_model()

    tokenized = [word_tokenize(comment.decode('utf-8').strip().lower()) for comment in comments]

    tokenized_id = [ [1] + [word_to_id2(wid) for wid in tokenized_text] for tokenized_text in tokenized]
    print len(tokenized)    
    tokenized_id_pad = sequence.pad_sequences(tokenized_id, maxlen=maxlen)

    print model.predict(tokenized_id_pad)
