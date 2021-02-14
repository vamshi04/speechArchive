import pandas as pd
import numpy as np
import os
from mp3towav import *
from transcribe import *
from addWord import addWordDict, DictCycler
from wordDataframe import *
from pathlib import Path

from pydub import AudioSegment


from collections import OrderedDict, defaultdict



# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/malkaiv/project/final/Git/speechArchive/finalProject-1cbe5aadc559.json"


################################## Convert Mp3 to Wav ###################################
#########################################################################################
df = pd.read_csv("/home/malkaiv/project/final/recordings/speakers_all.csv")
df = df.rename(columns={"file_missing?": "file_missing"})
df = df[df.file_missing != True]

indian = df[(df.country =='india')]
native = df[df.native_language == 'english']
spanish = df[df.native_language == 'spanish']
print("spanish", spanish.shape)
# spanish['filename'].apply(convert_mp3_wav)


######################## Transcribe: speech to words ##################################
#######################################################################################

speechText = "please call Stella ask her to bring these things with her from the store \
                    six spoons of fresh snow peas five thick slabs of blue cheese and maybe a snack for her \
                    brother Bob we also need a small plastic snake and a big toy frog for the kids she can \
                    scoop these things into three red bags and we will go meet her Wednesday at the train station"
originalCols = speechText.lower().split()


# filename = "/home/malkaiv/project/final/recordings/wav/english1.wav"
# response = wordTimeOffsets(filename, originalCols)
# wordDict = addWordDict(response, filename)
# print(wordDict["please"])
global_df = pd.DataFrame()
missingFiles = []
Word_Class = WordInfo(global_df, missingFiles)
counter = 0
files = spanish['filename']
def create_gobalDF():
    counter = 1
    for i, v  in files.iteritems():
        # print(i)
        print(counter)
        print(str(v))
        df, missing = Word_Class.wordDf(str(v), originalCols)
        counter = counter + 1
    return df, missing
global_df, missingFiles = create_gobalDF()
print(global_df.head())
global_df.to_excel (r'/home/malkaiv/project/final/recordings/spanish_word.xlsx', index = False, header=True)
# df = pd.read_excel(r'/home/malkaiv/project/final/recordings/native_word.xlsx')
# # df.set_index('speaker_id')
# count = 0 
# # outColumns = ["speaker_id"] + 
# output = pd.DataFrame(columns = ["speaker_id"] + originalCols)
# # print(output.columns)
# for index, rows in df.loc[1:3,:"station"].iterrows():
#     if count < 1:
#         count_1 = 0
#         s = rows
#         sDict_1 = s.to_dict(OrderedDict)
#         # print(sDict_1)
#         sDict = DictCycler(sDict_1)
#         keys = list(sDict_1.keys())
#         vals = list(sDict_1.values())

#         ############ #################

#         # curr, prev, _next = 
#         print(float(vals[1]))
#         for i, v in enumerate(vals):
#             if i > 1:
#                 if str(vals[i]) != 'nan' and str(vals[i - 1]) != 'nan' and str(vals[i + 1]) != 'nan':
#                     missing = []
#                     if "_" in keys[i]:
#                         key = keys[i].split("_")[0]
#                     else:
#                         key = keys[i]
#                     # print(key)
#                     # res = ini_list.strip('][').split(', ')
#                     prev_endTime = float(vals[i - 1].strip('][').strip(')(').split(",")[1]) 
#                     next_stTime = float(vals[i + 1].strip('][').strip(')(').split(",")[0]) 
#                     speaker_id = str(vals[0])
#                     # print(speaker_id)
#                     # t1 = t1 * 1000 #Works in milliseconds
#                     # t2 = t2 * 1000
#                     # "/home/malkaiv/project/final/recordings/wav/english1.wav"
#                     newAudio = AudioSegment.from_wav("/home/malkaiv/project/final/recordings/wav/" + speaker_id + ".wav")
#                     if prev_endTime > next_stTime:
#                         print(prev_endTime, next_stTime)
#                         newAudio = newAudio[float((prev_endTime * 1000) - 1000) :float((next_stTime * 1000) + 1000)]
#                         newAudio.export('/home/malkaiv/project/final/recordings/wav/temp/newSong.wav', format="wav")
#                         speech_file = Path("/home/malkaiv/project/final/recordings/wav/temp/newSong.wav")
#                         response1 = wordTimeOffsets("speech_file", [key], 1)
                        
#                         for result in response1.results:
#                             alternative = result.alternatives[0]
#                             for word in alternative.words:
#                                 print(word.word)
#                                 print(prev_endTime + float(word.start_time.seconds + (10 ** -9 * (word.start_time.nanos))))
#             # if str(v) == 'nan':
#             #     missing = []
#             #     if "_" in keys[i]:
#             #         key = keys[i].split("_")[0]
#             #     else:
#             #         key = keys[i]
#             #     print(key)
#             #     if str(vals[i+1]) != 'nan':
#             #         # res = ini_list.strip('][').split(', ')
#             #         prev_endTime = float(vals[i - 1].strip('][').strip(')(').split(",")[1]) 
#             #         next_stTime = float(vals[i + 1].strip('][').strip(')(').split(",")[0]) 
#             #         speaker_id = str(vals[0])
#             #         print(speaker_id)
#             #         # t1 = t1 * 1000 #Works in milliseconds
#             #         # t2 = t2 * 1000
#             #         # "/home/malkaiv/project/final/recordings/wav/english1.wav"
#             #         newAudio = AudioSegment.from_wav("/home/malkaiv/project/final/recordings/wav/" + speaker_id + ".wav")
#             #         if prev_endTime <= next_stTime:
#             #             print(prev_endTime, next_stTime)
#             #             newAudio = newAudio[float((prev_endTime * 1000) - 1000) :float((next_stTime * 1000) + 1000)]
#             #             newAudio.export('/home/malkaiv/project/final/recordings/wav/temp/newSong.wav', format="wav")
#             #             speech_file = Path("/home/malkaiv/project/final/recordings/wav/temp/newSong.wav")
#             #             response1 = wordTimeOffsets("speech_file", [key], 1)
                        
#             #             for result in response1.results:
#             #                 alternative = result.alternatives[0]
#             #                 for word in alternative.words:
#             #                     print(word)
#             #                     if word == key and word.confidence > 0.50:
#             #                         vals[i] = str([(prev_endTime, next_stTime, word.confidence)])
#             #                     else:
#             #                         vals[i] = str(np.nan)
#             #         # if os.path.exists("/home/malkaiv/project/final/recordings/wav/temp/newSong.wav"):
#             #         #     os.remove("/home/malkaiv/project/final/recordings/wav/temp/newSong.wav")
#             #         # else:
#             #         #     print("file does not exist")


#             #         # new_dict = {k: v for k, v in zip(keys, vals)}
#             #         # print(vals)
                

#             #     else:
#             #         break
#         output = output.append(pd.Series(vals, index= ["speaker_id"] + originalCols), ignore_index=True)
#                 # print("prev", type(list(vals[i-1])))
#                 # print("next", type(list(vals[i+1])))
#     # print(keys)
#     # print(vals)

#     count += 1

# # print(output.head())
# output.to_excel(r'/home/malkaiv/project/final/recordings/new_word.xlsx', index = False, header=True)