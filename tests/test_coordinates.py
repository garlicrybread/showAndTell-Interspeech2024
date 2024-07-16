from skimage.transform import ProjectiveTransform
import numpy as np
import os

from flask import (
    current_app, url_for
)

from flaskr.coordinates import (
    transformArray, vowelChartCoordinates, saveUserId
)

DATA_DIR = f'{os.getcwd()}/flaskr/static/participantData/'

''' coordinate calculation function tests'''
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

def test_vowelChartCoordinates():
    # test the basic case
    # f1List = [maxF1, minF1]
    # f2List = [maxF2, minF2]
    f1min = 300
    f1max = 800
    f2min = 400
    f2max = 3000
    diff = 10

    vowelsFH = {"f1List":[f1min,f1min-diff],"f2List":[f2max,f2max-diff]}
    vowelsBH = {"f1List":[f1min,f1min-diff],"f2List":[f2min,f2min-diff]}
    vowelsFL = {"f1List":[f1max,f1max-diff],"f2List":[f2max,f2max-diff]}
    vowelsBL = {"f1List":[f1max,f1max-diff],"f2List":[f2min,f2min-diff]}

    vowels = {
        'frontHigh': vowelsFH, 'backHigh': vowelsBH,
        'frontLow': vowelsFL, 'backLow':vowelsBL
    }
    padf = 50
    padb = 50
    FH, BH = (f2max+padf,f1min-diff-padf), (f2min-diff-padb,f1min-diff-padb)
    FL, BL = (f2max+padf,f1max+padf), (f2min-diff-padb,f1max+padb)
    calcFH, calcBH, calcFL, calcBL = vowelChartCoordinates(vowels)
    assert FH == calcFH
    assert BH == calcBH
    assert FL == calcFL
    assert BL == calcBL

def test_processCoordinateData(app,client,test_svgCoordinates):
    with app.app_context():
        id = 'testData'
        data = {'spa': False}
        t = current_app.config['TRANSFORM_FREQ_SVG']
        current_app.config.update(SVG_COORDINATES=test_svgCoordinates)
        current_app.config.update(USER_ID=id)
        assert t == None
        response = client.post(url_for('vowelCalibration.processCoordinateData'), json=data)
        assert response.status_code == 200
        t = current_app.config['TRANSFORM_FREQ_SVG']
        assert t != None
        assert type(t) == list
        assert len(t) == 3

        for line in t:
            # each line is three values long since it is a 3x3 matrix
            assert len(line) == 3
            assert type(line) == list
            assert line[0] < 10

        id = 'spaM0'
        data = {'spa': True}
        t = current_app.config['TRANSFORM_SPA']
        current_app.config.update(SVG_COORDINATES=test_svgCoordinates)
        current_app.config.update(USER_ID=id)
        response = client.post(url_for('vowelCalibration.processCoordinateData'), json=data)
        assert response.status_code == 200
        t = current_app.config['TRANSFORM_SPA']
        assert t != None
        assert type(t) == list
        assert len(t) == 3

        for line in t:
            # each line is three values long since it is a 3x3 matrix
            assert len(line) == 3
            assert type(line) == list
            assert line[0] < 10


def test_saveUserId(app, client):
    with app.app_context():
        userId = 'yoder'
        data = {'userId': userId}
        url = 'vowelCalibration.saveUserId'
        response = client.post(url_for(url),json=data)
        assert response.status_code == 200
        assert response.get_json()['saved'] == True
        assert current_app.config['USER_ID'] == userId

        userId = 'g19'
        data = {'userId': userId}
        response = client.post(url_for(url),json=data)
        assert response.status_code == 200
        assert current_app.config['USER_ID'] == userId
