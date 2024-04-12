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

from flask import (Blueprint, request, current_app)
# for transforming actual Vwl to SVG vwl points
from skimage.transform import ProjectiveTransform
import numpy as np

homeDir = f'{os.getcwd()}/'
dataDir = 'flaskr/static/participantData/'
bp = Blueprint('process', __name__, url_prefix='/process')

@bp.route('/api/processVwlData', methods=["POST"])
def processVwlData():
    filePath = request.get_json()['gotAudio']
    pathList = filePath.split('/')
    path = '/'.join(pathList[:len(pathList)-1]) + '/'
    filename = pathList[-1]
    print(path,filename)
    f1List, f2List = audioToVwlFormants(path,filename)
    jsonNameFreq = filename.split('.')[0] + '-freq.json'
    jsonNameSVG = filename.split('.')[0] + '-svg.json'
    formantsToJson(f1List,f2List,path,jsonNameFreq,jsonNameSVG)
    id,word,_ = jsonName.split('-')
    relPath = f'../../static/participantData/{id}/{word}/{jsonName}'
    return relPath

def mean(l):
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
    # TODO automate this step
    f0min = 65
    f0max = 1500
    # extract vowels
    pointProcess = praat.call(vowels, "To PointProcess (periodic, cc)", f0min, f0max)
    # source: https://www.fon.hum.uva.nl/praat/manual/Sound__To_Formant__burg____.html
    # retreive formants of vowels
    time_step = 0.0  # if time step = 0.0 (the standard), Praat will set it to 25% of the analysis window length
    formant_ceiling = 5500
    num_formants = 5
    # higher window length to deal with smoothing
    window_len = 0.05
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
    print(f'f1 frequencies: {f1_list}')
    return f1_list, f2_list

def condenseFormantList(formantList,cal=False):
    # If calibration, we need to retain the mins and maxes
    if cal:
        return formantList
    condensed = []
    num = 3
    i = 0
    for i in range(0, int(len(formantList) / num)):
        chunk = formantList[num * i:num * i + num]
        condensed.append(mean(chunk))
    # anything that was extra, append without change
    condensed += formantList[num * i + num:len(formantList)+1]
    return condensed

def formantsToJson(f1List,f2List,path,jsonNameFreq,jsonNameSVG, cal=False):
    idx_vwls = [0]
    # go through formants in f1 and f2 and get the starting indexes for each vowel depending on how big the abs
    # difference between two formants is
    for prev_idx, vwlF1 in enumerate(f1List[1:]):
        prevVwlF1 = f1List[prev_idx]
        prevVwlF2 = f2List[prev_idx]
        vwlF2 = f2List[prev_idx + 1]
        absDiffF1 = abs(vwlF1 - prevVwlF1)
        absDiffF2 = abs(vwlF2 - prevVwlF2)
        diff = 150
        if absDiffF1 >= diff and absDiffF2 >= diff:
            idx_vwls.append(prev_idx + 1)
    idx_vwls.append(len(f1List) - 1)
    print(f'idx vwls {idx_vwls}')
    data = []
    # go through the index list
    prev_idx = 0
    for i, idx in enumerate(idx_vwls[1:]):
        vwlsDict = {"vwl": []}
        tempF1 = condenseFormantList(f1List[prev_idx:idx],cal)
        tempF2 = condenseFormantList(f2List[prev_idx:idx],cal)
        print(f'tempF1 {tempF1}')
        for vwl_idx in range(len(tempF1)):
            f1_vwl = tempF1[vwl_idx]
            f2_vwl = tempF2[vwl_idx]
            tempDict = {"f1": f1_vwl, "f2": f2_vwl}
            vwlsDict["vwl"].append(tempDict)
        if vwlsDict['vwl'] != []:
            data.append(vwlsDict)
        prev_idx = idx_vwls[i + 1]
    print(f'data {data}')
    # Serializing json
    dataSVG = 0
    writeToJson(path, jsonNameFreq, data)
    writeToJson(path, jsonNameSVG, dataSVG)

def writeToJson(path, jsonName, data):
    # Serializing json
    json_object= json.dumps(data, indent=4)
    # Writing to json
    with open(path+jsonName, "w") as outfile:
        outfile.write(json_object)

def maxAndMinOfFormants(data):
    maxF1 = data['vwl'][0]['f1']
    maxF2 = data['vwl'][0]['f2']
    minF1 = maxF1
    minF2 = maxF2
    f1 = 'f1'
    f2 = 'f2'
    for formants in data['vwl']:
        # See if the f1 formant is greater than the current max
        # or if it is less than the current min
        if formants[f1] > maxF1:
            maxF1 = formants[f1]
        elif formants[f1] < minF1:
            minF1 = formants[f1]
        # See if the f2 formant is greater than the current max
        # or if it is less than the current min
        if formants[f2] > maxF2:
            maxF2 = formants[f2]
        elif formants[f2] < minF2:
            minF2 = formants[f2]
    return maxF1, maxF2, minF1, minF2


def loadVowelChartFiles(rootDirectory):
    vowels = {}
    for path, dir, files in os.walk(rootDirectory):
        for file in files:
            if '.json' in file and 'Coordinates' not in file:
                with open(path+file,'r') as f:
                    data = json.load(f)
                    name,word,_ = file.split('-')
                    vowels[word] = data
    coordinates = vowelChartPoints(vowels)
    return coordinates

def vowelChartPoints(vowels):
    ''' vowels is a dictionary {word: data} '''
    words = ['frontHigh','backHigh','frontLow', 'backLow']
    # F = Front, B = Back, H = High, L = Low
    print(f'vowls {vowels}\n')
    for word, vwls in vowels.items():
        for vwl in vwls:
            maxF1, maxF2, minF1, minF2 = maxAndMinOfFormants(vwl)
            if word == words[0]:
                xFH = maxF2
                yFH = minF1
            elif word == words[1]:
                xBH = minF2
                yBH = minF1
            elif word == words[2]:
                xFL = maxF2
                yFL = maxF1
            elif word == words[3]:
                xBL = minF2
                yBL = maxF1


    # m = abs((yt - y1) / (xt - x1))
    # x3 = y4 / m
    # x range, y range (xmin, xmax, ymin, ymax)
    frontHigh = (xFH,yFH)
    backHigh = (xBH,yBH)
    frontLow = (xFL,yFL)
    backLow = (xBL,yBL)
    coordinates = [frontHigh,backHigh,frontLow,backLow]
    return coordinates

def transformArray(actualCoordinates, svgCoordinates):
    t = ProjectiveTransform()
    src = np.asarray(actualCoordinates)
    print(f'src {src}')
    dst = np.asarray(svgCoordinates)
    print(f'dst {dst}')
    if not t.estimate(src, dst): raise Exception("estimate failed")

    # Homogeneous to Euclidean
    # [x, y, w]^T --> [x/w, y/w]^T
    x = t.params[0]
    y = t.params[1]
    w = t.params[2]
    transform = [x,y,w]
    current_app.config.update(TRANSFORM_FREQ_SVG=transform)


def freqToSVG(freq):
    '''
    params freq: list [x,y]
    returns svg: list [xSVG, ySVG]
    '''
    pass
def vowelChartCalibration(id):
    rootDirectory = homeDir + dataDir + id +"/vowelCalibration/"
    pprint(f'in directory {rootDirectory}')
    for path, dir, files in os.walk(rootDirectory):
        for file in files:
            if '.wav' in file:
                f1, f2 = audioToVwlFormants(path,file)
                jsonName = f"{file.split('.')[0]}-vwlCal.json"
                formantsToJson(f1,f2,path,jsonName, True)
        coordinates = loadVowelChartFiles(path)

        # Serializing json
        json_object = json.dumps(coordinates, indent=4)

        # Writing to sample.json
        jsonName = "vwlChartCoordinates.json"
        with open(path + jsonName, "w") as outfile:
            outfile.write(json_object)



if __name__ == '__main__':
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
            vowelChartCalibration(id)
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