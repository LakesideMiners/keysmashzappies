import pickle
import configparser
from time import sleep
import tensorflow as tf
from keras_preprocessing.sequence import pad_sequences
from pynput import keyboard
from threading import Timer, active_count
from piShock import piShock

import numpy as np
global keys_pressed

keys_pressed = []
global num_keys_pressed
num_keys_pressed = 0
global keys_to_keep
keys_to_keep = 10
model_sav_loc = "./model/"

config = configparser.ConfigParser()
config.read("config.ini")
# Auth
username = config["auth"]["username"]
apikey = config["auth"]["apikey"]
sharecode = config["auth"]["sharecode"]
name = config["auth"]["name"]

# Settings
mode = config["settings"]["mode"]
duration = int(config["settings"]["duration"])
intensity = int(config["settings"]["intensity"])

# Warning Settings
warning = int(config["warning"]["warning"])
randomenable = config["warning"]["random"]
minwait = int(config["warning"]["minwait"])
maxwait = int(config["warning"]["maxwait"])

# Load the model and the tokenizer
model = tf.keras.models.load_model("model/check.h5")
with open(model_sav_loc + "tokenizer.pickle", "rb") as handle:
    tk = pickle.load(handle)

# Functions that do the shock stuff


# Define some functions to help with processing
def bigger(input1: int, input2: int):

    if input1 > input2:
        # print("Input 1 is bigger!")
        return 1
    else:
        return 2


def unfuck_predict(input: np.ndarray) -> list:
    """unfuck_predict unfucks the prediction output

    :param input: the fucked prediction
    :type input: np.ndarray
    :return: the unfucked prediction
    :rtype: list
    """    
    unfucked = input.tolist()
    unfucked = str(unfucked)
    unfucked = unfucked.replace("[", "").replace("]", "").replace(" ", "")
    unfucked = unfucked.split(",")
    return unfucked


def predict_smash(input: str):
    """predict_smash _summary_

    Args:
        input (str): _description_

    Returns:
        list: returns a list in the follow format
    """    
    seq = tk.texts_to_sequences([input])
    padded = pad_sequences(seq, maxlen=96)
    prediction = model.predict(padded)
    unfucked = unfuck_predict(prediction)
    bottom = unfucked[0]
    notbottom = unfucked[1]
    bigger_value = bigger(unfucked[0], unfucked[1])
    return unfucked, bottom, notbottom, bigger_value


def to_string(input: list) -> str:
    stringed = "".join(input)
    return stringed


# Keylogger Stuff
def on_press(key):
    try:
        keys_pressed.append(key.char)
    except AttributeError:
        pass


def on_release(key):
    global num_keys_pressed
    global keys_pressed
    global keys_to_keep
    if num_keys_pressed >= keys_to_keep:
        predict_output = predict_smash(to_string(keys_pressed))
        if predict_output[3] == 2:
            zap()
        num_keys_pressed = 0
        print("Done")
        print(keys_pressed)
        keys_pressed = []
        return False
    else:
        num_keys_pressed += 1
        pass


def create_listener():
    sleep(5)
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()



#def shock(username, apikey, sharecode, name, duration, )
def zap():
    piShock(username, apikey, sharecode, name, duration, intensity, warning).shock()
    print("ZAP")



while True:
    create_listener()
