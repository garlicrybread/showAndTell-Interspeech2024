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
def viwekP1():
    return render_template('tutorial/vowelP1.html')
@bp.route('/vowelP2', methods=('GET', 'POST'))
def viwekP2():
    return render_template('tutorial/vowelP2.html')
