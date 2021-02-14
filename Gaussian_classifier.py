from Classifier_data import *

from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import  GaussianNB
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

x_train, x_test, y_train, y_test = train_test_split(features, y, test_size = 0.2,random_state=42, shuffle=True, stratify = data[['native_langauge','word_label']])
print(x_train.shape, x_test.shape)
print(y_train.shape, y_test.shape)

gaussian = GaussianNB()

print("gaussian training..")
gaussian.fit(x_train, y_train)

print("evaluating train gaussian..")
gaussian_train_pred = gaussian.predict(x_train)

trainscores = accuracy_score(gaussian_train_pred, y_train)
print("Train accuracy: ", trainscores)

train_confusion_matrix = confusion_matrix(gaussian_train_pred, y_train)
print("Train confusion_matrix: ", train_confusion_matrix)

print("evaluating test gaussian..")
gaussian_test_pred = gaussian.predict(x_test)

scores = accuracy_score(gaussian_test_pred, y_test)
print("Test accuracy: ", scores)

confusion_matrix = confusion_matrix(gaussian_test_pred, y_test)
print("Test confusion_matrix: ", confusion_matrix)

print("report")
cr = classification_report(gaussian_test_pred, y_test)
print(cr)

f = open('Gaussian_report.txt', 'w')
f.write('Gaussian Clasiffier:\n\Word Classification Report\n\n{}\n\nConfusion Matrix\n\n{}\n'.format(cr, confusion_matrix))
f.close()