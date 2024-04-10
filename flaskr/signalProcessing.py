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

from flask import (Blueprint, request)


homeDir = f'{os.getcwd()}/'
dataDir = 'flaskr/static/participantData/'
bp = Blueprint('process', __name__, url_prefix='/process')

@bp.route('/api/processVwlData', methods=["POST"])
def processVwlData():
    print('In process data',)
    filePath = request.get_json()['gotAudio']
    pathList = filePath.split('/')
    print(f'pathlist {pathList}')
    path = '/'.join(pathList[:len(pathList)-1]) + '/'
    filename = pathList[-1]
    print(path,filename)
    f1List, f2List = audioToVwlFormants(path,filename)
    f1List = condenseFormantList(f1List)
    f2List = condenseFormantList(f2List)
    jsonName = filename.split('.')[0] + '.json'
    formantsToJson(f1List,f2List,path,jsonName)
    id,word,_ = jsonName.split('-')
    relPath = f'../../static/participantData/{id}/{word}/{jsonName}'
    print(relPath)
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

    vowels = praat.run_file(sound, vocalToolKitDir + extractVwlFile, 0, 0)[0]

    # TODO automate this step
    f0min = 100
    f0max = 250

    # extract vowels
    pointProcess = praat.call(vowels, "To PointProcess (periodic, cc)", f0min, f0max)

    # source: https://www.fon.hum.uva.nl/praat/manual/Sound__To_Formant__burg____.html
    # retreive formants of vowels
    time_step = 0.0  # if time step = 0.0 (the standard), Praat will set it to 25% of the analysis window length
    formant_ceiling = 4500
    num_formants = 4
    window_len = 0.015
    preemphasis = 50
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

def formantsToJson(f1List,f2List,path,jsonName,cal=False):
    idx_vwls = [0]
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
    data = []
    # go through the index list
    prev_idx = 0
    for i, idx in enumerate(idx_vwls[1:]):
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
    pprint(data)

    # Serializing json
    json_object = json.dumps(data, indent=4)

    # Writing to sample.json
    print(path+jsonName)
    with open(path+jsonName, "w") as outfile:
        outfile.write(json_object)

def maxAndMinOfFormants(data):
    pprint(data)
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


def vowelChartPoints(rootDirectory):
    '''hardcoded for eee, ooo, and awe'''
    # todo: fix so that coordinates are correct might mean fixing max and min of formants too

    vowels = {}
    for path, dir, files in os.walk(rootDirectory):
        for file in files:
            if '.json' in file and 'Coordinates' not in file:
                with open(path+file,'r') as f:
                    data = json.load(f)
                    name,word,date,_ =file.split('-')
                    vowels[word] = data
    # json data in the form of list(dictionary
    edges = {}
    words = ['eee','ooo','awe']
    for word, vwls in vowels.items():
        ymin = []
        for vwl in vwls:
            pprint(vwl)
            maxF1, maxF2, minF1, minF2 = maxAndMinOfFormants(vwl)
            if word == words[0]:
                xmax = maxF2
                ymin.append(minF1)
            elif word == words[1]:
                xmin = minF2
                ymin.append(minF1)
            elif word == words[2]:
                ymax = maxF1
    # m = abs((yt - y1) / (xt - x1))
    # x3 = y4 / m
    # x range, y range (xmin, xmax, ymin, ymax)
    coordinates = [(xmin,xmax),(min(ymin),ymax)]
    print(coordinates)
    return coordinates


def vowelChartCalibration(id):
    rootDirectory = homeDir + dataDir + id +"/vowelCalibration/"
    print(f'in directory {rootDirectory}')
    for path, dir, files in os.walk(rootDirectory):
        # path = path + '/'
        for file in files:
            if '.wav' in file:
                f1, f2 = audioToVwlFormants(path,file)
                jsonName = f"{file.split('.')[0]}-vwlCal.json"
                formantsToJson(f1,f2,path,jsonName, True)
        coordinates = vowelChartPoints(path)

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
    if 'cal' in sys.argv:
        try:
            idx = sys.argv.index('-id') + 1
            print("Calibrating vowel chart coordinates...")
            # todo: make id a sys argv
            vowelChartCalibration(sys.argv[idx])
        except ValueError:
            print("Specify the -id")
    else:
        for path, dir, files in os.walk(rootDirectory):
            path = path + '/'
            for file in files:
                if 'vowelCalibration' not in path and '.json' not in file:
                    f1, f2 = audioToVwlFormants(path,file)
                    jsonName = f'{file.split(".")[0]}.json'
                    print(jsonName)
                    formantsToJson(f1,f2,path,jsonName)
    print("--- %s milliseconds ---" % ((time.time() - start_time)*1000))