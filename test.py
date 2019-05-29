from nltk import word_tokenize
from keras.datasets import imdb
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Embedding
from keras.layers import LSTM

max_features = 20000
maxlen = 80
INDEX_FROM=3

word_to_id = imdb.get_word_index()
word_to_id = {k:(v+INDEX_FROM) for k,v in word_to_id.items()}
word_to_id["<PAD>"] = 0
word_to_id["<START>"] = 1
word_to_id["<UNK>"] = 2
def word_to_id2(word):
    try:
        return word_to_id[word]
    except:
        return 2

text = "i hate this one it is bad, it's very bad! hating it 123123sdf"

tokenized_text = word_tokenize(text)
l_text = [1] + [word_to_id2(wid) for wid in tokenized_text]
test=sequence.pad_sequences([l_text],maxlen=maxlen)


model = Sequential()
model.add(Embedding(max_features, 128))
model.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(1, activation='sigmoid'))
model.load_weights("imdb.mdl.hdf5")

print model.predict(test)
