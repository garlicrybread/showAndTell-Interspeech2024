import os

from flaskr.signalProcessing import (
    vowelChartPoints
)
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

