from flask import (
    Blueprint, flash, g, redirect,
    render_template, request, url_for, jsonify,
    current_app
)

from werkzeug.exceptions import abort

from flask_login import login_required, current_user
# from flaskr.user import User
import pandas as pd
import os

# from flaskr.audio import record_file

bp = Blueprint('practice', __name__, url_prefix='/practice')

@bp.route('/weeks', methods=('GET', 'POST'))
@login_required
def weeks():
    return render_template('practice/weeks.html')

@bp.route('/api/loadWeeklyWordPairs', methods=["POST"])
@login_required
def loadWeeklyWordPairs():
    '''
    Fetches the week number from the query parameter and loads the appropriate pairs for that week and user
    '''
    try:
        # week_num will be a number of type str
        week_num = request.get_json()['week']
        # TODO: use config data
        current_directory = os.getcwd()
        print(f"current directory: {current_directory}")
        file_path = f"flaskr/data/{current_user.visualization}_pairs/{current_user.ordering}_practice.csv"
        file_path = os.path.join(current_directory,file_path)
        df = pd.read_csv(file_path)
        week_df = df[df['week']==int(week_num)]
        data = week_df.to_dict(orient='records')
        return jsonify({"data": data})

    except FileNotFoundError:
        print(f"File not found at path: {file_path}")
        #TODO: return error to client
        return "ERROR"

@bp.route('/api/retrieveLocationInfo', methods=["POST"])
@login_required
def retrieveLocationInfo():
    locationInfo = current_user.location
    return jsonify({"location": locationInfo})

@bp.route('/api/updateWeekNumber', methods=["POST"])
@login_required
def updateWeekNumber():
    weekNum = request.get_json()['week']

    # update week value in the database
    user = User.get(current_user.id)
    User.update(user.id, 'location.0', weekNum)

    # return jsonify({"week": weekNum})
    return jsonify({"week": weekNum})

@bp.route('/api/updateLocation', methods=["POST"])
@login_required
def updateLocation():
    idxs = request.get_json()['idxs']
    values = request.get_json()['values']
    user = User.get(current_user.id)

    # update week value in the database
    for idx,value in zip(idxs,values):
        User.update(user.id, 'location.'+idx, value)

    # return jsonify({"week": weekNum})
    return jsonify({"data": value})

@bp.route('/api/retrieveNextWordLocation', methods=["POST"])
@login_required
def retrieveNextWordLocation():
    '''
    Expects location and direction in request json, calculates next id and new week if needed in the form of "p##"
    :json direction: "prev" or "next"
    :json location: list of length three [week, word pair, p## (id)]
    :return jsonified location:
    '''
    # todo: test to make sure the correct id is always calculated.
    print("Retrieving Next word Location")
    data = request.get_json()
    location = data.get("location")
    direction = data.get("direction")
    week = int(location[0])
    current_id = location[2]
    # convert word number to integer
    wordNum = int(current_id[2])
    dayNum = int(current_id[1])
    if direction == "prev":
        if wordNum == "p11" and week == 1:
            # Make sure we're not at position one. The button SHOULDN'T appear, but I'm not taking chances
            # if we're at the first button in the first week, don't move
            return jsonify({"new_location":location})
        if wordNum >= 2:
            # if wordNum >= 2, it is the only thing that will decrease
            wordNum -= 1
        else:
            # if wordNum is 1, see if dayNum is >= 2
            if dayNum >= 2:
                dayNum -= 1
                wordNum = 5
            else:
                if week >= 2:
                    week -= 1
                    dayNum = 6
                    wordNum = 5

    elif direction == "next":
        if wordNum == "p65" and week == 8:
            # Make sure we're not at position one. The button SHOULDN'T appear, but I'm not taking chances
            # if we're at the first button in the first week, don't move
            return jsonify({"new_location":location})
        if wordNum <= 4:
            wordNum += 1
        else:
            if dayNum <= 5:
                dayNum += 1
                wordNum = 1
            else:
                if week <= 7:
                    week += 1
                    dayNum = 1
                    wordNum = 1
    new_id = f"p{dayNum}{wordNum}"
    pair = retrieveWordPair(week,new_id)
    new_location = [week, pair, new_id]
    print(f"old loc {location}, new loc: {new_location}\n\n")
    return jsonify({"new_location": new_location})

# todo: write function that takes in p## (and week?) and returns word pair associated
# @bp.route('/api/retrieveWordPair', methods=["POST"])
# @login_required
def retrieveWordPair(week, id):
    df = current_app.config['PRACTICE_DATA']
    weekdf = df[df["week"] == int(week)]
    row = weekdf[weekdf["id"] == id]#.iloc[0]
    spa0, spa1 = row['spa0'].iloc[0], row['spa1'].iloc[0]
    return f'{spa0}-{spa1}'

@bp.route('/api/record', methods=('GET', 'POST'))
# @login_required
def record():
    print("in record")
    gotAudio = record_file('bata','tester')
    print(f"I'm here {gotAudio}")
    return jsonify({'gotAudio': gotAudio})

@bp.route('/wordsInWeek', methods=('GET', 'POST'))
@login_required
def wordsInWeek():
    return render_template('practice/wordsInWeek.html')

@bp.route('/wordPair', methods=('GET', 'POST'))
@login_required
def wordPair():
    return render_template('practice/wordPair.html')