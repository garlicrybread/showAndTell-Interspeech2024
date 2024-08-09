from flaskr.autocorrelationVwlExtract import (
    extractVwlBoundaries
)

import os
import scipy.io.wavfile as wav
from math import floor
DATA_DIR = f'{os.getcwd()}/flaskr/static/participantData/'
flaskrDir = f'{os.getcwd()}/flaskr/'

def test_extractVwlBoundaries():
    id = 'testData_misc'
    # calibration files to test
    word = 'frontHigh'
    filename = f'{id}-{word}.wav'
    path = DATA_DIR + f'{id}/vowelCalibration/'
    fs, _ = wav.read(path+filename)
    data, tList = extractVwlBoundaries(path,filename)
    start = 0.6599999999999999
    end = 0.8099999999999999
    frameLen = round(fs * (end - start))
    assert len(data) == frameLen
    assert tList == [start,end]

    path = f'{DATA_DIR}/voicingDegreeTests/'
    word = 'bait_noisy'
    filename = f'{word}.wav'
    fs, _ = wav.read(path+filename)
    data, tList = extractVwlBoundaries(path,filename)
    start = 2.61
    end = 2.6999999999999997
    frameLen = floor(fs * (end - start))
    assert len(data) == frameLen
    assert tList == [start,end]

    word = 'dipayan_bait'
    filename = f'{word}.wav'
    fs, _ = wav.read(path+filename)
    data, tList = extractVwlBoundaries(path,filename)
    start = 1.65
    end = 1.89
    frameLen = floor(fs * (end - start))
    assert len(data) == frameLen
    assert tList == [start,end]
