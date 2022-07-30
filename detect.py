from lib2to3.pgen2 import token
import numpy as np
import json
import random
import pickle
import os
import tensorflow as tf
import re
from keras.models import Model
from keras.models import load_model
from keras_preprocessing.sequence import pad_sequences
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'


def set_tf_log_level(level: int):
    try:
        if level == 0:
            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'
            print("Supressing NOTHING from TF!")
        elif level == 1:
            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
            print("Supressing INFO messages from TF!")
        elif level == 2:
            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
            print("Supressing INFO and WARNING messages form TF!")
        elif level == 3:
            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
            print("Supressing INFO, WARNING, AND ERROR messages from TF! You better know what you are doing!")
        else:
            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'
            print('Somthing went wrong with setting the log level! Defualting to 0!')
    except:
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'
        print('Somthing went wrong with setting the log level! Defualting to 0!')


# Should be the same as in train.py SHOULD END IN "/"
# The files in this directory should be "model.h5" and "tokenizer.pickle"
model_sav_loc = './model/'


model = tf.keras.models.load_model(model_sav_loc + "model.h5")


with open(model_sav_loc + 'tokenizer.pickle', 'rb') as handle:
    tk = pickle.load(handle)






set_tf_log_level(2)
def unfuck(input):
    predstr = str(input) # list to string
    predstriped = re.sub(r"[\[\]]",'',predstr) #remove the brackets
    predlist = predstriped.split(" ") # get it back into a list
    print(predlist)
    predlist.remove(predlist[2]) # Drop the 2 item(the 3 if you start from 1)
    print(predlist) #print
    
while True:
    txt = input("Enter text: ")
    if txt != "exit":
        seq = tk.texts_to_sequences([txt])
        padded = pad_sequences(seq, maxlen=96)
        prediction = model.predict(padded)
        process_result(prediction)
    else:
        stop = True
        print("Exiting...")
        break


print("Done")