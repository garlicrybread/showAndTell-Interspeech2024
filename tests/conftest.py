import pytest

from flaskr import create_app
from flaskr.db import init_db
from flask_login import current_user, login_user

from flask import current_app


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SERVER_NAME': 'localhost:5000',
        'APPLICATION_ROOT': '/',
        'PREFERRED_URL_SCHEME': 'http',  # Use 'http' or 'https' based on your app

    })
    with app.app_context():
        pass
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def test_user():
    # TODO: modify if needed for show and tell
    idinfo = {
        "sub": "33",
        "given_name": "Pippin",
        "email": "foolOfATook@gmail.com",
        "picture": "https://static.wikia.nocookie.net/pjhobbitlotr/images/8/86/PippinBoyd.png/revision/latest?cb=20170219174505"
    }
    vis = "const"
    ordering = "first"
    location = ["1", "teísmo-deísmo"]

    return User(
        id_=idinfo["sub"],
        name=idinfo["given_name"],
        email=idinfo["email"],
        profile_pic=idinfo["picture"],
        visualization=vis,
        ordering=ordering,
        location=location
    )