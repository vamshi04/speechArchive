import pandas as pd
import numpy as np

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

data['word_label'].apply(getIndex)
features, y = data.loc[ : , dataColumns[2]: dataColumns[-4]], data[dataColumns[-1]]
y = y.apply(getIndex)

accent = data.loc[ : , dataColumns[1]]
print(accent.head())