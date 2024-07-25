# author: where unspecified, Charlotte Yoder off the Flask tutorial
# https://flask.palletsprojects.com/en/2.3.x/tutorial/
# Changes are mainly converting the database from SQL to mongodb

import os
import functools
import time

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort, current_app, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
import pymongo.errors as pyer
from flask_login import (
    LoginManager, current_user, login_required, login_user, logout_user,
)

# Google authentication
from google.oauth2 import id_token
from google.auth.transport import requests

# from flaskr.user import User

import pandas as pd

# Configuration
# TODO: Generate a client_id and secret
CLIENT_ID = os.environ.get("CLIENT_ID", None)

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/', methods=["GET", "POST"])
def home():
    return render_template('main/home.html')

@bp.route('/vowelCalibration',methods=['GET'])
def vowelCalibration():
    return render_template('main/vwlCal-oneByOne.html',user_id=current_app.config['USER_ID'])


# @bp.route("/google-callback", methods=["POST"])
# def callback():
#     # Authors: Mix of Google's Developer Page and Alexander VanTol (Real Python)
#     # https://developers.google.com/identity/gsi/web/guides/verify-google-id-token
#     # https://realpython.com/flask-google-login/
#     print("In callback")
#     csrf_token_cookie = request.cookies.get('g_csrf_token')
#     if not csrf_token_cookie:
#         abort(400, 'No CSRF token in Cookie.')
#     csrf_token_body = request.form.get('g_csrf_token')
#     if not csrf_token_body:
#         abort(400, 'No CSRF token in post body.')
#     if csrf_token_cookie != csrf_token_body:
#         abort(400, 'Failed to verify double submit cookie.')
#     token = request.form.get('credential')
#     time.sleep(2)
#     try:
#         # Specify the CLIENT_ID of the app that accesses the backend:
#         print("verifying token...")
#         idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
#
#         # ID token is valid. Get the user's Google Account ID from the decoded token.
#         user = load_user(idinfo)
#     except ValueError as e:
#         # Invalid token
#         print(f"Invalid token: {e}")
#         flash(f"Invalid token: {e}")
#         return redirect(url_for('login'))
#     # Begin user session by logging the user in
#     add_csv_data_to_config(user)
#     login_user(user)
#
#     # Send user to the homepage
#     # TODO: Return appropriate visual for the user at this time. Defaults to No vis right now
#     return redirect(url_for(f"practice.wordPair", pairID=user.location[1]))
#
# @bp.route("/dev_login", methods=["POST"])
# def dev_login():
#     idinfo = {
#         "sub": "33",
#         "given_name": "Pippin",
#         "email": "foolOfATook@gmail.com",
#         "picture": "https://static.wikia.nocookie.net/pjhobbitlotr/images/8/86/PippinBoyd.png/revision/latest?cb"
#                    "=20170219174505"
#     }
#     user = load_user(idinfo)
#     add_csv_data_to_config(user)
#     login_user(user)
#     return jsonify({'redirectUrl': url_for(f"practice.wordPair", pairID=user.location[1])})
#
# def load_user(idinfo):
#     # Create a user in your db with the information provided by Google
#     users_id = idinfo['sub']
#     users_name = idinfo['given_name']
#     users_email = idinfo['email']
#     picture = idinfo['picture']
#     user = User(
#         id_=users_id, name=users_name, email=users_email,
#         profile_pic=picture, visualization=None, ordering=None,
#         location=None
#     )
#     # If user already exists, return with user
#     if user.get(user.id):
#         print(f"user already added: {user.name}")
#         user = User.get(user.id)
#         return user
#
#     vis, ordering, location = getUserSetup()
#     user.visualization = vis
#     user.ordering = ordering
#     user.location = location
#
#     User.create(user.id, user.name, user.email, user.profile_pic,
#                 user.visualization, user.ordering, user.location)
#     return user
#
# def add_csv_data_to_config(user):
#     '''
#     Takes in a user object and adds the appropriate practice list data to the app config under PRACTICE_DATA.
#     This is run only when the user first logs in to avoid needing to load the csv every time we need that data.
#
#     :param user:
#     :return:
#     '''
#     current_directory = os.getcwd()
#     file_path = f"flaskr/data/{user.visualization}_pairs/{user.ordering}_practice.csv"
#     file_path = os.path.join(current_directory, file_path)
#     df = pd.read_csv(file_path)
#     print(f"Adding df to config {df}")
#     current_app.config.update(PRACTICE_DATA=df)
#     return
#
# def getUserSetup():
#     '''
#     location is initialized to the first week and first word pair in first_practice for whichever
#     Connects to db and gets the next row of the csv userConditions based on the number that is stored
#     in the db "miscInfo" under "nextCondition".
#     After getting number from the db, it looks up the appropriate location given the vis and ordering
#     from the csv.
#     :return vis, ordering, location:
#     '''
#     # get nextCondition from the db, then update number for nextCondition
#     mongo = current_app.config["MONGO"]
#     # then update the line number for the current condition
#     field = "nextCondition"
#     condition = mongo.db.miscInfo.distinct(field)[0]
#     update = {"$set": {field: condition + 1}}
#     mongo.db.miscInfo.update_one({field: condition}, update)
#     # load csv and get line where line# = condition
#     conditionFilePath = f"flaskr/data/userConditions.csv"
#     df = pd.read_csv(conditionFilePath)
#     # Filter to find the row where condition matches the row number
#     row = df[df["rowNum"] == condition]
#     print(row)
#     vis = row["condition"].iloc[0]
#     order = row["number"].iloc[0]
#     # use vis and order to read in word pair for location
#     current_directory = os.getcwd()
#     file_path = f"flaskr/data/{vis}_pairs/{order}_practice.csv"
#     file_path = os.path.join(current_directory, file_path)
#     df = pd.read_csv(file_path)
#     weekNum = 1
#     week_df = df[df['week'] == weekNum]
#     firstPair = week_df[week_df["id"] == "p11"]
#     location = (firstPair["spa0"].iloc[0], firstPair["spa1"].iloc[0])
#     print(location)
#     location = [str(weekNum), f"{location[0]}-{location[1]}","p11"]
#     # TODO: update the first word depending on which order and vis a user sees.
#     return vis, order, location
#
# @bp.route('/logout')
# def logout():
#     session.clear()
#     logout_user()
#     return redirect(url_for('login'))
