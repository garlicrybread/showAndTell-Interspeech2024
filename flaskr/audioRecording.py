import speech_recognition as sr
from datetime import datetime
import os

MAIN_DIR = os.getcwd() + "/" # "/Users/hearth/PycharmProjects/vwl_const_algo/"
DATA_DIR = MAIN_DIR + "flaskr/participantData/"

def recordFile(word, participantID, debug=False, L1=True, speakerCalibration=False, secondTime=False):
    # obtain lang_files from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please wait. Calibrating microphone...")
        # listen for 1 second and create the ambient noise energy level
        r.adjust_for_ambient_noise(source, duration=1)
        print(f"Please say {word}")
        # timeout after 5 seconds of not hearing anything and let user know that there was a timeout
        timeout = 3
        try:
            audio = r.listen(source, timeout=timeout)
            print("Heard you, just a moment\n")
            audioObtained = True
        except sr.WaitTimeoutError:
            print("We weren't able to hear you. Try talking a little louder!\n")
            audioObtained = False
            if not secondTime:
                recordFile(word, participantID,debug,L1,speakerCalibration,secondTime=True)
    # to give speaker time in case they say the word again
    time.sleep(2)
    if audioObtained:
        if debug:
            p = pyaudio.PyAudio()
            device_index = p.get_default_input_device_info()["index"]
            device_info = p.get_device_info_by_index(device_index)
            channels = device_info["maxInputChannels"]
            print(f"There are {channels} channel(s)")
            rate = int(device_info["defaultSampleRate"])
            # format = pyaudio.paInt16  # or pyaudio.paFloat32, depsamplesing on your microphone
            # stream = p.open(format=format, channels=channels, rate=rate, input=True)
            FS = rate
            print(f"The framerate of the microphone is {FS} Hz")

        # get wave data from lang_files
        wav_data = audio.get_wav_data()

        # save data to file
        now = datetime.now()
        date_time = now.strftime("%Y_%m_%d_%H%M%S")
        file_name = participantID + "-" + word + "-" + date_time

        folderID = f"{participantID}/"

        # If we're gathering words for vowel calibration, save the files in the same folder.
        if speakerCalibration:
            folderWORD = f"vowelCalibration/"
        else:
            folderWORD = f"{word}/"

        # Create user Directory if it doesn't exist
        if not os.path.exists(DATA_DIR+folderID):
            os.mkdir(DATA_DIR+folderID)
        # create word directory if it doesn't exist
        if not os.path.exists(DATA_DIR+folderID+folderWORD):
            os.mkdir(DATA_DIR+folderID+folderWORD)

        new_file_name = folderID + folderWORD + file_name + ".wav"
        # print(new_file_name)

        with open(DATA_DIR + new_file_name , "wb") as f:
            f.write(wav_data)

        return DATA_DIR + new_file_name
    return "NoDataRecorded"


def recordCalibrationFiles(id):
    words = ['beet','bat','bow','bot','boot']
    info = ["as in the vegetable", "as in the flying mammal",
            "as in bend forward", "as in robot", "as in what cowboys wear"]
    for idx, word in enumerate(words):
        speak = f"The next word you'll be asked to say is \t{word}, {info[idx]}"
        print(speak)
        recordFile(word,id,L1=False,speakerCalibration=True)

    return "Recorded calibration files."



def main():
    feedback = ''
    print(sys.argv)
    if "debug" in sys.argv:
        recordFile("bata",debug=True)
        return ''
    try:
        id = sys.argv.index('-id') + 1
    except ValueError:
        feedback += "You need to specify participant id with flag '-id'\n"
    # If the Speaker Calibration flag is set, then run recordCalibrationFiles. This only works if id was also set.
    if "speakerCalibration" in sys.argv:
        try:
            recordCalibrationFiles(sys.argv[id])
            return ''
        except UnboundLocalError:
            print("UnboundLocalError")
            pass
    # Check to make sure that L1 or L2 speaker was specified
    elif 'L1' in sys.argv:
        speaker = 'L1'
    elif 'L2' in sys.argv:
        speaker = 'L2'
    else:
        feedback += "Missing L1 and L2 flags."

    # If any flag was not properly set, then feedback won't be zero and it should be returned
    if len(feedback) != 0:
        return feedback
    return ''


if __name__ == '__main__':
    info='''
    This file can be run with the following flags
    -debug : prints out microphone information
    The following flags are required if debug is not set (choice between L1 or L2 NOT BOTH!)
        id : highest level folder name where the speaker's audio files will be stored
        L1 : collect L1 speaker's data or
        L2 : collect L2 speaker's data
    -speakerCalibration : record files for vowel chart calibration
    '''
    import time
    import sys

    start_time = time.time()
    feedback = main()
    if len(feedback) != 0:
        print(feedback)
        print(info)


