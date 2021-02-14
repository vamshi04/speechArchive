import pandas as pd
from pydub import AudioSegment
import librosa


def getword(str1):
    if "_" in str1:
        str1 = str1.split("_")
        str1 = str1[0]
    return str1
        


def splitAudio(str1, speaker_id, word):
    mfccs = []
    if str(str1) != 'nan':
        lst  = str1.strip('][').strip(')(').split(",")
        start, end = float(lst[0]), float(lst[1])
        start = (start * 1000)   # because split from AudioSegment works in milliseconds
        end = (end * 1000) 
        newAudio = AudioSegment.from_wav("/home/malkaiv/project/final/recordings/wav/" + speaker_id + ".wav")
        newAudio = newAudio[start - 10 : end + 10]
        filename = '/home/malkaiv/project/final/recordings/wav/temp/'+ word +'.wav'
        newAudio.export(filename, format="wav")
        y, sr = librosa.load(filename, sr=None)
        mfccs = librosa.feature.mfcc(y=y, n_mfcc=40)
    return mfccs 



df = pd.read_excel(r"/home/malkaiv/project/final/recordings/new_word.xlsx", header=0)
outColumns = ["Speaker", "NativeLang"]
for i in range(1, 14):
    outColumns.append("Co-Eff" + str(i))
    if i == 13:
        outColumns.append("WordLabel")
outputDF = pd.DataFrame(columns = outColumns) 

keys = list(df.columns)
# print(len(df))
# print(df.isnull().sum(axis=1))
# df = df[df.isnull().sum(axis=1) > 5]

print(keys)

for index, rows in df.loc[0:0,:].iterrows():
    speaker_id = rows['speaker_id']
    print(speaker_id)
    for i, v in enumerate(rows):
        if i > 0:
            word = getword(keys[i])
            mfccs = splitAudio(v, speaker_id, word)
            if word == 'her':
                # print(ke, i)
                print(word, len(mfccs[0]))            
            
        
        
