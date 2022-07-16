import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm
import pickle
filename = 'finalized_model.sav'
from sklearnex import patch_sklearn
patch_sklearn()

smash = pd.read_csv('datasets/dataset2.csv')
z = smash['UserText']
y = smash["Label"]
z_train, z_test,y_train, y_test = train_test_split(z,y,test_size = 0.2)
print("Done splitting")


cv = CountVectorizer()
features = cv.fit_transform(z_train)
print("Done fit transform")

model = svm.SVC()
model.fit(features,y_train)
print("Done model.fit")


features_test = cv.transform(z_test)
print(model.score(features_test,y_test))
pickle.dump(model, open(filename, 'wb'))