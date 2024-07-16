from flaskr import create_app
from flask import current_app

def test_config(app):
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing
    with app.app_context():
        tSpa = current_app.config['TRANSFORM_SPA']
        assert tSpa is not None
        assert type(tSpa) == list
        assert len(tSpa) == 3
