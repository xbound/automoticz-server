import sys
import click
from flask import current_app as app
from flask.cli import FlaskGroup
from automoticz.utils.constants import ENV
from automoticz.app import create_app


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    '''
    Main entry point.
    '''
    if app.config.ENV == ENV.TESTING:
        print('Running in TESTING mode...Aborting!')
        sys.exit(1)
