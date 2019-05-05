import click
import os
import subprocess


@click.command()
def reset_migrations():
    '''
    Reset database migrations.
    '''
    subprocess.run(['rm', '-rf', 'migrations/'])
    subprocess.run([
        'rm',
        'db.sqlite3',
    ])