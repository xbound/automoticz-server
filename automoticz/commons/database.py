from automoticz.extensions import db
from automoticz.models import User


def add_new_user_if_not_exists(data):
    '''
    Helper function for adding new user to database.

    :param data: user's data
    :return: user instance
    '''
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        user = User(username=data['username'])
        db.session.add(user)
        db.session.commit()
    return user