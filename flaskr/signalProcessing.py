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


homeDir = f'{os.getcwd()}/'
dataDir = 'flaskr/participantData/'

def audioToVwlFormants(path,file_name):
    vocalToolKitDir = '~/plugin_VocalToolkit/'
    extractVwlFile = "extractvowels.praat"
    file = path + file_name
    print(file)
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

    print(f"f1 list: {f1_list}, \nf2 list: {f2_list}")
    return f1_list, f2_list


def formantsToJson(f1List,f2List,path,jsonName):
    idx_vwls = [0]
    for prev_idx, vwlF1 in enumerate(f1List[1:]):
        prevVwlF1 = f1List[prev_idx]
        prevVwlF2 = f2List[prev_idx]
        vwlF2 = f2List[prev_idx + 1]
        absDiffF1 = abs(vwlF1 - prevVwlF1)
        absDiffF2 = abs(vwlF2 - prevVwlF2)
        # print(prev_idx+1,vwlF1,vwlF2)
        diff = 150
        if absDiffF1 >= diff and absDiffF2 >= diff:
            idx_vwls.append(prev_idx + 1)
    idx_vwls.append(len(f1List) - 1)
    # print(idx_vwls)
    # print(f2_list[20])
    data = []
    # go through the index list
    prev_idx = 0
    for i, idx in enumerate(idx_vwls[1:]):
        vwlsDict = {"vwl": []}
        print(prev_idx, idx)
        for vwl_idx in range(prev_idx, idx):
            # print(f1_list[idx],f2_list[idx])
            f1_vwl = f1List[vwl_idx]
            f2_vwl = f2List[vwl_idx]
            tempDict = {"f1": f1_vwl, "f2": f2_vwl}
            vwlsDict["vwl"].append(tempDict)
        data.append(vwlsDict)
        prev_idx = idx_vwls[i + 1]

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
    print(type(data))
    for formants in data['vwl']:
        # See if the f1 formant is greater than the current max
        # or if it is less than the current min
        print(formants)
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
    '''hardcoded for beet, bat, bot, and bow'''

    vowels = {}
    for path, dir, files in os.walk(rootDirectory):
        for file in files:
            if '.json' in file and 'Coordinates' not in file:
                with open(path+file,'r') as f:
                    data = json.load(f)
                    name,word,date,_ =file.split('-')
                    vowels[word] = data
    # json data in the form of list(dictionary
    pprint(vowels)
    edges = {}
    words = ['beet','bot','bow','bat']
    for word, vwls in vowels.items():
        print(f"Processing {word, vwls}")
        for vwl in vwls:
            maxF1, maxF2, minF1, minF2 = maxAndMinOfFormants(vwl)
            if word == words[0]:
                x1, y1 = maxF2, minF1
            elif word == words[1]:
                x2 = minF1
            elif word == words[2]:
                y4 = maxF1
            elif word == words[3]:
                xt, yt = maxF2, maxF1
    m = abs((yt - y1) / (xt - x1))
    x3 = y4 / m
    # top: left corner, right corner, bottom: left corner, right corner
    coordinates = [(x1,y1),(x2,y1),(x3,y4),(x2,y4)]
    return coordinates


def vowelChartCalibration(id):
    rootDirectory = homeDir + dataDir + id +"/vowelCalibration/"
    for path, dir, files in os.walk(rootDirectory):
        # path = path + '/'
        for file in files:
            if '.wav' in file:
                # f1, f2 = audioToVwlFormants(path,file)
                jsonName = f"{file.split('.')[0]}-vwlCal.json"
                # formantsToJson(f1,f2,path,jsonName)
        coordinates = vowelChartPoints(path)

        # Serializing json
        json_object = json.dumps(coordinates, indent=4)

        # Writing to sample.json
        jsonName = "vwlChartCoordinates.json"
        print(path + jsonName)
        with open(path + jsonName, "w") as outfile:
            outfile.write(json_object)




if __name__ == '__main__':
    start_time = time.time()
    # hardcoded for now
    path = homeDir + dataDir + 'cry/tardo/'
    file = 'cry-tardo-2023_05_02_155250.wav'
    jsonName = f"{file.split('.')[0]}-vwl.json"
    if 'cal' in sys.argv:
        vowelChartCalibration('yoder')
    else:
        f1, f2 = audioToVwlFormants(path,file)
        formantsToJson(f1,f2,path,jsonName)
    print("--- %s milliseconds ---" % ((time.time() - start_time)*1000))