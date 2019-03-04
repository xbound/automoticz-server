# Automoticz server

## Setting up development environment

```shell
$ pipenv install --dev
```

## Setting up database for local development

In project root create file `.secrets.yaml` and set following variables:

```yaml
default:
  SECRET_KEY: <your-secret-key>
  JWT_SECRET_KEY: <your-jwt-secret-key>
  CLIENT_SECRETS_FILE: "<path-to-client-id-file>"
  PROJECT_ID: "<project-id>"
development:
  SQLALCHEMY_DATABASE_URI: "<path-to-sqlite-db-file>"
```

**NOTE**:
Application works with [Proximity Beacon API](https://developers.google.com/beacons/proximity/guides) and generated OAuth2 Client ID is required to interact with beacons' data.

Run migration commands:

```shell
$ pipenv flask db migrate
$ pipenv flask db upgrade
```

## Running development server

```shell
$ pipenv run flask run
```

After starting up server, Swagger API documentation will be available at http://127.0.0.1:5000/api/. 

## Running gunicorn server

```
$ pipenv run ./run.sh
```

## Testing and coverage

Run flask command to run pytest:
```shell
$ pipenv run flask test
```

To run pytest using:

```shell
$ pipenv run pytest
```

Switch `FLASK_ENV` from `development` to `testing` in `.env` file.

Run coverage:

```shell
$ pipenv run coverage run -m pytest
```

Get report:

```shell
$ pipenv run coverage report
```

Get report in html:

```shell
$ pipenv run coverage html
```

