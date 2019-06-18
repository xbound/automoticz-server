# Automoticz server

## Setting up development environment

```shell
$ pipenv install --dev
```

## Setting up database for local development

In project root create file `.secrets.yaml` and set following variables:

```yaml
default:
  PUBLIC_URL: http://127.0.0.1:5000
  SECRET_KEY: <your-secret-key>
  JWT_SECRET_KEY: <your-jwt-secret-key>
  CLIENT_SECRETS_FILE: "<path-to-client-id-file>"
  PROJECT_ID: "<project-id>"
  DOMOTICZ_HOST: <domoticz-host>
  DOMOTICZ_PORT: <domoticz-port>
  DOMOTICZ_USERNAME: <domoticz-username>
  DOMOTICZ_PASSWORD: <domoticz-password>
  DOMOTICZ_API_TIMEOUT: <timeout>
development:
  PUBLIC_URL: <url-of-your-server>
  SQLALCHEMY_DATABASE_URI: "<path-to-sqlite-db-file>"
```

**NOTE**:
Application works with [Proximity Beacon API](https://developers.google.com/beacons/proximity/guides) and generated OAuth2 Client ID is required to interact with beacons' data.

Run migration commands:

```shell
$ pipenv flask db migrate
$ pipenv flask db upgrade
```

## Running development server (no Socket.IO support)

```shell
$ pipenv run flask run
```

After starting up server, Swagger API documentation will be available at http://127.0.0.1:5000/api/. 

## Running uwsgi server

```
$ pipenv run uwsgi
```

## Testing and coverage

Run flask command to run pytest:
```shell
$ pipenv run test
```

Get coverage report:

```shell
$ pipenv run coverage report
```

Get coverage report in html:

```shell
$ pipenv run coverage html
```

