from skimage.transform import ProjectiveTransform
import numpy as np
import os

from flask import (
    current_app, url_for
)

from flaskr.coordinates import (
    transformArray, vowelChartCoordinates
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
    calcFH, calcBH, calcFL, calcBL = vowelChartCoordinates(vowels)
    assert FH == calcFH
    assert BH == calcBH
    assert FL == calcFL
    assert BL == calcBL

def test_processCoordinateData(app,client):
    id = 'testData'
    path = DATA_DIR + f'{id}/vowelCalibration/'
    data = {'gotAudio': path}
    with app.app_context():
        t = current_app.config['TRANSFORM_FREQ_SVG']
        svgCoordinates = [(200,0),(0,0),(0,100),(150,100)]
        current_app.config.update(SVG_COORDINATES=svgCoordinates)
        assert t == None
        response = client.post(url_for('coordinates.processCoordinateData'), json=data)
        assert response.status_code == 200
        t = current_app.config['TRANSFORM_FREQ_SVG']
        assert t != None
        assert type(t) == list
        assert len(t) == 3

        for line in t:
            # each line is three values long since it is a 3x3 matrix
            assert len(line) == 3
            assert type(line) == list


