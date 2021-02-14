from Classifier_data import *

from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

x_train, x_test, y_train, y_test = train_test_split(features, y, test_size = 0.2,random_state=42, shuffle=True, stratify = data[['native_langauge','word_label']])
print(x_train.shape, x_test.shape)
print(y_train.shape, y_test.shape)

SVC_model = SVC()

print("SVM training..")
SVC_model.fit(x_train, y_train)

print("evaluating train SVM..")
SVC_pred = SVC_model.predict(x_train)

trainscores = accuracy_score(SVC_pred, y_train)
print("Train accuracy: ", trainscores)

train_confusion_matrix = confusion_matrix(SVC_pred, y_train)
print("Train confusion_matrix: ", train_confusion_matrix)

print("evaluating test SVM..")
SVC_prediction = SVC_model.predict(x_test)

scores = accuracy_score(SVC_prediction, y_test)
print("Test accuracy: ", scores)

confusion_matrix = confusion_matrix(SVC_prediction, y_test)
print("Test confusion_matrix: ", confusion_matrix)

print("report")
cr = classification_report(SVC_prediction, y_test)
print(cr)

f = open('SVM_report.txt', 'w')
f.write('SVM Clasiffier:\n\Word Classification Report\n\n{}\n\nConfusion Matrix\n\n{}\n'.format(cr, confusion_matrix))
f.close()