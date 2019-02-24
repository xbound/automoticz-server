import click
import coverage
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

@click.command()
def test_coverage():
    '''
    Run tests with coverage.
    '''
    os.environ['FLASK_ENV'] = ENV.TESTING
    cov = coverage.Coverage()
    cov.start()
    pytest.main(['--rootdir', './tests'])
    cov.stop()
    cov.save()
