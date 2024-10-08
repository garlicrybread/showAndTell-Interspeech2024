import os

import numpy as np

import app
from flaskr.signalProcessing import (
    freqToSVG, formantsToJsonFormat, condenseFormantList, writeToJson,
    audioToVwlFormants, maxAndMinOfFormants, calAudioToVwl, analyzeformants,
    metricFmt, split_and_find_medians
)
from flask import (current_app, url_for)
import json
import parselmouth
from parselmouth import praat

DATA_DIR = f'{os.getcwd()}/flaskr/static/participantData/'
flaskrDir = f'{os.getcwd()}/flaskr/'


def test_processVwlData(app,client):
    # DATA_DIR = f'{os.getcwd()}/flaskr/static/participantData/'
    id = 'testData'
    word1 = 'audio'
    filename1 = f'{id}-{word1}-0000'
    path1 = DATA_DIR + f'{id}/{word1}/{filename1}.wav'
    data = {'filePath': path1, 'cal': False}

    # second file to test
    word2 = 'aaudiioo'
    filename2 = f'{id}-{word2}-0000'
    path2 = DATA_DIR + f'{id}/{word2}/{filename2}.wav'
    data2 = {'filePath': path2, 'cal': False}

    # third file to test
    word3 = 'crudo'
    filename3 = f'{id}-{word3}-0000'
    path3 = DATA_DIR + f'{id}/{word3}/{filename3}.wav'
    data3 = {'filePath': path3, 'cal': False}

    # calibration files to test
    word4 = 'frontHigh'
    id1 = 'testData'
    filename4 = f'{id1}-{word4}'
    path4 = DATA_DIR + f'{id1}/vowelCalibration/{filename4}.wav'
    data4 = {'filePath': path4, 'cal': True}

    word5 = 'backHigh'
    filename5 = f'{id1}-{word5}'
    path5 = DATA_DIR + f'{id1}/vowelCalibration/{filename5}.wav'
    data5 = {'filePath': path5, 'cal': True}

    word6 = 'frontLow'
    filename6 = f'{id1}-{word6}'
    path6 = DATA_DIR + f'{id1}/vowelCalibration/{filename6}.wav'
    data6 = {'filePath': path6, 'cal': True}

    word7 = 'backLow'
    filename7 = f'{id1}-{word7}'
    path7 = DATA_DIR + f'{id1}/vowelCalibration/{filename7}.wav'
    data7 = {'filePath': path7, 'cal': True}

    with app.app_context():
        response = client.post(url_for('signalProcessing.processVwlData'), json=data)
        assert response.status_code == 200
        relPath = response.get_json()
        path, location = relPath['data']
        assert path == f'../../static/participantData/{id}/{word1}/{filename1}.json'

        # check for another file to be sure
        response = client.post(url_for('signalProcessing.processVwlData'), json=data2)
        assert response.status_code == 200
        relPath = response.get_json()
        path, location = relPath['data']
        assert path == f'../../static/participantData/{id}/{word2}/{filename2}.json'

        # test edge case of consonant classified as first vowel
        response = client.post(url_for('signalProcessing.processVwlData'), json=data3)
        assert response.status_code == 200
        relPath = response.get_json()
        path, location = relPath['data']
        assert path == f'../../static/participantData/{id}/{word3}/{filename3}.json'

        # test case of vowel calibration FrontHigh
        response = client.post(url_for('signalProcessing.processVwlData'), json=data4)
        assert response.status_code == 200
        relPath = response.get_json()
        path, location = relPath['data']
        assert location == '0'
        assert path == f'../../static/participantData/{id1}/vowelCalibration/{filename4}-vwlCal.json'

        # test case of vowel calibration backHigh
        response = client.post(url_for('signalProcessing.processVwlData'), json=data5)
        assert response.status_code == 200
        relPath = response.get_json()
        path, location = relPath['data']
        assert location == '1'
        assert path == f'../../static/participantData/{id1}/vowelCalibration/{filename5}-vwlCal.json'

        # test case of vowel calibration frontLow
        response = client.post(url_for('signalProcessing.processVwlData'), json=data6)
        assert response.status_code == 200
        relPath = response.get_json()
        path, location = relPath['data']
        assert location == '2'
        assert path == f'../../static/participantData/{id1}/vowelCalibration/{filename6}-vwlCal.json'

        # test case of vowel calibration backLow
        response = client.post(url_for('signalProcessing.processVwlData'), json=data7)
        assert response.status_code == 200
        relPath = response.get_json()
        path, location = relPath['data']
        assert location == '3'
        assert path == f'../../static/participantData/{id1}/vowelCalibration/{filename7}-vwlCal.json'


def mean(l):
    if len(l) != 0:
        return sum(l) / len(l)

def test_condenseFormantList():
    # base case test first
    f = [20,15,80,90,45,3]
    condensedActual = [mean(f[:2]),mean(f[2:4]),mean(f[4:])]
    condensedCalc = condenseFormantList(f)
    assert len(condensedCalc) == len(condensedActual)
    assert (condensedActual == condensedCalc)


    f = [20,15,80]
    condensedActual = [mean(f[:2]),f[2]]
    condensedCalc = condenseFormantList(f)
    assert len(condensedCalc) == len(condensedActual)
    assert (condensedActual == condensedCalc)

    # lists that are not evenly divisible by 2
    # length 5
    f = [20,15,80,90,45]
    condensedActual = [mean(f[:2]),mean(f[2:4]),f[4]]
    condensedCalc = condenseFormantList(f)
    assert len(condensedCalc) == len(condensedActual)
    assert (condensedActual == condensedCalc)

    # # length 4
    # f = [20,15,80,90]
    # condensedActual = [mean(f[:3]),mean(f[3:])]
    # condensedCalc = condenseFormantList(f)
    # assert len(condensedCalc) == len(condensedActual)
    # assert (condensedActual == condensedCalc)

    # length 2
    f = [20,15]
    condensedActual = [mean(f)]
    condensedCalc = condenseFormantList(f)
    assert len(condensedCalc) == len(condensedActual)
    assert (condensedActual == condensedCalc)

    # length 1
    f = [20]
    condensedActual = [mean(f)]
    condensedCalc = condenseFormantList(f)
    assert len(condensedCalc) == len(condensedActual)
    assert (condensedActual == condensedCalc)

def test_formantsToJsonFormat(app, test_transform):
    with app.app_context():
        # one vowel test
        f1 = [390.5, 365.0]
        f2 = [1800.6, 1760.9]
        mf1 = condenseFormantList(f1)
        mf2 = condenseFormantList(f2)
        data = [{'vwl': [{ "f1": mf1[0], "f2": mf2[0] }] }]
        calcdata = formantsToJsonFormat(f1,f2)

        # make sure data was saved correctly
        # data = [{'vwl': [{ "f1": mf1, "f2": mf2 }] }]
        assert type(data) == list
        assert type(data[0]) == dict

        for idx, pair in enumerate(data[0]['vwl']):
            calcpair = calcdata[0]['vwl'][idx]
            for key in pair:
                assert calcpair[key] == pair[key]

        # testing f1 out of range, f2 fine
        f1 = [500,550,650,1500]
        f2 = [400,400,400,400]
        mf1 = condenseFormantList(f1[:3])
        mf2 = condenseFormantList(f2[:3])
        data = [{'vwl': [{"f1": mf1[0], "f2": mf2[0]},
                         {"f1": mf1[1], 'f2': mf2[1]}
                         ]
        }]
        calcdata = formantsToJsonFormat(f1,f2)

        # make sure data was calculated correctly
        for idx, pair in enumerate(data[0]['vwl']):
            calcpair = calcdata[0]['vwl'][idx]
            for key in pair:
                assert calcpair[key] == pair[key]

        # testing f2 out of range, f1 fine
        f1 = [500,500,500,500,500,500]
        f2 = [2000,1900,1950,1850,1300,1400]
        mf1 = condenseFormantList(f1[:5])
        mf2 = condenseFormantList(f2[:5])
        data = [{'vwl': [{"f1": mf1[0], "f2": mf2[0] },
                         {"f1": mf1[1], "f2": mf2[1] }]
        }]
        calcdata = formantsToJsonFormat(f1,f2)

        # make sure data was calculated correctly
        for idx, pair in enumerate(data[0]['vwl']):
            calcpair = calcdata[0]['vwl'][idx]
            for key in pair:
                assert calcpair[key] == pair[key]

def test_audioToVwlFormants(app,client):
    # DATA_DIR = f'{os.getcwd()}/flaskr/static/participantData/'
    id = 'testData_misc'
    word = 'audio'
    filename1 = f'{id}-{word}-0000.wav'
    path1 = DATA_DIR + f'{id}/{word}/'
    data = {'gotAudio': path1}

    # second file to test
    word = 'aaudiioo'
    filename2 = f'{id}-{word}-0000.wav'
    path2 = DATA_DIR + f'{id}/{word}/'
    data2 = {'gotAudio': path2}

    # second file to test
    word = 'crudo'
    filename3 = f'{id}-{word}-0000.wav'
    path3 = DATA_DIR + f'{id}/{word}/'
    data3 = {'gotAudio': path3}
    with app.app_context():
        actualf1List, actualf2List = audioToVwlFormants(path1,filename1)
        assert len(actualf1List) == len(actualf2List)
        assert len(actualf1List) != 0
        # assert len(actualf1List) == 10
        #
        # actualf1List, actualf2List = audioToVwlFormants(path2,filename2)
        # assert len(actualf1List) == len(actualf2List)
        # assert len(actualf1List) != 0
        # assert len(actualf1List) == 42
        #
        # actualf1List, actualf2List = audioToVwlFormants(path3,filename3)
        # assert len(actualf1List) == len(actualf2List)
        # assert len(actualf1List) != 0
        # assert len(actualf1List) == 6

# def test_writeToJson():
#     text = "I am written"
#     path =  DATA_DIR + 'testData/test/'
#     name = 'test.json'
#     writeToJson(path,name,text)
#     with open(path+name,'r') as f:
#         assert f.readlines()[0] == f'"{text}"'

def transform(t, freq):
    xt = t[0]
    yt = t[1]
    wt = t[2]
    x = xt[0] * freq[0] + xt[1] * freq[1] + xt[2]
    y = yt[0] * freq[0] + yt[1] * freq[1] + yt[2]
    w = wt[0] * freq[0] + wt[1] * freq[1] + wt[2]
    return [x / w, y / w]

# def test_freqToSVG(app, test_transform, client, test_svgCoordinates):
#
#     with app.app_context():
#         # base case tests
#         t = current_app.config['TRANSFORM_FREQ_SVG']
#         svgCoordinates = test_svgCoordinates
#         current_app.config.update(SVG_COORDINATES=svgCoordinates)
#         freq = [1400,400]
#         actualSVG = transform(t,freq)
#         url = 'signalProcessing.freqToSVG'
#         data = {'freq':{'f1':freq[1],'f2':freq[0]},'spa':False}
#         response = client.post(url_for(url), data=json.dumps(data), content_type='application/json')
#
#         # Assert that the response status code is 200 (success)
#         assert response.status_code == 200
#
#         # Check if the JSON response indicates success
#         calcSVG = response.json['svg']
#         assert type(calcSVG) == list
#         assert len(calcSVG) == 2
#         assert (calcSVG[0] == actualSVG[0] and calcSVG[1] == actualSVG[1])
#
#         # outside the y boundary
#         freq = [2500.3,210.43]
#         actualSVG = transform(t,freq)
#         data = {'freq':{'f1': freq[1], 'f2': freq[0]},'spa':False}
#         response = client.post(url_for(url), data=json.dumps(data), content_type='application/json')
#         calcSVG = response.json['svg']
#         assert type(calcSVG) == list
#         assert len(calcSVG) == 2
#         assert (calcSVG[0] == actualSVG[0] and calcSVG[1] == test_svgCoordinates[1][1])

def test_calAudioToVwl():
    id = 'testData_misc'
    # calibration files to test
    # word = 'frontHigh'
    # filename = f'{id}-{word}.wav'
    # path1 = DATA_DIR + f'{id}/vowelCalibration/'
    # f1List, f2List = calAudioToVwl(path1,filename)
    # assert len(f1List) == len(f2List)
    # assert len(f1List) == 2
    #
    # word = 'backHigh'
    # filename = f'{id}-{word}.wav'
    # path = DATA_DIR + f'{id}/vowelCalibration/'
    # f1List, f2List = calAudioToVwl(path,filename)
    # assert len(f1List) == len(f2List)
    # assert len(f1List) == 2
    #
    # # test out of bound trigger
    # word = 'frontHigh'
    # filename = f'{id}-{word}.wav'
    # path = DATA_DIR + f'{id}/vowelCalibration_false/'
    # f1List, f2List = calAudioToVwl(path,filename)
    # assert len(f1List) == len(f2List)
    # assert f1List == ['OtT']
    #
    # word = 'backHigh'
    # filename = f'{id}-{word}.wav'
    # path = DATA_DIR + f'{id}/vowelCalibration_false/'
    # f1List, f2List = calAudioToVwl(path,filename)
    # assert len(f1List) == len(f2List)
    # assert f1List == ['OtT']
    #
    # word = 'frontLow'
    # filename = f'{id}-{word}.wav'
    # path = DATA_DIR + f'{id}/vowelCalibration_false/'
    # f1List, f2List = calAudioToVwl(path,filename)
    # assert len(f1List) == len(f2List)
    # assert f1List == ['OtT']

    # word = 'backLow'
    # filename = f'{id}-{word}.wav'
    # path = DATA_DIR + f'{id}/vowelCalibration_false/'
    # f1List, f2List = calAudioToVwl(path, filename)
    # assert len(f1List) == len(f2List)
    # assert f1List == ['OtT']
    #
    # # empty audio file to test fail case
    # word1 = 'snaps'
    # filename1 = f'{id}-{word1}.wav'
    # f1List, f2List = calAudioToVwl(path1,filename1)
    # assert len(f1List) == len(f2List)
    # assert len(f1List) == 0

def test_maxAndMinOfFormants():
    # test getting max and Min of formants basic
    f1List = [1,10,20]
    f2List = [200,100,2]
    actualMaxF1,actualMaxF2,actualMinF1,actualMinF2 = 20,200,1,2
    maxF1,maxF2,minF1,minF2 = maxAndMinOfFormants(f1List,f2List)
    assert actualMaxF1 == maxF1
    assert actualMaxF2 == maxF2
    assert actualMinF1 == minF1
    assert actualMinF2 == minF2

def test_analyzeformants():
    vocalToolKitDir = flaskrDir+"plugin_VocalToolkit/"
    extractVwlFile = "extractvowelsNoViewAndEdit.praat"

    # tiffany files test
    # frontHigh
    path = DATA_DIR + 'testData_tiffany/vowelCalibration/'
    file = path + 'testData_tiffany-frontHigh.wav'
    sound = parselmouth.Sound(file)
    vowels, grid = praat.run_file(sound, vocalToolKitDir + extractVwlFile,1,0)
    f0min = 75
    f0max = 600
    # extract vowels
    pointProcess = praat.call(vowels, "To PointProcess (periodic, cc)", f0min, f0max)
    f1, f2, bestFmt = analyzeformants(vowels, pointProcess)
    assert bestFmt == 4

    # backHigh
    # path = DATA_DIR + 'testData_tiffany/vowelCalibration/'
    # file = path + 'testData_tiffany-backHigh.wav'
    # sound = parselmouth.Sound(file)
    # vowels, grid = praat.run_file(sound, vocalToolKitDir + extractVwlFile,1,0)
    # f0min = 75
    # f0max = 600
    # # extract vowels
    # pointProcess = praat.call(vowels, "To PointProcess (periodic, cc)", f0min, f0max)
    # f1, f2, bestFmt = analyzeformants(vowels, pointProcess)
    # # doesn't currently work, but I think that's because we aren't using autocorrelation to target the vowels
    # assert bestFmt == 5
    #
    # id = 'testData_misc'
    # word = 'backHigh'
    # filename = f'{id}-{word}.wav'
    # path = DATA_DIR + f'{id}/vowelCalibration/'
    # sound = parselmouth.Sound(path+filename)
    # vowels, grid = praat.run_file(sound, vocalToolKitDir + extractVwlFile,1,0)
    # f0min = 75
    # f0max = 600
    # # extract vowels
    # pointProcess = praat.call(vowels, "To PointProcess (periodic, cc)", f0min, f0max)
    # f1, f2, bestFmt = analyzeformants(vowels, pointProcess)
    # assert bestFmt == 4

def test_metricFmt():
    fmtList = [[1, 2,4],[1,2,4],[1,2,4],[1,np.nan,np.nan]]
    mtr = metricFmt(fmtList)
    assert not np.isnan(mtr)

def test_splitAndFindMedians():
    f1 = [1,1,2,5,5]
    min, max = split_and_find_medians(f1)
    assert min == 1 and max == 5

    f = [6,3,6,6]
    min, max = split_and_find_medians(f)
    assert min == 4.5 and max == 6
