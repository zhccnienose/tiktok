import faker
import pytest
from app import create_app

Fake = faker.Faker()


@pytest.fixture()
def app():
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


class Login(object):
    def __init__(self, client, username, password):
        self.username = username
        self.password = password
        response = client.post(
            '/user/login',
            data={'username': username, 'password': password})
        print(response.json['base']['msg'])
        assert response.status_code == 200
        self.data = response.json['data']
