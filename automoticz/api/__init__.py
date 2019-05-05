from automoticz.extensions import jwt
from automoticz.utils import is_token_revoked


@jwt.token_in_blacklist_loader
def check_if_token_revoked(decoded_token):
    return is_token_revoked(decoded_token)
