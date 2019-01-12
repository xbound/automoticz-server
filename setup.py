from setuptools import setup, find_packages

__version__ = '0.1-dev'

setup(
    name='automoticz',
    version=__version__,
    packages=find_packages(exclude='tests'),
    entry_points={
        'console_scripts': [
            'automoticz = automoticz.manage:cli'
        ]
    }
)