import click
import os
import pytest

from automoticz.utils.constants import ENV

@click.command()
def test():
    '''
    Run tests.
    '''
    os.environ['FLASK_ENV'] = ENV.TESTING
    pytest.main(['--rootdir', './tests'])