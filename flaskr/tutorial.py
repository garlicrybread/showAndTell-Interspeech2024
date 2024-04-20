from flask import (
    Blueprint, flash, g, redirect,
    render_template, request, url_for, jsonify,
    current_app
)

from werkzeug.exceptions import abort

# from flask_login import login_required, current_user
# from flaskr.user import User
import pandas as pd
import os

# from flaskr.audio import record_file

bp = Blueprint('tutorial', __name__, url_prefix='/tutorial')

@bp.route('/vowelP1', methods=('GET', 'POST'))
def vowelP1():
    return render_template('tutorial/vowelP1.html')

@bp.route('/vowelP2', methods=('GET', 'POST'))
def vowelP2():
    return render_template('tutorial/vowelP2.html')

@bp.route('/vowelP3', methods=('GET', 'POST'))
def vowelP3():
    return render_template('tutorial/vowelP3.html')

@bp.route('/vowelP4', methods=('GET', 'POST'))
def vowelP4():
    return render_template('tutorial/vowelP4.html')

@bp.route('/vowelP5', methods=('GET', 'POST'))
def vowelP5():
    return render_template('tutorial/vowelP5.html')

@bp.route('/vowelP6', methods=('GET', 'POST'))
def vowelP6():
    return render_template('tutorial/vowelP6.html')
