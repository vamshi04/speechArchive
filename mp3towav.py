from pathlib import Path 
from pydub import AudioSegment


missing_files = []
def convert_mp3_wav(filename):
    
    fpath = Path("/home/vamshi/project/SpeechArchive/recordings/recordings/wav" + filename + ".wav")
#     fpath = Path("/home/vamshi/project/CV/CV/en/clips/" + filename)
    #     print(fpath)
    if not fpath.is_file():
    	print("File Doesnot exist", filename)
        missing_files.append(filename)
    return missing_files
    #         print(fpath)
     #   sound = AudioSegment.from_mp3(fpath)
     #   sound.export("/home/vamshi/project/SpeechArchive/recordings/wav/" + filename + ".wav", format="wav")
    #else:
        

