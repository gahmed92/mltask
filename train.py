#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Embedding
from keras.layers import LSTM
from keras.datasets import imdb
from keras.callbacks import EarlyStopping, ModelCheckpoint, \
    ReduceLROnPlateau

from keras import backend as K
from sklearn.metrics import f1_score

max_features = 20000

# cut texts after this number of words (among top max_features most common words)

maxlen = 80
batch_size = 32

print('Loading data...')
((x_train, y_train), (x_test, y_test)) = \
    imdb.load_data(num_words=max_features)

# Pad sequences (samples x time)

x_train = sequence.pad_sequences(x_train, maxlen=maxlen)
x_test = sequence.pad_sequences(x_test, maxlen=maxlen)

print('Build model...')

model = Sequential()
model.add(Embedding(max_features, 128))
model.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(1, activation='sigmoid'))

def recall_m(y_true, y_pred):
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
        recall = true_positives / (possible_positives + K.epsilon())
        return recall

def precision_m(y_true, y_pred):
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
        precision = true_positives / (predicted_positives + K.epsilon())
        return precision

def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))

#def f1_m(y_true, y_pred):     
#    return f1_score(y_true, y_pred)


model.compile(loss='binary_crossentropy', optimizer='adam',
              metrics=['accuracy', f1_m])
print('Train...')

# Configs for saving the best model

earlyStopping = EarlyStopping(monitor='val_loss', patience=10,
                              verbose=0, mode='min')
mcp_save = ModelCheckpoint('imdb.mdl.hdf5', save_best_only=True,
                           monitor='val_loss', mode='min')
reduce_lr_loss = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.1,
    patience=7,
    verbose=1,
    epsilon=1e-4,
    mode='min',
    )

# Start Training

model.fit(
    x_train,
    y_train,
    batch_size=batch_size,
    epochs=15,
    validation_data=(x_test, y_test),
    callbacks=[earlyStopping, mcp_save, reduce_lr_loss],
    )
(score, acc, f1_score) = model.evaluate(x_test, y_test,
        batch_size=batch_size)

print('Test score:', score)
print('Test accuracy:', acc)
print('Test F1 score:', f1_score)
