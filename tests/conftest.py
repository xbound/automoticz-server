import pytest

from flask_socketio import SocketIOTestClient
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from automoticz.app import create_app
from automoticz.extensions import db as _db


@pytest.fixture
def app():
    return create_app(True)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def database(app):
    _db.app = app

    with app.app_context():
        _db.create_all()

    yield _db

    _db.session.close()
    _db.drop_all()
