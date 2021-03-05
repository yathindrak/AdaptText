import click
from flask.cli import with_appcontext

from .connection.initializers import guard, database
from .models.user import User


@click.command(name='init_database')
@with_appcontext
def init_database():
    database.create_all()


@click.command(name='add_user')
@click.argument("name")
@click.argument("password")
@with_appcontext
def add_user(name: str, password: str):
    user = User(username=name, password=guard.hash_password(password))

    database.session.add(user)
    database.session.commit()

# flask init_database
# flask add_user yathindra yathindra123