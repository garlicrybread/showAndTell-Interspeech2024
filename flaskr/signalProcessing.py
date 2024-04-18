# so I can know how long it takes for the program to run
import sys
import time
import os
# extracting vwl formant
from scipy.io import wavfile
import parselmouth
from parselmouth import praat
from pprint import pprint

# writing to json
import json

from flask import (Blueprint, request, current_app, jsonify)
# for transforming actual Vwl to SVG vwl points
import numpy as np

homeDir = f'{os.getcwd()}/'
dataDir = 'flaskr/static/participantData/'
bp = Blueprint('signalProcessing', __name__, url_prefix='/signalProcessing')

@bp.route('/api/processVwlData', methods=["POST"])
def processVwlData():
    filePath = request.get_json()['gotAudio']
    pathList = filePath.split('/')
    path = '/'.join(pathList[:len(pathList)-1]) + '/'
    filename = pathList[-1]
    print(path,filename)
    f1List, f2List = audioToVwlFormants(path,filename)
    jsonName = filename.split('.')[0] + '.json'
    data = formantsToJsonFormat(f1List,f2List)
    writeToJson(path,jsonName,data)
    id,word,_ = jsonName.split('-')
    relPath = f'../../static/participantData/{id}/{word}/{jsonName}'
    return relPath

@bp.route('/api/freqToSVG',methods=['POST'])
def freqToSVG():
    # todo: update function description
    '''
    params freq: list [x,y]
    returns svg: list [xSVG, ySVG]
    '''
    # freq is a 3x1
    def yToX(y):
        '''assumes y to x is not a straight line'''
        m = (fl[1] - fh[1]) / (fl[0] - fh[0])
        b = fl[1] - m * fl[0]
        return (y - b) / m
    freq = request.get_json()
    print(f'freq {freq}')
    tempList = [[freq['f2']],[freq['f1']],[1]]
    freq = np.array(tempList)
    # t is a 3x3
    t = np.array(current_app.config['TRANSFORM_FREQ_SVG'])
    x,y,w = np.dot(t,freq).tolist()
    w = sum(w)
    x = sum(x)/w
    y = sum(y)/w

    fh, bh, fl, bl = current_app.config['SVG_COORDINATES']
    print(fh,bh,fl,bl)
    if y < bh[1]:
        print(f'y outside of bounds {y}')
        y = bh[1]
    elif y > bl[1]: y = bh[1]

    leftBoundaryX = yToX(y)
    if x < leftBoundaryX: x = leftBoundaryX
    elif x > bh[0]: x = bh[0]

    data = {'svg': [x,y]}
    return jsonify(data)

@bp.route('/api/svgToConfig',methods=['POST'])
def svgToConfig():
    svg = request.get_json()
    current_app.config.update(SVG_COORDINATES=svg)
    print(f'\ncurrent app {current_app.config["SVG_COORDINATES"]}\n')
    return jsonify({'success':True})

def mean(l):
    if len(l) != 0:
        return sum(l) / len(l)

def audioToVwlFormants(path,file_name):
    vocalToolKitDir = '~/plugin_VocalToolkit/'
    extractVwlFile = "extractvowels.praat"
    file = path + file_name
    # read the wav file and get the samplerate and data
    samplerate, data = wavfile.read(file)
    # fft_data = np.fft.fft(data)

    sound = parselmouth.Sound(file)

    vowels = praat.run_file(sound, vocalToolKitDir + extractVwlFile,0,0)[0]
    # TODO after deadline automate this step
    # charlotte 65, 500, 5500, 4
    f0min = 65
    f0max = 500
    # extract vowels
    pointProcess = praat.call(vowels, "To PointProcess (periodic, cc)", f0min, f0max)
    # source: https://www.fon.hum.uva.nl/praat/manual/Sound__To_Formant__burg____.html
    # retreive formants of vowels
    time_step = 0.0  # if time step = 0.0 (the standard), Praat will set it to 25% of the analysis window length
    formant_ceiling = 5000
    num_formants = 4
    # higher window length to deal with smoothing
    window_len = 0.025
    preemphasis = 100
    formants = praat.call(vowels, "To Formant (burg)", time_step, num_formants, formant_ceiling, window_len,
                          preemphasis)
    numPoints = praat.call(pointProcess, "Get number of points")
    f1_list = []
    f2_list = []
    for point in range(0, numPoints):
        point += 1
        t = praat.call(pointProcess, "Get time from index", point)
        f1 = praat.call(formants, "Get value at time", 1, t, 'Hertz', 'Linear')
        f2 = praat.call(formants, "Get value at time", 2, t, 'Hertz', 'Linear')
        # filter out "nan"
        if f1 > 0:
            f1_list.append(f1)
            f2_list.append(f2)
    return f1_list, f2_list

def condenseFormantList(formantList,cal=False):
    # If calibration, we need to retain the mins and maxes
    length = len(formantList)
    if cal:
        return formantList
    condensed = []
    num = 2
    i = 0
    for i in range(0, int(length / num)):
        chunk = formantList[num * i:num * i + num]
        condensed.append(mean(chunk))
    # anything that was extra, append without change
    if length % num != 0:
        if length <= num - 1:
            condensed.append(mean(formantList))
        else:
            condensed.append(mean(formantList[num * i + num : length+1]))

    return condensed

def formantsToJsonFormat(f1List,f2List,cal=False):
    idx_vwls = [0]
    # go through formants in f1 and f2 and get the starting indexes for each vowel depending on how big the abs
    # difference between two formants is
    for prev_idx, vwlF1 in enumerate(f1List[1:]):
        prevVwlF1 = f1List[prev_idx]
        prevVwlF2 = f2List[prev_idx]
        vwlF2 = f2List[prev_idx + 1]
        absDiffF1 = abs(vwlF1 - prevVwlF1)
        absDiffF2 = abs(vwlF2 - prevVwlF2)
        diff = 200
        if absDiffF1 >= diff and absDiffF2 >= diff:
            idx_vwls.append(prev_idx + 1)
    idx_vwls.append(len(f1List))
    data = []
    # go through the index list; only takes the first vowel
    prev_idx = 0
    for i, idx in enumerate(idx_vwls[1:2]):
        vwlsDict = {"vwl": []}
        tempF1 = condenseFormantList(f1List[prev_idx:idx],cal)
        tempF2 = condenseFormantList(f2List[prev_idx:idx],cal)
        for vwl_idx in range(len(tempF1)):
            f1_vwl = tempF1[vwl_idx]
            f2_vwl = tempF2[vwl_idx]
            tempDict = {"f1": f1_vwl, "f2": f2_vwl}
            vwlsDict["vwl"].append(tempDict)
        if vwlsDict['vwl'] != []:
            data.append(vwlsDict)
        prev_idx = idx_vwls[i + 1]
    # Serializing json
    print(data)
    return data

def writeToJson(path, jsonName, data):
    # Serializing json
    json_object= json.dumps(data, indent=4)
    # Writing to json
    with open(path+jsonName, "w") as outfile:
        outfile.write(json_object)
    print(f'json filename {path+jsonName}')



if __name__ == '__main__': # pragma: no cover
    start_time = time.time()
    # hardcoded for now
    rootDirectory = homeDir + dataDir
    try:
        idx = sys.argv.index('-id')+1
        id = sys.argv[idx]
    except:
        print('Specify the -id')
    if 'cal' in sys.argv:
        try:
            print("Calibrating vowel chart coordinates...")
            # todo: move coordinate code into coordinates
            calAudioToCoordinatesJson(id)
        except ValueError as e:
            print("Specify the -id")
            print(e)
    else:
        for path, dir, files in os.walk(rootDirectory):
            path = path + '/'
            for file in files:
                if 'vowelCalibration' not in path and ('.wav' in file) and (id in file):
                    print(file)
                    f1, f2 = audioToVwlFormants(path,file)
                    jsonName = f'{file.split(".")[0]}.json'
                    print(jsonName)
                    formantsToJson(f1,f2,path,jsonName)
        print("--- %s milliseconds ---" % ((time.time() - start_time)*1000))