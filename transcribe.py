import wave
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums
from google.cloud.speech_v1p1beta1 import types
import sys, io
from pathlib import Path


# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/malkaiv/project/final/Git/speechArchive/finalProject-1cbe5aadc559.json"
def wordTimeOffsets(filename, phrases, flag):

    client = speech.SpeechClient()

    if flag == 0:
        speech_file = "/home/malkaiv/project/final/recordings/wav/" + str(filename) + ".wav"
    else:
        print("in flag = 1")
        speech_file = "/home/malkaiv/project/final/recordings/wordsWav/" + str(filename) +".wav"
    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    with wave.open(speech_file, 'rb') as wave_file:
        frame_rate = wave_file.getframerate()

    # speechText = "please call Stella ask her to bring these things with her from the store \
    #                     six spoons of fresh snow peas five thick slabs of blue cheese and maybe a snack for her \
    #                     brother Bob we also need a small plastic snake and a big toy frog for the kids she can \
    #                     scoop these things into three red bags and we will go meet her Wednesday at the train station"
    # phrases = speechText.lower().split()


    boost = 20.0
    speech_contexts_element = {"phrases": phrases, "boost": boost}
    speech_contexts = [speech_contexts_element]

    config = types.RecognitionConfig(
        speech_contexts=speech_contexts,
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=frame_rate,
        language_code="en-US",
        enable_word_time_offsets=True,
        enable_word_confidence=True,
    )
    # print(client.recognize(config=config, audio=audio))
    # first = response.results[0].alternatives[0]
    # print("{}\n{}".format(first.transcript, first.confidence))
    return client.recognize(config=config, audio=audio)


