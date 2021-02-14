import pandas as pd
from collections import OrderedDict, defaultdict



def checkSameKey(str1, str2):
    equals = False
    if "_" in str1:
        str1 = str1.split("_")[0]
    elif "_" in str2:
        str2 = str2.split("_")[0]
    if str1 == str2:
        equals = True
    return equals
    

def getFloats(str1):
    Returnlist = str1.strip('][').strip(')(').split(",")
    return [float(i) for i in Returnlist] #convert each element into float and return the list
    # return Returnlist

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

df = pd.read_excel(r'/home/malkaiv/project/final/recordings/native_word.xlsx')
# df.set_index('speaker_id')
count = 0 
# outColumns = ["speaker_id"] + 
output = pd.DataFrame(columns = column_names)
# print(output.columns)
for index, rows in df.loc[1:3,:"station"].iterrows():
    if count < 4:
        count_1 = 0
        s = rows
        sDict_1 = s.to_dict(OrderedDict)
        # print(sDict_1)
        # sDict = DictCycler(sDict_1)
        keys = list(sDict_1.keys())
        vals = list(sDict_1.values())
        # print("value: ", vals[1])    
        for i, v in enumerate(vals):
            if i > 1 and str(vals[i - 1]) != 'nan':
                prev_endTime = getFloats(vals[i - 1])[1]
                if str(vals[i]) != 'nan':
                    # print(i, keys[i], vals[i])
                    this_start = getFloats(vals[i])[0]
                    if this_start > prev_endTime:
                        print(keys[i])
                        for k in range(i, 70):
                            if  checkSameKey(keys[i], keys[k]):
                                print(keys[i], keys[k])
                                vals[i], vals[k] = vals[k], vals[i]
                                
                        
                else:
                    print("nan: ", keys[i])
                    # print(checkSameKey(keys[i], keys[i - 1]))
    count += 1
    output = output.append(pd.Series(vals, index= keys), ignore_index=True)
output.to_excel(r'/home/malkaiv/project/final/recordings/new_word_sorted.xlsx', index = False, header=True)
res = dict(zip(keys, vals))
# print(res)

