After setting up beacon and generating OAuth2 keys we could start developing our authentication server. In this example we will be using Flask micro-framework with addtional extensions/pluigns. Namely we will use:

* [Flask-RESTPlus](https://flask-restplus.readthedocs.io/en/stable/) - this extension will allow us to create endpoints with interactive [Swagger UI](https://swagger.io/tools/swagger-ui/) API documentation.
* [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/en/latest/) - will be used to generate JWT access token for our Android mbile app client.
* [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org) - will allow us to declare database models that will be used to create tables for storing data like: registered devices, OAuth2 credentials and JWT tokens.
* [Flask-Migrate](https://flask-migrate.readthedocs.io/en/stable/) - small utility extension that will simplify creation of database with migrations.
* [Dynaconf](https://dynaconf.readthedocs.io/en/latest/) - additional library that will allow us load settings for our Flask application from `.yaml` and `.env` config files.

To install all these packages we will use [`pipenv`](https://github.com/pypa/pipenv):
```shell
$ pipenv install flask-restplus
$ pipenv install flask-jwt-extended 
$ pipenv install flask-sqlalchemy 
$ pipenv install flask-migrate
$ pipenv install dynaconf
```
Also, if we want to store configurations for app in .yaml file we need to install this Dynaconf dependency:
``` 
$ pipenv install dynaconf[yaml]
```

Additionally, we will need to download [Google API client for Python](https://developers.google.com/api-client-library/python/) with few packages that will help authenticate and authorize our app to use PBAPI:
```shell
$ pipenv install google-api-python-client google-auth google-auth-httplib2 google-auth-oauthlib
```