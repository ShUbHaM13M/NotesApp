import click
from flask.cli import with_appcontext

from app import db

@click.command(name="create_table")
@with_appcontext
def create_table():
    db.create_all()
    