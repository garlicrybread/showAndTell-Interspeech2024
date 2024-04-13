import os

import app
from flaskr.signalProcessing import (
    vowelChartPoints, transformArray, freqToSVG
)
from skimage.transform import ProjectiveTransform
import numpy as np
from flask import (current_app)

DATA_DIR = f'{os.getcwd()}/flaskr/static/participantData/'
def test_vowelChartPoints():
    # test the basic case
    vowelsFH = [{'vwl': [{
        "f1": 290.5,
        "f2": 2300.6
    },{
        "f1": 177.0,
        "f2": 2235.9
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
    FH, BH = (2300.6,177.0), (736.4,274.6)
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

def test_freqToSVG(app):
    def transform(t, freq):
        xt = t[0]
        yt = t[1]
        wt = t[2]
        x = xt[0] * freq[0] + xt[1] * freq[1] + xt[2]
        y = yt[0] * freq[0] + yt[1] * freq[1] + yt[2]
        w = wt[0] * freq[0] + wt[1] * freq[1] + wt[2]
        return [x / w, y / w]

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






