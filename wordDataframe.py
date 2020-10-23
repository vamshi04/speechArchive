from addWord import addWordDict
from transcribe import wordTimeOffsets 
import pandas as pd
from google.cloud import speech_v1p1beta1 as speech
# word_np = np.array() # size = (max(repetation of a word)) x (no. of words)

# word_np 

global_df = pd.DataFrame()
missingFiles = []

class WordInfo:
    
    def __init__(self, global_df, missingFiles):
        self.global_df = global_df
        self.missingFiles = missingFiles
        
    
    def wordDf(self, filename):
        speech_file = Path("/home/vamshi/project/SpeechArchive/recordings/wav/" + filename + ".wav")
        if speech_file.exists ():
            response = wordTimeOffsets(selffilename)
            temp = 0
            word_dict = addWordDict(response, filename)

            if self.global_df.empty:
                print("empty")
                self.global_df = pd.DataFrame.from_dict(word_dict, orient='index')
                self.global_df = self.global_df.transpose()
            else:
                self.global_df.head()
                temp = pd.DataFrame.from_dict(word_dict, orient='index')
                temp = temp.transpose()
                self.global_df = pd.concat([self.global_df,temp], axis=0, ignore_index=True)
        else:
            self.missingFiles.append(filename)
            
        return self.global_df, self.missingFiles

    def concat_df(self, word_dic):
        if self.global_df.empty:
            print("empty")
            self.global_df = pd.DataFrame.from_dict(word_dic, orient='index')
            self.global_df = self.global_df.transpose()
        else:
            self.global_df.head()
            temp = pd.DataFrame.from_dict(word_dic, orient='index')
            temp = temp.transpose()
            self.global_df = pd.concat([self.global_df,temp], axis=0, ignore_index=True)
        return self.global_df
# Word_Class = Word_Info()

Word_Class = Word_Info(global_df, missingFiles)

