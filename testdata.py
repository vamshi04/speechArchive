import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split

from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import  GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score




unique = ['please', 'call', 'stella', 'ask', 'her', 'to', 'bring', 'these', 'things', 'with',
        'from', 'the', 'store', 'six', 'spoons', 'of', 'fresh', 'snow', 'peas', 'five',
        'thick', 'slabs', 'blue', 'cheese', 'and', 'maybe', 'a', 'snack', 'for', 'brother',
        'bob', 'we', 'also', 'need', 'small', 'plastic', 'snake', 'big', 'toy', 'frog',
        'kids', 'she', 'can', 'scoop', 'into', 'three', 'red', 'bags', 'will', 'go', 'meet',
        'wednesday', 'at', 'train', 'station']

def getIndex(label):
    global unique 
    return int(unique.index(label))
     

data = pd.read_excel("/home/malkaiv/project/final/recordings/mfccs_total.xlsx")
dataColumns = data.columns

features, y = data.loc[ : , dataColumns[1]: dataColumns[-2]], data[dataColumns[-1]]
y = y.apply(getIndex)
# print(features.shape, y.shape)

x_train, x_test, y_train, y_test = train_test_split(features, y, test_size = 0.2,random_state=42, shuffle=True, stratify = y)
print(x_train.shape, x_test.shape)
print(y_train.shape, y_test.shape)

logreg_clf = LogisticRegression()
SVC_model = SVC()
KNN_model = KNeighborsClassifier(n_neighbors=54)
DTC_model = DecisionTreeClassifier()

print("SVM training..")
SVC_model.fit(x_train, y_train)

print("KNN training..")
KNN_model.fit(x_train, y_train)

print("logreg training..")
logreg_clf.fit(x_train, y_train)

print("DecisionTree Training..")
DTC_model.fit(x_train, y_train)

print("Gaussian Training..")
GaussianNB
print("training done")

print("evaluating train SVM..")
SVC_pred = SVC_model.predict(x_train)
trainscores = accuracy_score(SVC_pred, y_train)
train_confusion_matrix = confusion_matrix(SVC_pred, y_train)
print("accuracy: ", trainscores)
print("confusion_matrix: ", train_confusion_matrix)



print("evaluating test SVM..")
SVC_prediction = SVC_model.predict(x_test)
scores = accuracy_score(SVC_prediction, y_test)
confusion_matrix = confusion_matrix(SVC_prediction, y_test)
print("accuracy: ", scores)
print("confusion_matrix: ", confusion_matrix)



# scores = SVC_model.evaluate(x_test, y_test)

# print(SVC_test_results)
