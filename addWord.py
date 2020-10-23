def addWordDict(response, filename):
    word_dict = {}
    word_dict["speaker_id"] = filename
    for result in response.results:
        alternative = result.alternatives[0]
#             print(alternative.words)

        for word in alternative.words:
#                 print(word)
#                 fname = {filename:[]}
            word_str = str(word.word)
            start = float(word.start_time.seconds + (10 ** -6 * (word.start_time.microseconds)))
            end = float(word.end_time.seconds + (10 ** -6 * (word.end_time.microseconds)))
#                 speaker[str(filename)] 

            if word_str in word_dict:
                # print("word_str: ", type(self.word_dict[word_str])) 
                word_dict[word_str].append((start, end))
            else:
                word_dict[word_str] = [(start, end)] 
            # print(u"Word: {}, start: {} , end: {}".format(word.word, \
            # word.start_time.seconds + (10 ** -9 * (word.start_time.nanos)),\
            # word.end_time.seconds + (10 ** -9 * (word.end_time.nanos))))
#         word_pd = pd.DataFrame.from_dict(self.word_dict)

        return word_dict
