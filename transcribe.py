from google.cloud import speech_v1p1beta1 as speech

def wordTimeOffsets(filename):
    """Transcribe the given audio file asynchronously and output the word time
    offsets."""
    
    client = speech.SpeechClient()

    with open(filename, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    #     sample_rate_hertz=16000,                #
        language_code="en-US",
        enable_word_confidence=True,
        enable_word_time_offsets=True
        )

    return client.recognize(request={"config": config, "audio": audio})

