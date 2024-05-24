import speech_recognition as sr
from datetime import datetime
import os
import numpy as np
from flask import (Blueprint, jsonify, request, current_app)
import librosa as lr
import soundfile as sf

MAIN_DIR = os.getcwd() + "/" # "/Users/hearth/PycharmProjects/vwl_const_algo/"
DATA_DIR = MAIN_DIR + "flaskr/static/participantData/"


bp = Blueprint('audio', __name__, url_prefix='/audio')
@bp.route('/api/record', methods=('GET', 'POST'))
def record():
    print("in record")
    data = request.get_json()
    word = data['word']
    participantID = current_app.config['USER_ID']
    print(participantID)
    cal = data['cal']
    print(cal,type(cal))
    gotAudio = recordFile(word,participantID,cal=cal)
    return jsonify({'gotAudio': gotAudio})



def recordFile(word, participantID, debug=False, cal='False', secondTime=False):
    # obtain lang_files from the microphone
    import speech_recognition as sr
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please wait. Calibrating microphone...")
        # listen for 1 second and create the ambient noise energy level
        r.adjust_for_ambient_noise(source, duration=1)
        print(f"Please say {word}")
        # timeout after 5 seconds of not hearing anything and let user know that there was a timeout
        timeout = 5
        try:
            audio = r.listen(source, timeout=timeout)
            print("Heard you, just a moment\n")
            audioObtained = True
        except sr.WaitTimeoutError:
            print("We weren't able to hear you. Try talking a little louder!\n")
            audioObtained = False
            return 'Quiet'
            if not secondTime:
                recordFile(word, participantID,debug,L1,secondTime=True)
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

        folderID = f"{participantID}/"

        # If we're gathering words for vowel calibration, save the files in the same folder.
        if cal == 'True':
            file_name = participantID + "-" + word
            folderWORD = f"vowelCalibration/"
            new_file_name = folderID + folderWORD + file_name + ".wav"
        else:
            file_name = participantID + "-" + word + "-" + date_time
            print(file_name)
            folderWORD = f"{word}/"
            new_file_name = folderID + folderWORD + file_name + ".wav"

        # Create user Directory if it doesn't exist
        if not os.path.exists(DATA_DIR+folderID):
            os.mkdir(DATA_DIR+folderID)
        # create word directory if it doesn't exist
        if not os.path.exists(DATA_DIR+folderID+folderWORD):
            os.mkdir(DATA_DIR+folderID+folderWORD)

        with open(DATA_DIR + new_file_name , "wb") as f:
            f.write(wav_data)

        # Normalize audio
        # this is for boosting ;) just for you Dipayan
        audio_data, fs = sf.read(DATA_DIR + new_file_name)  # Load audio at original SR
        peak_amp = np.max(np.abs(audio_data))
        scale_factor = 0.9 / peak_amp
        normalized_audio = audio_data * scale_factor
        sf.write(DATA_DIR + new_file_name, normalized_audio, fs)

        return DATA_DIR + new_file_name
    return "NoDataRecorded"


def recordCalibrationFiles(id):
    words = ['bee','boo','baa','baw']
    pointLabels = ['frontHigh','backHigh','frontLow','backLow']
    for idx, word in enumerate(words):
        speak = f"The next word you'll be asked to say is \t{word}, {info[idx]}"
        print(speak)
        recordFile(word,id,cal=pointLabels[idx])
    return "Recorded calibration files."



def main():
    feedback = ''
    print(sys.argv)
    if "debug" in sys.argv:
        recordFile("bata",debug=True)
        return ''
    try:
        idIDX = sys.argv.index('-id') + 1
    except ValueError:
        feedback += "You need to specify participant id with flag '-id'\n"
    # If the Speaker Calibration flag is set, then run recordCalibrationFiles. This only works if id was also set.
    try:
        id = sys.argv[idIDX]
    except UnboundLocalError:
        feedback += "Include an id name along with the -id flag, e.g. -id [id_name]"
        return feedback
    print('calibrate' in sys.argv)
    if "-calibrate" in sys.argv:
        recordCalibrationFiles(id)
        return ''

    # If any flag was not properly set, then feedback won't be zero and it should be returned
    if len(feedback) != 0:
        return feedback

    eng_words = ['cheese','big','beg','bag','ruler','dune','could','cup']
    for word in eng_words:
        recordFile(word,id)
    return ''


if __name__ == '__main__':
    info='''
    This file can be run with the following flags
    -debug : prints out microphone information
    The following flags are required if debug is not set 
        id : highest level folder name where the speaker's audio files will be stored
    -calibrate : record files for vowel chart calibration
    '''
    import time
    import sys

    start_time = time.time()
    feedback = main()
    if len(feedback) != 0:
        print(feedback)
        print(info)


