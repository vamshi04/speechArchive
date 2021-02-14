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

def sortRow(vals):
    for i, v in enumerate(vals):   ## looping on each row
        if i > 1 and str(vals[i - 1]) != 'nan':
            prev_stTime = getFloats(vals[i - 1])[0]
            prev_endTime = getFloats(vals[i - 1])[1]
            if str(vals[i]) != 'nan':
                # print(i, keys[i], vals[i])
                this_start = getFloats(vals[i])[0]
                if this_start < prev_endTime:
                    # print(keys[i])
                    for k in range(i, len(keys) - 1):
                        if checkSameKey(keys[i], keys[k]):
                            # print(keys[i], keys[k])
                            vals[i], vals[k] = vals[k], vals[i]
                
                        # i = i - 1 
                ############## How to loop back to previous item  #########
    return vals


# def get_nan(vals):
#     missing = 0
#     missing_keys = {}
#     for i, v in enumerate(vals):
#         if i > 1:

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
 
# outColumns = ["speaker_id"] + 
output = pd.DataFrame(columns = column_names)
# print(output.columns)
for index, rows in df.loc[:,:].iterrows():  
    # if count < 4:
        # count_1 = 0
    temp = pd.DataFrame()
    s = rows
    sDict_1 = s.to_dict(OrderedDict)
    # print(sDict_1)
    # sDict = DictCycler(sDict_1)
    keys = list(sDict_1.keys())
    vals = list(sDict_1.values())
    print("speaker_id", vals[0])
    vals = sortRow(vals)
    # vals = sortRow(vals)
    missing = 0
    flag = 1
    for i, v in enumerate(vals):   ## looping on each row
        
        missing_keys = []
        if i > 0 and str(vals[i]) == 'nan':
            
            if i == 1:
                if str(vals[i + 1]) != 'nan':
                    missing_keys.append(keys[i + 1])
                    next_stTime = getFloats(vals[i + 1])[0]

                    for k in range(2, len(vals) - 1):
                        if str(vals[k]) != 'nan' and k < len(vals) - 2:
                            this_end = getFloats(vals[k])[1]
                            if next_stTime == this_end:
                                # print("")
                                vals[i], vals[k] = vals[k], vals[i]
                                flag = 0
            
            else:
                for k in range(70, len(keys) - 1):
                    if checkSameKey(keys[i], keys[k]):
                        if str(vals[k]) != 'nan':
                            vals[i], vals[k] = vals[k], vals[i]
                            flag = 0
            if flag:
                missing += 1

                # if i < len(vals) - 2 and str(vals[i - 1]) != 'nan':    
                #     prev_stTime = getFloats(vals[i - 1])[0]
                #     missing_keys.append(keys[i - 1])
                # if i < len(vals) - 2 and str(vals[i + 1]) != 'nan':
                #     missing_keys.append(keys[i +1])
                #     next_endTime = getFloats(vals[i + 1])[1]
                
                # vals[i] = str([(prev_stTime, next_endTime, 0.5)])


                ############## How to loop back to previous item  #########

                    

                            
                    
        #     else:
        #         missing += 1
        #         print(len(vals))
        #         if i < len(vals) -2 and str(vals[i + 1]) != 'nan':
        #             next_endTime = getFloats(vals[i + 1])[1]
        #             words = [keys[i - 1], keys[i], keys[i + 1]] 
        #             missing_keys[keys[i]] = [prev_stTime, next_endTime, words]

                
        #         # print("nan: ", keys[i])
        #         # print(checkSameKey(keys[i], keys[i - 1]))
        #     print("missing Dict: ", missing_keys)
        #     print(missing)

        # if str(vals[1]) == 'nan':
        #     missing += 1
    
    temp = pd.Series(vals[0:70], index= keys[0:70])
    output = output.append(temp,  ignore_index=True)
    # count += 1
    # output = output.append(temp,  ignore_index=True)
output.to_excel(r'/home/malkaiv/project/final/recordings/new_word_sorted.xlsx', index = False, header=True)
res = dict(zip(keys[0:70], vals[0:70]))
# print(res)

