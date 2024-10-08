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
from flaskr.autocorrelationVwlExtract import extractVwlBoundaries
import numpy as np
import statistics as stat

homeDir = f'{os.getcwd()}/'
flaskrDir = f'{os.getcwd()}/flaskr/'
dataDir = 'static/participantData/'
bp = Blueprint('signalProcessing', __name__, url_prefix='/signalProcessing')

@bp.route('/api/processVwlData', methods=["POST"])
def processVwlData():
    data = request.get_json()
    filePath = data['filePath']
    cal = data['cal']
    pathList = filePath.split('/')
    path = '/'.join(pathList[:len(pathList)-1]) + '/'
    filename = pathList[-1]
    if cal:
        f1List, f2List = calAudioToVwl(path, filename)
        jsonName = filename.split('.')[0] + '-vwlCal.json'
        data = {"f1List":f1List,"f2List":f2List}
        if f1List == ['OtT']:
            return jsonify({'data': ['OvertheThresh', 'OvertheThresh']})
    else:
        f1List, f2List = audioToVwlFormants(path,filename)
        jsonName = filename.split('.')[0] + '.json'
        data = formantsToJsonFormat(f1List,f2List)
    if data == [] or f1List == []:
        # unable to extract formants, probably didn't pick up voices but loud sounds instead
        return jsonify({'data': ['empty','empty']})
    print('------')
    print(filename)
    print(f"processVwlData")
    print('------\n')

    writeToJson(path,jsonName,data)
    id, word, _ = jsonName.split('-')
    print(f'cal {cal,word,jsonName}')
    if cal:
        locations = ['frontHigh', 'backHigh', 'frontLow', 'backLow']
        relPath = f'../../static/participantData/{id}/vowelCalibration/{jsonName}'
    else:
        locations = [word]
        relPath = f'../../static/participantData/{id}/{word}/{jsonName}'
    location = locations.index(word)
    data = {'data': [relPath,str(location)]}
    return jsonify(data)

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
    freq = request.get_json()['freq']
    spa = request.get_json()['spa']
    tut = request.get_json()['tut']
    print('in freq to svg, spa ', spa)
    tempList = [[freq['f2']],[freq['f1']],[1]]
    freq = np.array(tempList)
    # t is a 3x3
    print()
    if spa:
        print('using spa transform')
        t = np.array(current_app.config['TRANSFORM_SPA'])
    elif tut:
        t = np.array(current_app.config['TRANSFORM_TUTORIAL'])
    else:
        t = np.array(current_app.config['TRANSFORM_FREQ_SVG'])
    print('t ', t, 'freq ', freq, 'tut ', tut)
    x,y,w = np.dot(t,freq).tolist()
    w = sum(w)
    x = sum(x)/w
    y = sum(y)/w

    fh, bh, fl, bl = current_app.config['SVG_COORDINATES']
    if y < bh[1]:
        y = bh[1]
    elif y > bl[1]: y = bl[1]

    leftBoundaryX = yToX(y)
    if x < leftBoundaryX: x = leftBoundaryX
    elif x > bh[0]: x = bh[0]

    data = {'svg': [x,y]}
    return jsonify(data)

@bp.route('/api/svgToConfig',methods=['POST'])
def svgToConfig():
    svg = request.get_json()
    current_app.config.update(SVG_COORDINATES=svg)
    return jsonify({'success':True})

@bp.route('/api/getSvgCoordinates',methods=['GET'])
def getSvgCoordinates():
    coordinates = current_app.config['SVG_COORDINATES']
    return jsonify({'coordinates':coordinates})

def mean(l):
    if len(l) != 0:
        return sum(l) / len(l)

def split_and_find_medians(numbers):
    # Sort the list
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)

    # Determine the split point
    mid = (n + 1) // 2  # Bottom half takes the extra element if odd

    # Split the list
    bottom_half = sorted_numbers[:mid]
    top_half = sorted_numbers[mid:]

    # Calculate the medians
    bottom_median = stat.median(bottom_half)
    top_median = stat.median(top_half)

    return bottom_median, top_median


def calAudioToVwl(path, file_name):
    id, word = file_name.split('-')
    word = word.replace('.wav','')
    f1List, f2List = audioToVwlFormants(path, file_name)
    if len(f1List) == 0:
        return [], []
    words = ['frontHigh','backHigh','frontLow', 'backLow']
    minF1, maxF1 = split_and_find_medians(f1List)
    minF2, maxF2 = split_and_find_medians(f2List)
    f1List = [maxF1, minF1]
    f2List = [maxF2, minF2]

    return f1List, f2List

def maxAndMinOfFormants(f1List, f2List):
    maxF1 = max(f1List)
    minF1 = min(f1List)
    maxF2 = max(f2List)
    minF2 = min(f2List)
    return maxF1, maxF2, minF1, minF2

def metricFmt(fmtList,alpha=0.8,linear=0):
    lenfmt = len(fmtList)
    for i in range(lenfmt):
        fmtList[i] = [x for x in fmtList[i] if x > 0]
    mtr = np.std(fmtList[0])
    # mtr +=  np.std(fmtList[1])
    count = 2
    if linear == 1:
        for i in range(2,lenfmt):
            if fmtList[i] != []:
                mtr += alpha*np.std(fmtList[i])
                count += alpha
    else:
        for i in range(1,lenfmt):
            if fmtList[i] != []:
                mtr += pow(alpha,i) * np.std(fmtList[i])
                count += pow(alpha,i)
    mtr = mtr/count
    return mtr

def analyzeformants(vowels,pointProcess):
    time_step = 0.0  # if time step = 0.0 (the standard), Praat will set it to 25% of the analysis window length
    formant_ceiling = 5500
    # higher window length to deal with smoothing
    window_len = 0.025
    preemphasis = 100

    # num_formants = 5

    ## Looping through the formant count
    f_list_dict = {}
    bestMetric = 9223372036854775807 ## sys.maxsize
    f1_list = []
    f2_list = []
    bestFmt = 0
    for num_formants in range(4,7):
        formants = praat.call(vowels, "To Formant (burg)", time_step, num_formants, formant_ceiling, window_len,
                            preemphasis)
                
        numPoints = praat.call(pointProcess, "Get number of points")

        ## Creating a list of list of for each formant
        f_list_dict[num_formants] = [ [] for _ in range(num_formants) ]
        

        for point in range(0, numPoints):
            point += 1
            f_local = [ 0 for _ in range(num_formants)]
            t = praat.call(pointProcess, "Get time from index", point)
            for fmt in range(num_formants):
                f_local[fmt] = praat.call(formants, "Get value at time", fmt+1, t, 'Hertz', 'Linear')
                # print(fmt,f_local[fmt])
            # f1 = praat.call(formants, "Get value at time", 1, t, 'Hertz', 'Linear')
            # f2 = praat.call(formants, "Get value at time", 2, t, 'Hertz', 'Linear')
            for fmt in range(num_formants):
                # filter out "nan"
                f_list_dict[num_formants][fmt].append(f_local[fmt])
                # f2_list.append(f2)
        print(num_formants,f_list_dict[num_formants])
        metricVal = metricFmt(f_list_dict[num_formants],0.5)
        if metricVal < bestMetric:
            bestMetric = metricVal
            bestFmt = num_formants
            f1_list = f_list_dict[num_formants][0]
            f2_list = f_list_dict[num_formants][1]
    #### At this point we should have the formants and their values. Now analyze the values
    # Analyze and then return the list of the two formants
    print('---')
    print(f'best formant {bestFmt}')
    print('---')
    return f1_list,f2_list,bestFmt

def audioToVwlFormants(path,file_name, cal=False):
    # vocalToolKitDir = '~/plugin_VocalToolkit/'
    vocalToolKitDir = flaskrDir+"plugin_VocalToolkit/"
    extractVwlFile = "extractvowelsNoViewAndEdit.praat"
    file = path + file_name
    # read the wav file and get the samplerate and data

    justVwlFile, timeStamps = extractVwlBoundaries(file)
    vwlSound = parselmouth.Sound(justVwlFile)
    f0min = 75
    f0max = 600
    # extract vowels
    try:
        pointProcess = praat.call(vwlSound, "To PointProcess (periodic, cc)", f0min, f0max)
    except parselmouth.PraatError as error:
        print(error)
        return [],[]
    # source: https://www.fon.hum.uva.nl/praat/manual/Sound__To_Formant__burg____.html

    f1_list,f2_list,fmtNum = analyzeformants(vwlSound,pointProcess)
    print(fmtNum,f1_list,f2_list)
    return f1_list, f2_list

def condenseFormantList(formantList):
    # condenses the formant list / smooths it out
    length = len(formantList)
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

def formantsToJsonFormat(f1List,f2List):
    # condense the formant lists and write to json format
    vwlsDict = {"vwl": []}
    data = []
    print('f1list', f1List)
    idx = len(f1List) + 1
    for i in range(1,len(f1List)):
        diff = 250
        if abs(f1List[i] - f1List[i-1]) > diff or abs(f2List[i] - f2List[i-1]) > diff:
            idx = i
            break
    f1List = condenseFormantList(f1List[:idx])
    f2List = condenseFormantList(f2List[:idx])

    for vwl_idx in range(len(f1List)):
        f1_vwl = f1List[vwl_idx]
        f2_vwl = f2List[vwl_idx]
        tempDict = {"f1": f1_vwl, "f2": f2_vwl}
        vwlsDict["vwl"].append(tempDict)

    if vwlsDict['vwl'] != []:
        data.append(vwlsDict)

    # Serializing json
    print('data', data)
    return data

def writeToJson(path, jsonName, data):
    # Serializing json
    json_object= json.dumps(data, indent=4)
    # Writing to json
    with open(path+jsonName, "w") as outfile:
        outfile.write(json_object)



if __name__ == '__main__': # pragma: no cover
    start_time = time.time()
    # hardcoded for now
    rootDirectory = flaskrDir + dataDir
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