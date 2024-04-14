from skimage.transform import ProjectiveTransform
import numpy as np
import os
import json

from flask import (
    current_app, Blueprint, request, jsonify
)

from flaskr.signalProcessing import (
    maxAndMinOfFormants, audioToVwlFormants, formantsToJsonFormat, writeToJson
)
from pprint import pprint
bp = Blueprint('coordinates', __name__, url_prefix='/coordinates')

@bp.route('/api/processCoordinateData', methods=["POST"])
def processCoordinateData():
    rootDirectory = request.get_json()['gotAudio']
    svg = current_app.config['SVG_COORDINATES']
    for path, dir, files in os.walk(rootDirectory):
        for file in files:
            if '.wav' in file:
                f1, f2 = audioToVwlFormants(path, file)
                jsonName = f"{file.split('.')[0]}-vwlCal.json"
                data = formantsToJsonFormat(f1, f2, True)
                writeToJson(path, jsonName, data)
    vowels = jsonToVowelPoints(rootDirectory)
    coordinates = vowelChartCoordinates(vowels)
    transformArray(coordinates,svg)
    return jsonify({'success':True})

def transformArray(actualCoordinates, svgCoordinates):
    '''
    takes in vowel coordinates and coordinates of the SVG
    - calculates the transform using a projective transform
    - updates TRANSFORM_FREQ_SVG
    - returns transform (needed?)
    '''
    t = ProjectiveTransform()
    pprint(actualCoordinates)
    pprint(svgCoordinates)
    src = np.asarray(actualCoordinates)
    dst = np.asarray(svgCoordinates)
    if not t.estimate(src, dst): raise Exception("estimate failed")

    # Homogeneous to Euclidean
    # [x, y, w]^T --> [x/w, y/w]^T
    x = t.params[0].tolist()
    y = t.params[1].tolist()
    w = t.params[2].tolist()
    transform = [x,y,w]
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
    frontHigh = (xFH,yFH)
    backHigh = (xBH,yBH)
    frontLow = (xFL,yFL)
    backLow = (xBL,yBL)
    coordinates = [frontHigh,backHigh,frontLow,backLow]
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
