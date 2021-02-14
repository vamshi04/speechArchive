import pandas as pd
import numpy as np
import librosa
from pydub import AudioSegment
from mp3towav import *
from transcribe import *

from collections import OrderedDict, defaultdict
import os
import glob


def checkSameKey(str1, str2):
    equals = False
    if "_" in str1:
        str1 = str1.split("_")[0]
    elif "_" in str2:
        str2 = str2.split("_")[0]
    if str1 == str2:
        equals = True
    return equals

def moreconfidence(vals_i, vals_k):
    confident = False
    if str(vals_k) != 'nan':
        # print(vals_k)
        iConfidence = getFloats(vals_i)[2]
        kConfidence = getFloats(vals_k)[2]
        if iConfidence < kConfidence:
            confident = True
    return confident

def swapSameKeys(index, keys, vals):
    for k in range(index, len(vals) - 1):
        if  checkSameKey(keys[index], keys[k]) and moreconfidence(vals[index], vals[k]):
            # print(keys[index], keys[k])
            vals[index], vals[k] = vals[k], vals[index]
    

def getFloats(str1):
    Returnlist = str1.strip('][').strip(')(').split(",")
    return [float(i) for i in Returnlist] #convert each element into float and return the list
    # return Returnlist

def getword(str1):
    if "_" in str1:
        str1 = str1.split("_")[0]
    return str1

def getWordTimeoffs(word, words):
    # returnVals = []
    response = wordTimeOffsets(word, words, 1)
    # print(response)
    for result in response.results:
        alternative = result.alternatives[0]
        for w in alternative.words:

            if str(w.word) == word:
                # print(w)
                start = float(w.start_time.seconds + (10 ** -9 * (w.start_time.nanos)))
                end = float(w.end_time.seconds + (10 ** -9 * (w.end_time.nanos)))
                confidence = float(w.confidence)
                return [(start, end, confidence)]
    # return returnVals
          


def getAudioChunk(t1, t2, speaker_id, word, flag):
    t1 = t1 * 1000 #Works in milliseconds
    t2 = t2 * 1000
                    # "/home/malkaiv/project/final/recordings/wav/english1.wav"
    # print(t1, t2)

    if flag == 0:
        # audio = AudioSegment.from_wav("/home/malkaiv/project/final/recordings/wav/" + speaker_id + ".wav")
        # fpath = Path('/home/malkaiv/project/final/recordings/wav/'+ speaker_id +'.wav')
        # if fpath.is_file():
        #     audio = AudioSegment.from_wav("/home/malkaiv/project/final/recordings/wav/" + speaker_id + ".wav")
        # else:
        #     convert_mp3_wav(speaker_id)
        #     audio = AudioSegment.from_wav("/home/malkaiv/project/final/recordings/wav/" + speaker_id + ".wav")
        audio = AudioSegment.from_wav("/home/malkaiv/project/final/recordings/wav/" + speaker_id + ".wav")
    else:
        audio = AudioSegment.from_wav("/home/malkaiv/project/final/recordings/wordsWav/" + word + ".wav")
    audio_chunk = audio[t1:t2]
    audio_chunk.export('/home/malkaiv/project/final/recordings/wordsWav/'+ word +'.wav', format="wav")


def calculatedMFCCs(speaker_id, word, val, flag, calculatedKeys):
    # print(val)
    floats = getFloats(val)
    t1 = floats[0]
    t2 = floats[1]
    if t1 != t2:
        getAudioChunk(t1, t2, speaker_id, word, flag)
    else:
        getAudioChunk(t1 - 0.001, t2 + 0.001, speaker_id, word, flag)

    word_speech_file = "/home/malkaiv/project/final/recordings/wordsWav/"+ word +".wav"
    y, sr = librosa.load(word_speech_file)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc = 15)
    mfccs = normalise(mfccs)
    calculatedKeys.append(word)
    return mfccs, calculatedKeys

def normalise(mfccs):
    mfcc_arr = []
    for mfcc in mfccs:
        coeff = np.mean(mfcc)
        mfcc_arr.append(coeff)
    return mfcc_arr

def create_mfcc_series(speaker_id, ne, mfcc_arr, word_label):
    output = [speaker_id, ne] + mfcc_arr + [word_label]
    
    # output.extend(mfcc_arr)
    return output

            
                    


column_names = ['speaker_id', 'please', 'call', 'stella', 'ask', 'her', 'to', 'bring',
       'these', 'things', 'with', 'her_1', 'from', 'the', 'store', 'six',
       'spoons', 'of', 'fresh', 'snow', 'peas', 'five', 'thick', 'slabs',
       'of_1', 'blue', 'cheese', 'and', 'maybe', 'a', 'snack', 'for', 'her_2',
       'brother', 'bob', 'we', 'also', 'need', 'a_1', 'small', 'plastic',
       'snake', 'and_1', 'a_2', 'big', 'toy', 'frog', 'for_1', 'the_1', 'kids',
       'she', 'can', 'scoop', 'these_1', 'things_1', 'into', 'three', 'red',
       'bags', 'and_2', 'we_1', 'will', 'go', 'meet', 'her_3', 'wednesday',
       'at', 'the_2', 'train', 'station']
    #    originalCols = speechText.lower().split()


output_columns = ["speaker_id", "native_langauge"]
for i in range(1, 16):
    if i < 15:
        output_columns.append("co-eff" + str(i))
    else:
        output_columns.extend(["co-eff15", "word_label"])

print(output_columns)
df1 = pd.read_excel(r'/home/malkaiv/project/final/recordings/native_word.xlsx')
# print(df1.columns[0:70])
df = df1.copy()
na_count = df.loc[:,"speaker_id":"station"].isnull().sum(axis=1).tolist()

output = pd.DataFrame(columns = column_names)
mfcc_output = pd.DataFrame(columns = output_columns)

# print(output.columns)
for index, rows in df.iterrows():
    calculatedKeys = []
    if na_count[index] <= 6:
        s = rows
        sDict_1 = s.to_dict(OrderedDict)
        # print(sDict_1)
        # sDict = DictCycler(sDict_1)
        keys = list(sDict_1.keys())
        vals = list(sDict_1.values())
        # print("value: ", vals[1])    
        speaker_id = vals[0]
        print(speaker_id)
        files = glob.glob('/home/malkaiv/project/final/recordings/wordsWav/*')
        for f in files:
            os.remove(f)
        for i, v in enumerate(vals[0:70]):
            word = getword(keys[i])
            # mfccs = []
            if word not in calculatedKeys:
                # mfccs = []
                word_speech_file = "/home/malkaiv/project/final/recordings/wordsWav/"+ word +".wav"
                flag = 0
                ne = 0
                # mfccs = []
                if i == 1:
                    if str(vals[i]) != 'nan':
                        mfccs, calculatedKeys =  calculatedMFCCs(speaker_id, word, vals[i], 0, calculatedKeys)
                        # floats = getFloats(vals[i])
                        # t1 = floats[0]
                        # t2 = floats[1]
                        # getAudioChunk(t1, t2, speaker_id, word, 0)
                        # # speech_file = "/home/vamshi/SpeechArchive/wordsWav/"+ word +".wav"
                        # y, sr = librosa.load(word_speech_file)
                        # mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc = 15)
                        # mfccs = normalise(mfccs)
                        # calculatedKeys.append(keys[i])
                        # print(mfccs)
                        print(mfccs)
                        out = [speaker_id, ne]
                        for i in mfccs:
                            out = out + [i] 
                        out = out + [word]
                        temp = pd.Series(out, index = output_columns)
                        mfcc_output = mfcc_output.append(temp,  ignore_index=True)
                        
                        # df1.iloc[index, i] = mfccs
                        
                
                    else:
                        if str(vals[i + 1]) != 'nan':
                            # print(vals[i + 1])
                            t1 = float(0) 
                            t2 = getFloats(vals[i + 1])[1]
                            # print(t2)
                            getAudioChunk(t1, t2, speaker_id, word, 0)
                            
                            times = getWordTimeoffs(word, [word])
                            
                            if times:
                                vals[i] = str(times)
                                # vals[i] != 'nan':

                                mfccs, calculatedKeys = calculatedMFCCs(speaker_id, word, vals[i], 1, calculatedKeys)
                            
                            # # print(times)
                            # getAudioChunk(float(times[0]), float(times[1]), word, word, 1)
                            # y, sr = librosa.load(word_speech_file)
                            # mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc = 15)
                            # # print(mfccs)
                                # mfccs = normalise(mfccs)
                                out = [speaker_id, ne] + mfccs + [word]
                                temp = pd.Series(out, index = output_columns)
                                mfcc_output = mfcc_output.append(temp,  ignore_index=True)
                                # df1.iloc[index, i] = mfccs
                                # calculatedKeys.append(keys[i])
                                # print(mfccs)
                                
                
                elif i > 1:
                    # for k in range(i, len(vals) - 1):
                    #     if  checkSameKey(keys[i], keys[k]) and moreconfidence(vals[i], vals[k]):
                    #         print(keys[i], keys[k])
                    #         vals[i], vals[k] = vals[k], vals[i]
                    if str(vals[i]) != 'nan': 
                        if str(vals[i + 1]) != 'nan': 
                            next_stTime = getFloats(vals[i + 1])[0]
                            this_endTime = getFloats(vals[i])[1]
                            if this_endTime > next_stTime:
                                swapSameKeys(i, keys, vals)
                        mfccs, calculatedKeys = calculatedMFCCs(speaker_id, word, vals[i], 0, calculatedKeys)
                        # mfccs = normalise(mfccs)
                        out = [speaker_id, ne] + mfccs + [word]
                        temp = pd.Series(out, index = output_columns)
                        mfcc_output = mfcc_output.append(temp,  ignore_index=True)
                        # df1.iloc[index, i] = mfccs

                        
                    else:
                        prev = vals[i - 1]
                        nex = vals[ 1+ 1] 
                        if str(prev) != 'nan' and str(nex) != 'nan':
                            t1 = getFloats(prev)[0]
                            t2 = getFloats(nex)[1]
                            words = [getword(keys[i - 1]), getword(keys[i]), getword(keys[i + 1])]
                            getAudioChunk(t1, t2, speaker_id, word, 0)
                            times = getWordTimeoffs(getword(keys[i]), words)
                            # vals[i] = str(times)
                            # print(times)
                            if times:
                                vals[i] = str(times)
                                mfccs, calculatedKeys = calculatedMFCCs(speaker_id, word, vals[i], 1, calculatedKeys)
                                # mfccs = normalise(mfccs)
                                out = [speaker_id, ne] + mfccs + [word]
                                temp = pd.Series(out, index = output_columns)
                                mfcc_output = mfcc_output.append(temp,  ignore_index=True)
                                # df1.iloc[index, i] = mfccs
                    
                
                    # mfccs, calculatedKeys = calculatedMFCCs(speaker_id, word, vals[i], 1, calculatedKeys)
                    # mfccs = normalise(mfccs)
                    # if mfccs:
                        


                            


                    





# df.to_excel(r'/home/vamshi/test.xlsx', index = False, header=True)


            

#         if i > 1 and str(vals[i - 1]) != 'nan':
#             prev_endTime = getFloats(vals[i - 1])[1]
#             if str(vals[i]) != 'nan':
#                 # print(i, keys[i], vals[i])
#                 this_start = getFloats(vals[i])[0]
#                 if this_start > prev_endTime:
#                     print(keys[i])
#                     for k in range(i, 70):
#                         if  checkSameKey(keys[i], keys[k]):
#                             print(keys[i], keys[k])
#                             vals[i], vals[k] = vals[k], vals[i]
                            
                    
#             else:
#                 print("nan: ", keys[i])
#                 # print(checkSameKey(keys[i], keys[i - 1]))
        temp = pd.Series(vals[0:70], index= keys[0:70])
        output = output.append(temp,  ignore_index=True)
output.to_excel(r'/home/malkaiv/project/final/recordings/ind_new_word_local.xlsx', index = False, header=True)
mfcc_output.to_excel(r'/home/malkaiv/project/final/recordings/ind_mfccs.xlsx', index = False, header=True)
df1.to_excel(r'/home/malkaiv/project/final/recordings/ind_dataframe_copy.xlsx', index = False, header=True)
# res = dict(zip(keys, vals))
# # print(res)

