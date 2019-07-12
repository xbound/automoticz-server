import pytest
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_socketio import SocketIOTestClient

from automoticz.app import create_app
from automoticz.extensions import db as _db


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
def sio(app):
    sio = app.extensions['socketio']
    return sio


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
