import pandas as pd
import random
from collections import Counter

from sklearn.model_selection import train_test_split

extra_data = "./rawdata/1000.txt"
random.seed(123)

positive = []
negative = []

CHARS = []

with open("rawdata/letmesmash.txt") as f:
    for line in f:
        line = line.strip().lower()
        if not line:
            continue

        positive.append(line)

        for c in line:
            CHARS.append(c)


def gen_random_seq(length):

    s = ""

    for c in range(length):
        s += random.choice(CHARS)
    return s


#for line in positive:
#    negative.append(gen_random_seq(len(line)))


def insert_ext_data(file):
    with open(file) as data_file:
        for line in data_file:
            line = line.strip().lower()
            if not line:
                continue
            negative.append(line)


insert_ext_data(extra_data)

df = pd.DataFrame()
df["text"] = positive + negative
df["label"] = ["BOTTOM_KEY_SMASH" for _ in positive] + ["RANDOM" for _ in negative]


df_train, df_test = train_test_split(df, test_size=0.2, random_state=123)

df_test.head(10)


df_train.to_csv("processeddata/train.csv", index=False)
df_test.to_csv("processeddata/test.csv", index=False)


print("done")
