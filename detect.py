from lib2to3.pgen2 import token
import numpy as np
import json
import random
import pickle
import tensorflow as tf

from keras.models import Model
from keras.models import load_model
from keras_preprocessing.sequence import pad_sequences

# Should be the same as in train.py SHOULD END IN "/"
# The files in this directory should be "model.h5" and "tokenizer.pickle"
model_sav_loc = './model/'


model = tf.keras.models.load_model(model_sav_loc + "model.h5")


with open(model_sav_loc + 'tokenizer.pickle', 'rb') as handle:
    tk = pickle.load(handle)



txt = ';;;;;;;;;;;'
seq = tk.texts_to_sequences([txt])
padded = pad_sequences(seq, maxlen=96)
pred = model.predict(padded)
print(pred)



