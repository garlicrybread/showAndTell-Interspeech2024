from skimage.transform import ProjectiveTransform
import numpy as np
import os
import json

from flask import (
    current_app, Blueprint, request, jsonify
)

from flaskr.signalProcessing import (
    audioToVwlFormants, formantsToJsonFormat, writeToJson, maxAndMinOfFormants
)
from pprint import pprint
bp = Blueprint('vowelCalibration', __name__, url_prefix='/vowelCalibration')

flaskrPath = f'{os.getcwd()}/flaskr/'
dataDir = 'static/participantData/'

@bp.route('/api/processCoordinateData', methods=["POST"])
def processCoordinateData():
    spa = request.get_json()['spa']
    print(f'\n{spa, type(spa)}, spa')
    if spa:
        id = 'spaM0'
    else:
        id = current_app.config['USER_ID']
    rootDirectory = flaskrPath + dataDir + id + '/vowelCalibration/'
    svg = current_app.config['SVG_COORDINATES']
    if not spa:
        for path, dir, files in os.walk(rootDirectory):
            for file in files:
                if '.wav' in file:
                    print(f'in file {file}')
                    f1, f2 = audioToVwlFormants(path, file)
                    jsonName = f"{file.split('.')[0]}-vwlCal.json"
                    data = formantsToJsonFormat(f1, f2, True)
                    writeToJson(path, jsonName, data)
    vowels = jsonToVowelPoints(rootDirectory)
    print(f'in processCoordinateData {vowels}')
    coordinates = vowelChartCoordinates(vowels)
    if spa:
        transformArray(coordinates, svg, True)
    else:
        transformArray(coordinates,svg)
    return jsonify({'success':True})

@bp.route('/api/saveUserId',methods=["POST"])
def saveUserId():
    userId = request.get_json()
    current_app.config.update(USER_ID=userId['userId'])
    return jsonify({'saved':True})

def transformArray(actualCoordinates, svgCoordinates, spa=False):
    '''
    takes in vowel coordinates and coordinates of the SVG
    - calculates the transform using a projective transform
    - updates TRANSFORM_FREQ_SVG
    - returns transform (needed?)
    '''
    t = ProjectiveTransform()
    src = np.asarray(actualCoordinates)
    dst = np.asarray(svgCoordinates)
    print(f'src {src}')
    print(f'dst {dst}')
    if not t.estimate(src, dst): raise Exception("estimate failed")

    # Homogeneous to Euclidean
    # [x, y, w]^T --> [x/w, y/w]^T
    x = t.params[0].tolist()
    y = t.params[1].tolist()
    w = t.params[2].tolist()
    transform = [x,y,w]
    if spa:
        current_app.config.update(TRANSFORM_SPA=transform)
        spaFilePath = flaskrPath + dataDir + 'vowelCalibration/spaTransform.txt'
        with open(flaskrPath+dataDir+'spaM0/vowelCalibration/spaTransform.txt', 'w') as f:
            f.write(str(current_app.config['TRANSFORM_SPA']))
    else:
        current_app.config.update(TRANSFORM_FREQ_SVG=transform)
    return transform

def vowelChartCoordinates(vowels):
    ''' vowels is a dictionary {word: jsonFormatData} '''
    words = ['frontHigh','backHigh','frontLow', 'backLow']
    # F = Front, B = Back, H = High, L = Low
    for word, vwls in vowels.items():
        for vwl in vwls:
            maxF1, maxF2, minF1, minF2 = maxAndMinOfFormants(vwl)
            if word == words[0]:
                xFH = maxF2
                yFH = minF1
            elif word == words[1]:
                xBH = minF2
                yBH = minF1
            elif word == words[2]:
                xFL = maxF2
                yFL = maxF1
            elif word == words[3]:
                xBL = minF2
                yBL = maxF1

    # m = abs((yt - y1) / (xt - x1))
    # x3 = y4 / m
    # x range, y range (xmin, xmax, ymin, ymax)
    padf = 50
    padb = 50
    frontHigh = (xFH+padf,yFH-padf)
    backHigh = (xBH-padb,yBH-padb)
    frontLow = (xFL+padf,yFL+padf)
    backLow = (xBL-padb,yBL+padb)
    coordinates = [frontHigh,backHigh,frontLow,backLow]
    print(f'coordinates: {coordinates}')
    return coordinates

def jsonToVowelPoints(rootDirectory):
    vowels = {}
    for path, dir, files in os.walk(rootDirectory):
        for file in files:
            if '.json' in file:
                with open(path+file,'r') as f:
                    data = json.load(f)
                    name,word,_ = file.split('-')
                    vowels[word] = data
    return vowels
