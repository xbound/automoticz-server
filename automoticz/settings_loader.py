import pathlib


def load(obj, env=None, silent=True, key=None, filename=None):
    """
    Custom settings loader for Dynaconf for replacing BASE_URL values
    with real path.
    :param obj: the settings instance
    :param env: settings current env (upper case) default='DEVELOPMENT'
    :param silent: if errors should raise
    :param key: if defined load a single key, else load all from `env`
    :param filename: Custom filename to load (useful for tests)
    :return: None
    """
    # Load data from your custom data source (file, database, memory etc)
    # use `obj.set(key, value)` or `obj.update(dict)` to load data
    # use `obj.logger.debug` to log your loader activities
    # use `obj.find_file('filename.ext')` to find the file in search tree
    # Return nothing
    BASE_URL = pathlib.Path(__file__).parent
    obj.update(
        CLIENT_SECRETS_FILE=obj.CLIENT_SECRETS_FILE.format(
            BASE_URL=str(BASE_URL)),
        CREDENTIALS_FILE=obj.CREDENTIALS_FILE.format(
            BASE_URL=str(BASE_URL)),
        SQLALCHEMY_DATABASE_URI=obj.SQLALCHEMY_DATABASE_URI.format(
            BASE_URL=str(BASE_URL.parent)))