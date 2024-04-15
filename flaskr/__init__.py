# Python standard libraries
import os
# import pymongo
import json
# import ast

#Third-party libraries
from flask import (
    Flask, render_template, g,
    redirect, request, url_for
)

from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask.cli import AppGroup
from flask_pymongo import PyMongo
from dotenv import load_dotenv
# Internal imports
# from flaskr.user import User

# Configuration
# GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
# print(f"google client secret: {GOOGLE_CLIENT_SECRET}")
load_dotenv() # take environment variables from .env
MONGODB = os.environ.get("MONGODB_URI")
# for mongodb Compass local connection: mongodb://localhost:27017
# MONGODB = "mongodb://127.0.0.1"
# conn_str = config("MONGODB_URI")

def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True, static_folder='static')
    init_cli = AppGroup("init")
    if test_config:
        app.config.from_mapping(
            TESTING=True,
            MONGO_URI=f"{MONGODB}/testProVis",  # MongoDB connection string for testing
            TRANSFORM_FREQ_SVG= None,
            SVG_COORDINATES=None,
            USER_ID=None
        )
        print("Testing config")
    else:
        app.config.from_mapping(
            SECRET_KEY='dev',
            MONGO_URI=f"{MONGODB}/pronunciation_vis",  # MongoDB connection string for production
            TRANSFORM_FREQ_SVG = None,
            SVG_COORDINATES = None,
            USER_ID = None
        )
        print("Development config")

    if 'MONGO_URI' in app.config:
        app.config['MONGO'] = PyMongo(app)  # Initialize Flask-PyMongo with the app
    else:
        raise Exception("No MONGO_URI configuration found.")

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

    # # User session management setup
    # # https://flask-login.readthedocs.io/en/latest
    # login_manager = LoginManager()
    # login_manager.init_app(app)
    # check to make sure we are at the correct directory level
    if "flaskr" not in os.listdir(os.getcwd()):
        print("moving into proVISweb")
        os.chdir(os.path.join(os.getcwd(),"pronunciation_VIS_web"))

    # shouldn't need a login helper for the show and tell
    # # Flask-Login helper to retrieve a user from our db
    # @login_manager.user_loader
    # def load_user(user_id):
    #     return User.get(user_id)
    from . import main
    app.register_blueprint(main.bp)
    app.add_url_rule('/', endpoint='home')

    from . import db

    from . import tutorial
    app.register_blueprint(tutorial.bp)

    from . import practice
    app.register_blueprint(practice.bp)

    from . import audioRecording
    app.register_blueprint(audioRecording.bp)

    from . import signalProcessing
    app.register_blueprint(signalProcessing.bp)

    from . import coordinates
    app.register_blueprint(coordinates.bp)



    @init_cli.command("db")
    def init_db():
        print("Initializing database...")
        db.init_db()

    app.cli.add_command(init_cli)
    return app
