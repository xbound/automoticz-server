from sqlalchemy.orm.exc import NoResultFound
from automoticz.models import JWToken

def is_token_revoked(decoded_token):
    '''
    Checks if the given token is revoked or not. Because we are adding all the
    tokens that we create into this database, if the token is not present
    in the database we are going to consider it revoked, as we don't know where
    it was created.
    '''
    jti = decoded_token['jti']
    try:
        token = JWToken.query.filter_by(jti=jti).one()
        return token.revoked
    except NoResultFound:
        return True