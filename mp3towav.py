from pathlib import Path
from pydub import AudioSegment


missing_files = []

def convert_mp3_wav(filename):
    fpath = Path("/home/malkaiv/project/final/recordings/recordings/" + filename + ".mp3")

    if fpath.is_file():

        sound = AudioSegment.from_mp3(fpath)
        sound.export("/home/malkaiv/project/final/recordings/wav/" + filename + ".wav", format="wav")
    else:

        print("File Doesnot exist", filename)
        missing_files.append(filename)
        
    return missing_files
