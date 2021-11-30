import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

dataToTree = pd.read_csv('user_fake_authentic_4class.csv')
dataToTree['class'] = dataToTree['class'].replace(['r', 'a', 'i', 's'], [0, 1, 2, 3])

# Dropar colunas cs e pi
dataToTree = dataToTree.drop(['cs', 'pi'], axis=1)


x = dataToTree.drop("class", axis=1)
y = dataToTree["class"]

Xtrain, Xval, Ytrain, Yval = train_test_split(x, y, test_size=0.5, random_state=None)

trees = RandomForestClassifier(n_estimators=1000,random_state=0, n_jobs=-1)
trees.fit(Xtrain, Ytrain)

filename='finalized_model.sav'
pickle.dump(trees, open(filename, 'wb'))