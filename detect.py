from ast import comprehension
from dataclasses import replace
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

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "0"


def set_tf_log_level(level: int):
    try:
        if level == 0:
            os.environ["TF_CPP_MIN_LOG_LEVEL"] = "0"
            print("Supressing NOTHING from TF!")
        elif level == 1:
            os.environ["TF_CPP_MIN_LOG_LEVEL"] = "1"
            print("Supressing INFO messages from TF!")
        elif level == 2:
            os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
            print("Supressing INFO and WARNING messages form TF!")
        elif level == 3:
            os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
            print(
                "Supressing INFO, WARNING, AND ERROR messages from TF! You better know what you are doing!"
            )
        else:
            os.environ["TF_CPP_MIN_LOG_LEVEL"] = "0"
            print("Somthing went wrong with setting the log level! Defualting to 0!")
    except:
        os.environ["TF_CPP_MIN_LOG_LEVEL"] = "0"
        print("Somthing went wrong with setting the log level! Defualting to 0!")


# Should be the same as in train.py SHOULD END IN "/"
# The files in this directory should be "model.h5" and "tokenizer.pickle"

model_sav_loc = "./model/"


model = tf.keras.models.load_model("model/check.h5")


with open(model_sav_loc + "tokenizer.pickle", "rb") as handle:
    tk = pickle.load(handle)


set_tf_log_level(2)

# Unfucks the output


def unfuck(input):
    unfucked = input.tolist()
    unfucked = str(unfucked)
    unfucked = unfucked.replace("[", "").replace("]", "").replace(" ", "")
    unfucked = unfucked.split(",")
    print(unfucked)
    return unfucked


def bigger(input1, input2):
    if input1 > input2:
        # print("Input 1 is bigger!")
        return 1
    else:
        return 2


while True:
    txt = input("Enter text: ")
    if txt != "exit":
        seq = tk.texts_to_sequences([txt])
        padded = pad_sequences(seq, maxlen=96)
        prediction = model.predict(padded)
        unfucked = unfuck(prediction)
        print("Val 1: " + unfucked[0])
        print("Val 2: " + unfucked[1])
        gay = bigger(unfucked[0], unfucked[1])
        print(gay)
    else:
        stop = True
        print("Exiting...")
        break


print("Done")
