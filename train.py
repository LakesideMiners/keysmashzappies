
from xml.etree.ElementInclude import DEFAULT_MAX_INCLUSION_DEPTH
import pandas as pd
import numpy as np
import json
import random
import pickle
from sklearn.model_selection import train_test_split

from keras.models import Sequential
from keras.layers import Dense
from keras.utils.np_utils import to_categorical
from keras.preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences

from keras.layers import Input, Embedding, Activation, Flatten, Dense
from keras.layers import Conv1D, MaxPooling1D, Dropout
from keras.models import Model

from sklearn.model_selection import ParameterGrid
from itertools import combinations
from tqdm import tqdm




# The path to put the CSV files, these wont exist till after the code is ran
data_train_loc_csv = "./data/train.csv"
data_test_loc_csv = "./data/test.csv"

# Where to save the models files. this is where the "model.h5" and "tokenizer.pickle" files go. SHOULD END WITH A "/"
model_sav_loc = "./model/"



MAX_LEN = 96

df_train = pd.read_csv(data_train_loc_csv)
df_test = pd.read_csv(data_test_loc_csv)

train_texts = df_train["text"]
test_texts = df_test["text"]

tk = Tokenizer(num_words=None, char_level=True, oov_token='UNK')
tk.fit_on_texts(train_texts)

train_sequences = tk.texts_to_sequences(train_texts)
test_texts = tk.texts_to_sequences(test_texts)
f = open("./scratchpads/temp/uwu", "w")
f.write(str(train_sequences))
f.close()
f = open("./scratchpads/temp/uwutest", "w")
f.write(str(test_texts))
f.close()
# Padding
train_data = pad_sequences(train_sequences, maxlen=MAX_LEN, padding='post')
test_data = pad_sequences(test_texts, maxlen=MAX_LEN, padding='post')

# Convert to numpy array
train_data = np.array(train_data, dtype='float32')
test_data = np.array(test_data, dtype='float32')

train_classes = [1 if l == "BOTTOM_KEY_SMASH" else 0 for l in df_train["label"].values]
test_classes = [1 if l == "BOTTOM_KEY_SMASH" else 0 for l in df_test["label"].values]

train_classes = to_categorical(train_classes)
test_classes = to_categorical(test_classes)


test_data.shape


VOCAB_SIZE = len(tk.word_index)

num_of_classes = 2
optimizer = 'adam'
loss = 'categorical_crossentropy'


def train_model(conv_layers, fully_connected_layers, dropout_p, epochs=10):
    embedding_weights = []
    embedding_weights.append(np.zeros(VOCAB_SIZE))

    for char, i in tk.word_index.items():
        onehot = np.zeros(VOCAB_SIZE)
        onehot[i - 1] = 1
        embedding_weights.append(onehot)

    embedding_weights = np.array(embedding_weights)

    embedding_layer = Embedding(VOCAB_SIZE + 1,
                                VOCAB_SIZE,
                                input_length=MAX_LEN,
                                weights=[embedding_weights])

    inputs = Input(shape=(MAX_LEN,), name='input', dtype='int32')

    x = embedding_layer(inputs)

    for filter_num, filter_size, pooling_size in conv_layers:
        x = Conv1D(filter_num, filter_size, padding='same')(x)
        x = Activation('relu')(x)
        if pooling_size != -1:
            x = MaxPooling1D(pool_size=pooling_size)(x)
    x = Flatten()(x)

    for dense_size in fully_connected_layers:
        x = Dense(dense_size, activation='relu')(x)
        x = Dropout(dropout_p)(x)

    predictions = Dense(num_of_classes, activation='softmax')(x)

    model = Model(inputs=inputs, outputs=predictions)
    model.compile(optimizer=optimizer, loss=loss, metrics=['accuracy'])  # Adam, categorical_crossentropy

    indices = np.arange(train_data.shape[0])

    x_train = train_data[indices]
    y_train = train_classes[indices]

    x_test = test_data
    y_test = test_classes

    hist = model.fit(x_train, y_train,
              validation_data=(x_test, y_test),
              batch_size=64,
              epochs=epochs,
              verbose=0)

    return hist, model


num_layers = [5]

layer_params = {
    "filter_num": [128, 256, 512],
    "filter_size": [3,5,7],
    "pooling_size": [-1, 3],
}

fc_params = {
    "num_layers": [1,2],
    "layer_size": [64, 128]
}

layer_combinations = list(ParameterGrid(layer_params))
architectures = []
for n in num_layers:
    for arch in combinations(layer_combinations, n):
        architectures.append([[
            x["filter_num"], x["filter_size"], x["pooling_size"]
        ] for x in arch])

def tune():
    best_acc = 0
    for conv_layers in tqdm(architectures):
        for fc_param in ParameterGrid(fc_params):
            for dropout_p in [0.25, 0.5]:

                fully_connected_layers = [fc_param["layer_size"]] * fc_param["num_layers"]

                hist, _ = train_model(conv_layers, fully_connected_layers, dropout_p)
                acc = max(hist.history["val_accuracy"])

                if acc > best_acc:
                    print(f"conv={conv_layers} fc={fully_connected_layers}, d={dropout_p} ACC={acc}")
                    best_acc = acc
#tune()


hist, model = train_model([[128, 3, -1], [256, 3, 3]], [64], 0.25)
print(hist.history["val_accuracy"])

hist, model = train_model([[128, 3, -1], [256, 3, 3]], [64], 0.25, epochs=9)

model.save(model_sav_loc + 'model.h5')

with open(model_sav_loc + 'tokenizer.pickle', 'wb') as handle:
    pickle.dump(tk, handle, protocol=pickle.HIGHEST_PROTOCOL)


