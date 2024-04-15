from flaskr.main import saveUserId
from flask import current_app, url_for

def test_saveUserId(app, client):
    with app.app_context():
        userId = 'yoder'
        data = {'userId': userId}
        response = client.post(url_for('main.saveUserId'),json=data)
        assert response.status_code == 200
        assert response.get_json()['saved'] == True
        assert current_app.config['USER_ID'] == userId

        userId = 'g19'
        data = {'userId': userId}
        response = client.post(url_for('main.saveUserId'),json=data)
        assert response.status_code == 200
        assert current_app.config['USER_ID'] == userId



