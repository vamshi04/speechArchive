from Classifier_data import *

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier as DTC
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

x_train, x_test, y_train, y_test = train_test_split(features, y, test_size = 0.2,random_state=42, shuffle=True, stratify = data[['native_langauge','word_label']])
print(x_train.shape, x_test.shape)
print(y_train.shape, y_test.shape)

DTC_model = DTC()

print("DTS training..")
DTC_model.fit(x_train, y_train)

print("evaluating train DTS..")
DTS_pred = DTC_model.predict(x_train)

trainscores = accuracy_score(DTS_pred, y_train)
print("Train accuracy: ", trainscores)

train_confusion_matrix = confusion_matrix(DTS_pred, y_train)
print("Train confusion_matrix: ", train_confusion_matrix)

print("evaluating test DTS..")
DTS_prediction = DTC_model.predict(x_test)

scores = accuracy_score(DTS_prediction, y_test)
print("Test accuracy: ", scores)

confusion_matrix = confusion_matrix(DTS_prediction, y_test)
print("Test confusion_matrix: ", confusion_matrix)

print("report")
cr = classification_report(DTS_prediction, y_test)
print(cr)

f = open('DecisionTree_report.txt', 'w')
f.write('DecisionTree Clasiffier:\n\Word Classification Report\n\n{}\n\nConfusion Matrix\n\n{}\n'.format(cr, confusion_matrix))
f.close()