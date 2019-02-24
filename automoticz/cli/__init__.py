import click
import os
import subprocess

from automoticz.utils.constants import ENV

@click.command()
def test():
    '''
    Run tests.
    '''
    os.environ['FLASK_ENV'] = ENV.TESTING
    subprocess.run([
        'pytest',
        '--cov=automoticz',
        'tests/'
    ])