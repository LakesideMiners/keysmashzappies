import pickle
import configparser
import tensorflow as tf
from keras_preprocessing.sequence import pad_sequences

model_sav_loc = "./model/"

config = configparser.ConfigParser()
config.read('config.ini')
# Auth
username = config['auth']['username']
apikey = config['auth']['apikey']
sharecode = config['auth']['sharecode']
name = config['auth']['name']

# Settings
mode = config['settings']['mode']
duration = config['settings']['duration']
intensity = config['settings']['intensity']

# Warning Settings
warning = config['warning']['enable']
randomenable = config['warning']['random']
minwait = config['warning']['minwait']
maxwait = config['warning']['maxwait']

# Load the model and the tokenizer
model = tf.keras.models.load_model("model/check.h5")
with open(model_sav_loc + "tokenizer.pickle", "rb") as handle:
    tk = pickle.load(handle)


# Define some functions to help with processing
def bigger(input1, input2):
    if input1 > input2:
        # print("Input 1 is bigger!")
        return 1
    else:
        return 2


def unfuck(input):
    unfucked = input.tolist()
    unfucked = str(unfucked)
    unfucked = unfucked.replace("[", "").replace("]", "").replace(" ", "")
    unfucked = unfucked.split(",")
    return unfucked


def process(input):
    seq = tk.texts_to_sequences([input])
    padded = pad_sequences(seq, maxlen=96)
    prediction = model.predict(padded)
    unfucked = unfuck(prediction)
    bottom = unfucked[0]
    notbottom = unfucked[1]
    bigger_value = bigger(unfucked[0], unfucked[1])
    return bottom, notbottom, bigger_value


def 


