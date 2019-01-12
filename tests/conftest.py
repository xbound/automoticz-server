import pytest

from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from automoticz.app import create_app
from automoticz.models import User, BLEDevice
from automoticz.extensions import db as _db


@pytest.fixture
def app():
    return create_app()


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


@pytest.fixture
def user(database):
    username = 'user'
    blu_id = '91:74:4D:78:FC:30'
    user = User(username=username)
    user.devices.append(BLEDevice(name=blu_id))
    database.session.add(user)
    database.session.commit()
    return user


@pytest.fixture
def access_token(app, user):
    with app.app_context():
        access_token = create_access_token(user.id)
        return access_token


@pytest.fixture
def refresh_token(app, user):
    with app.app_context():
        refresh_token = create_refresh_token(user.id)
        return refresh_token
