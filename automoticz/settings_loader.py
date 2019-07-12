import pathlib
import importlib

from flask_restplus import Api


def load_celery_imports(app, default=None):
    ''' Loader for celery tasks imports.

    :param app: Flask application instance.
    :param default: default imports tuple. 
    '''
    celery_tasks = default or tuple()
    celery_tasks += tuple(app.config.CELERY_TASKS)
    return celery_tasks


def load_api_endpoints(app, api: Api):
    ''' Loader for api endpoints.

    :param app: Flask application instance.
    :param api: flask_restplus.Api instance. 
    '''
    endpoint_list = app.config.ENABLED_ENDPOINTS
    for endpoint in endpoint_list:
        end_module = endpoint.get('module')
        end_path = endpoint.get('url_path')
        end_ns = endpoint.get('namespace', 'namespace')
        if not end_module: raise Exception('No module path...')
        if not end_path:
            raise Exception('No url path for "{}"...'.format(end_module))
        module = importlib.import_module(end_module)
        api.add_namespace(getattr(module, end_ns), path=end_path)


def load(obj, env=None, silent=True, key=None, filename=None):
    '''
    Custom settings loader for Dynaconf for replacing BASE_URL values
    with real path.
    :param obj: the settings instance
    :param env: settings current env (upper case) default='DEVELOPMENT'
    :param silent: if errors should raise
    :param key: if defined load a single key, else load all from `env`
    :param filename: Custom filename to load (useful for tests)
    :return: None
    '''
    # Load data from your custom data source (file, database, memory etc)
    # use `obj.set(key, value)` or `obj.update(dict)` to load data
    # use `obj.logger.debug` to log your loader activities
    # use `obj.find_file('filename.ext')` to find the file in search tree
    # Return nothing
    BASE_URL = pathlib.Path(__file__).parent.absolute()
    PARENT_BASE_URL = BASE_URL.parent.absolute()
    obj.update(
        LOGGING_SETTINGS=obj.LOGGING_SETTINGS.format(BASE_URL=str(PARENT_BASE_URL)),
        CLIENT_SECRETS_FILE=obj.CLIENT_SECRETS_FILE.format(
            BASE_URL=str(BASE_URL)),
        CREDENTIALS_FILE=obj.CREDENTIALS_FILE.format(BASE_URL=str(BASE_URL)),
        SQLALCHEMY_DATABASE_URI=obj.SQLALCHEMY_DATABASE_URI.format(
            BASE_URL=str(PARENT_BASE_URL)
        )
    )