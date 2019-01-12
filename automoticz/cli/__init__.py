import click
import os
import pytest

from automoticz.commons.constants import ENV

@click.command()
def test():
    '''
    Run tests.
    '''
    pytest.main(['--rootdir', './tests'])