def addWordDict(response, filename):
    word_dict = {}
    word_dict["speaker_id"] = filename
    for result in response.results:
        alternative = result.alternatives[0]

        for word in alternative.words:
            punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
            word_str = str(word.word).lower()
            temp = ""

            #remove formatting to the word
            for char in word_str:
                if char not in punctuations:
                    temp += char
            word_str = temp 
            
            start = float(word.start_time.seconds + (10 ** -9 * (word.start_time.nanos)))
            end = float(word.end_time.seconds + (10 ** -9 * (word.end_time.nanos)))
            confidence = float(word.confidence)

            if word_str not in word_dict:
                word_dict[word_str] = [(start, end, confidence)] 
                # word_dict[word_str].append((start, end, confidence))

            else:
                count = 1
                while True:
                    check = word_str + "_" + str(count)
                    if check not in word_dict:
                        word_dict[check] = [(start, end, confidence)] 
                        break
                    else:
                        count += 1
                        continue

                # word_dict[word_str] = [(start, end, confidence)] 

        return word_dict


import itertools


class DictCycler:
    def __init__(self, data):
        self.data = data
        self.iterator = itertools.cycle(data)
        self.jump_to_previous = len(data) - 2

    def next(self):
        return self.data[next(self.iterator)]

    def previous(self):
        prev = itertools.islice(self.iterator, self.jump_to_previous, None)
        return self.data[next(prev)]