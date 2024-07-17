import speech_recognition as sr
from datetime import datetime
import os
import numpy as np
from flask import (Blueprint, jsonify, request, current_app)
import librosa as lr
import soundfile as sf
import sys

CWD = os.getcwd()+"/"

def boostAudio(inpFile):
    fileName = inpFile.split("/")[-1]
    DATA_DIR = "/".join(inpFile.split("/")[1:-1])
    TOT_DIR = CWD + DATA_DIR+"/"
    # print("Local Folder",DATA_DIR)
    # print("global Folder",TOT_DIR)
    # print("total file",TOT_DIR+fileName)
    audio_data, fs = sf.read(TOT_DIR+fileName)  # Load audio at original SR
    peak_amp = np.max(np.abs(audio_data))
    scale_factor = 0.9 / peak_amp
    normalized_audio = audio_data * scale_factor
    new_file_name = "boost_"+fileName
    sf.write(TOT_DIR + new_file_name, normalized_audio, fs)

if __name__ == '__main__':
    print("Starting main..")
    get_file = sys.argv[1]
    boostAudio(get_file)
    print("End file")
