import os

import app
from flaskr.signalProcessing import (
    freqToSVG, formantsToJsonFormat, condenseFormantList, writeToJson,
)
from flask import (current_app, url_for)
import json

DATA_DIR = f'{os.getcwd()}/flaskr/static/participantData/'


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
        mf1 = mean(f1)
        mf2 = mean(f2)
        data = [{'vwl': [{ "f1": mf1, "f2": mf2 }] }]
        calcdata = formantsToJsonFormat(f1,f2)

        # make sure data was calculated correctly
        for idx, pair in enumerate(data[0]['vwl']):
            calcpair = calcdata[0]['vwl'][idx]
            for key in pair:
                assert calcpair[key] == pair[key]

        # two vowels test, should be seen as one
        f1 = [390.5, 365.0, 150, 210, 240, 250]
        f2 = [1800.6, 1760.9, 1500, 1450, 1425, 1450]
        mf1 = condenseFormantList(f1)
        mf2 = condenseFormantList(f2)
        data = [{'vwl': [{"f1": mf1[0], "f2": mf2[0]},
                         {"f1": mf1[1], 'f2': mf2[1]},
                         {"f1": mf1[2], 'f2': mf2[2]}
                         ]
        }]
        calcdata = formantsToJsonFormat(f1,f2)

        # make sure data was calculated correctly
        for idx, pair in enumerate(data[0]['vwl']):
            calcpair = calcdata[0]['vwl'][idx]
            for key in pair:
                assert calcpair[key] == pair[key]

        # two vowels test - cal
        f1 = [390.5, 365.0, 150]
        f2 = [1800.6, 1760.9, 1500]
        data = [{'vwl': [{"f1": f1[0], "f2": f2[0]},
                         {"f1": f1[1], 'f2': f2[1]},
                         {"f1": f1[2], 'f2': f2[2]}
                         ]
                 }]
        calcdata = formantsToJsonFormat(f1,f2,True)

        # make sure data was calculated correctly
        for idx, pair in enumerate(data[0]['vwl']):
            calcpair = calcdata[0]['vwl'][idx]
            for key in pair:
                assert calcpair[key] == pair[key]

        # three "vowels" test
        f1 = [390.5, 365.0, 400, 410, 390, 180, 210, 240, 250, 500]
        f2 = [1800.6, 1760.9, 1720, 1705, 1700, 1400, 1450, 1425, 1450, 1610]
        mf1 = condenseFormantList(f1)
        mf2 = condenseFormantList(f2)
        data = [{'vwl': [{"f1": mf1[0], "f2": mf2[0] },
                         {"f1": mf1[1], "f2": mf2[1] },
                         {"f1": mf1[2], "f2": mf2[2] },
                         {"f1": mf1[3], "f2": mf2[3]},
                         {"f1": mf1[4], "f2": mf2[4]}]

        }]
        calcdata = formantsToJsonFormat(f1,f2)

        # make sure data was calculated correctly
        for idx, pair in enumerate(data[0]['vwl']):
            calcpair = calcdata[0]['vwl'][idx]
            for key in pair:
                assert calcpair[key] == pair[key]

# TODO: record more test data files
# def test_audioToVwlFormants(app,client):
#     id = 'testData'
#     filename1 = 'testData-bag-2024_04_03_110633'
#     filename2 = 'testData-bag-2024_04_10_102243'
#     path1 = DATA_DIR + f'{id}/bag/{filename1}.wav'
#     path2 = DATA_DIR + f'{id}/bag/{filename2}.wav'
#     data = {'gotAudio': path1}
#     data2 = {'gotAudio': path2}
#     with app.app_context():
#         response = client.post(url_for('signalProcessing.processVwlData'), json=data)
#         assert response.status_code == 200
#         relPath = response.data.decode('utf-8')
#         assert relPath == f'../../static/participantData/{id}/bag/{filename1}.json'
#
#         # check for another file to be sure
#         response = client.post(url_for('signalProcessing.processVwlData'), json=data2)
#         assert response.status_code == 200
#         relPath = response.data.decode('utf-8')
#         assert relPath == f'../../static/participantData/{id}/bag/{filename2}.json'

def test_writeToJson():
    text = "I am written"
    path =  DATA_DIR + 'testData/test/'
    name = 'test.json'
    writeToJson(path,name,text)
    with open(path+name,'r') as f:
        assert f.readlines()[0] == f'"{text}"'

def transform(t, freq):
    xt = t[0]
    yt = t[1]
    wt = t[2]
    x = xt[0] * freq[0] + xt[1] * freq[1] + xt[2]
    y = yt[0] * freq[0] + yt[1] * freq[1] + yt[2]
    w = wt[0] * freq[0] + wt[1] * freq[1] + wt[2]
    return [x / w, y / w]

def test_freqToSVG(app, test_transform, client, test_svgCoordinates):

    with app.app_context():
        # base case tests
        t = current_app.config['TRANSFORM_FREQ_SVG']
        svgCoordinates = test_svgCoordinates
        current_app.config.update(SVG_COORDINATES=svgCoordinates)
        freq = [1400,400]
        actualSVG = transform(t,freq)
        url = 'signalProcessing.freqToSVG'
        data = {'freq':{'f1':freq[1],'f2':freq[0]},'spa':False}
        response = client.post(url_for(url), data=json.dumps(data), content_type='application/json')

        # Assert that the response status code is 200 (success)
        assert response.status_code == 200

        # Check if the JSON response indicates success
        calcSVG = response.json['svg']
        assert type(calcSVG) == list
        assert len(calcSVG) == 2
        assert (calcSVG[0] == actualSVG[0] and calcSVG[1] == actualSVG[1])

        # outside the y boundary
        freq = [2500.3,210.43]
        actualSVG = transform(t,freq)
        data = {'freq':{'f1': freq[1], 'f2': freq[0]},'spa':False}
        response = client.post(url_for(url), data=json.dumps(data), content_type='application/json')
        calcSVG = response.json['svg']
        assert type(calcSVG) == list
        assert len(calcSVG) == 2
        assert (calcSVG[0] == actualSVG[0] and calcSVG[1] == test_svgCoordinates[1][1])

