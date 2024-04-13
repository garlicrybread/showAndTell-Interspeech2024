import os

import app
from flaskr.signalProcessing import (
    vowelChartPoints, transformArray, freqToSVG, formantsToJsonFormat, condenseFormantList, writeToJson, calJsonToCoordinates
)
from skimage.transform import ProjectiveTransform
import numpy as np
from flask import (current_app)
import json

DATA_DIR = f'{os.getcwd()}/flaskr/static/participantData/'

def transform(t, freq):
    xt = t[0]
    yt = t[1]
    wt = t[2]
    x = xt[0] * freq[0] + xt[1] * freq[1] + xt[2]
    y = yt[0] * freq[0] + yt[1] * freq[1] + yt[2]
    w = wt[0] * freq[0] + wt[1] * freq[1] + wt[2]
    return [x / w, y / w]

def mean(l):
    if len(l) != 0:
        return sum(l) / len(l)

def test_processVwlData():
    pass

def test_audioToVwlFormants():
    pass

def test_vowelChartPoints():
    # test the basic case
    vowelsFH = [{'vwl': [{
        "f1": 290.5,
        "f2": 2300.6
    },{
        "f1": 177.0,
        "f2": 2435.9
    }]}]

    vowelsBH = [{'vwl': [{
        "f1": 274.6,
        "f2": 746.5
    },{
        "f1": 281.4,
        "f2": 736.4
    }]}]

    vowelsFL = [{'vwl': [{
            "f1": 860.4,
            "f2": 2400.6
        },{
            "f1": 852.2,
            "f2": 2393.6
        }]}]

    vowelsBL = [{'vwl': [{
            "f1": 550.8,
            "f2": 834.3
        },{
            "f1": 553.8,
            "f2": 831.9
        }]}]
    vowels = {
        'frontHigh': vowelsFH, 'backHigh': vowelsBH,
        'frontLow': vowelsFL, 'backLow':vowelsBL
    }
    FH, BH = (2435.9,177.0), (736.4,274.6)
    FL, BL = (2400.6,860.4), (831.9,553.8)
    calcFH, calcBH, calcFL, calcBL = vowelChartPoints(vowels)
    assert FH == calcFH
    assert BH == calcBH
    assert FL == calcFL
    assert BL == calcBL

def test_transformArray(app):
    with app.app_context():
        t = ProjectiveTransform()
        actualCoordinates = [
            (2500.5, 300.5),(250.5,350.5),
            (1571.5, 850.6), (255.8, 834.3),
        ]
        # todo: determine svg's 0,0
        svgCoordinates = [
            (0,1),(1,1),
            (0,0),(1,0)
        ]
        src = np.asarray(actualCoordinates)
        dst = np.asarray(svgCoordinates)
        print(f'dst {dst}')
        if not t.estimate(src, dst): raise Exception("estimate failed")
        actualX = t.params[0]
        actualY = t.params[1]
        actualW = t.params[2]
        transformArray(actualCoordinates,svgCoordinates)
        calcT = current_app.config['TRANSFORM_FREQ_SVG']
        assert (actualX == calcT[0]).all()
        assert (actualY == calcT[1]).all()
        assert (actualW == calcT[2]).all()

def test_freqToSVG(app, test_transform):

    with app.app_context():
        # base case tests
        t = current_app.config['TRANSFORM_FREQ_SVG']
        freq = [6,9]
        actualSVG = transform(t,freq)
        calcSVG = freqToSVG(freq)
        assert type(calcSVG) == list
        assert len(calcSVG) == 2
        assert (calcSVG[0] == actualSVG[0] and calcSVG[1] == actualSVG[1])

        freq = [2500.3,210.43]
        actualSVG = transform(t,freq)
        calcSVG = freqToSVG(freq)
        assert type(calcSVG) == list
        assert len(calcSVG) == 2
        assert (calcSVG[0] == actualSVG[0] and calcSVG[1] == actualSVG[1])

def test_formantsToJsonFormat(app, test_transform):
    with app.app_context():
        t = current_app.config['TRANSFORM_FREQ_SVG']
        # one vowel test
        f1 = [390.5, 365.0]
        f2 = [1800.6, 1760.9]
        mf1 = mean(f1)
        mf2 = mean(f2)
        data = [{'vwl': [{ "f1": mf1, "f2": mf2 }] }]
        svg = transform(t,[mf1,mf2])
        dataSVG = [{'vwl': [{ 'f1': svg[0], 'f2': svg[1]}] }]
        calcData, calcDataSVG = formantsToJsonFormat(f1,f2)

        # make sure data was calculated correctly
        for idx, pair in enumerate(data[0]['vwl']):
            calcPair = calcData[0]['vwl'][idx]
            svgPair = dataSVG[0]['vwl'][idx]
            calcSvgPair = calcDataSVG[0]['vwl'][idx]
            for key in pair:
                assert calcPair[key] == pair[key]
                assert svgPair[key] == calcSvgPair[key]

        # two vowels test, two freq for the kept vowel
        f1 = [390.5, 365.0, 200, 210, 240, 250]
        f2 = [1800.6, 1760.9, 1500, 1450, 1425, 1450]
        mf1 = mean(f1[:2])
        mf2 = mean(f2[:2])
        data = [{'vwl': [{ "f1": mf1, "f2": mf2 }] }]
        svg = transform(t,[mf1,mf2])
        dataSVG = [{'vwl': [{ 'f1': svg[0], 'f2': svg[1]}] }]
        calcData, calcDataSVG = formantsToJsonFormat(f1,f2)

        # make sure data was calculated correctly
        for idx, pair in enumerate(data[0]['vwl']):
            calcPair = calcData[0]['vwl'][idx]
            svgPair = dataSVG[0]['vwl'][idx]
            calcSvgPair = calcDataSVG[0]['vwl'][idx]
            for key in pair:
                assert calcPair[key] == pair[key]
                assert svgPair[key] == calcSvgPair[key]

        # three vowels test, 5 freq for the kept vowel
        f1 = [390.5, 365.0, 400, 410, 390, 200, 210, 240, 250, 500, 510]
        f2 = [1800.6, 1760.9, 1720, 1705, 1700, 1500, 1450, 1425, 1450, 1610, 1670]
        mf1 = [mean(f1[:3]), mean(f1[3:5])]
        mf2 = [mean(f2[:3]), mean(f2[3:5])]
        data = [{'vwl': [{ "f1": mf1[0], "f2": mf2[0] }, { "f1": mf1[1], "f2": mf2[1] }] }]
        svg1 = transform(t,[mf1[0],mf2[0]])
        svg2 = transform(t,[mf1[1],mf2[1]])
        dataSVG = [{'vwl': [{ 'f1': svg1[0], 'f2': svg1[1]},{ 'f1': svg2[0], 'f2': svg2[1]}] }]
        calcData, calcDataSVG = formantsToJsonFormat(f1,f2)

        # make sure data was calculated correctly
        for idx, pair in enumerate(data[0]['vwl']):
            calcPair = calcData[0]['vwl'][idx]
            svgPair = dataSVG[0]['vwl'][idx]
            calcSvgPair = calcDataSVG[0]['vwl'][idx]
            for key in pair:
                assert calcPair[key] == pair[key]
                assert svgPair[key] == calcSvgPair[key]

def test_condenseFormantList():
    # base case test first
    f = [20,15,80,90,45,3]
    condensedActual = [mean(f[:3]),mean(f[3:])]
    condensedCalc = condenseFormantList(f)
    assert len(condensedCalc) == len(condensedActual)
    assert (condensedActual == condensedCalc)
    # check calibration
    condensedCalc = condenseFormantList(f,True)
    assert len(condensedCalc) == len(f)
    assert (condensedCalc == f)


    f = [20,15,80]
    condensedActual = [mean(f)]
    condensedCalc = condenseFormantList(f)
    assert len(condensedCalc) == len(condensedActual)
    assert (condensedActual == condensedCalc)

    # lists that are not evenly divisible by 3
    # length 5
    f = [20,15,80,90,45]
    condensedActual = [mean(f[:3]),mean(f[3:])]
    condensedCalc = condenseFormantList(f)
    assert len(condensedCalc) == len(condensedActual)
    assert (condensedActual == condensedCalc)

    # length 4
    f = [20,15,80,90]
    condensedActual = [mean(f[:3]),mean(f[3:])]
    condensedCalc = condenseFormantList(f)
    assert len(condensedCalc) == len(condensedActual)
    assert (condensedActual == condensedCalc)

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

def test_writeToJson():
    text = "I am written"
    path =  DATA_DIR + 'testData/test/'
    name = 'test.json'
    writeToJson(path,name,text)
    with open(path+name,'r') as f:
        assert f.readlines()[0] == f'"{text}"'

def test_calJsonToCoordinates():
    path = f"{DATA_DIR}testData/vowelCalibration/"
    file1 = 'testData-backHigh-vwlCal.json'
    file2 = 'testData-backLow-vwlCal.json'
    file3 = 'testData-frontHigh-vwlCal.json'
    file4 = 'testData-frontLow-vwlCal.json'
    files = [file1,file2,file3,file4]
    vowels = {}
    for file in files:
        with open(path+file,'r') as f:
            data = json.load(f)
            name,word,_ = file.split('-')
            vowels[word] = data
    aCoordinates = vowelChartPoints(vowels)
    cCoordinates = calJsonToCoordinates(path)
    assert len(aCoordinates) == len(cCoordinates)
    assert aCoordinates == cCoordinates


def test_calAudioToCoordinatesJson():
    pass


