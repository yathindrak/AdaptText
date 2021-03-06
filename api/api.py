import os
from os import environ
from flask import Flask
import flask_cors
import logging

from .commands import init_database, add_user
from .connection.initializers import database, guard
from .models.user import User
from .routes.auth import api

cors = flask_cors.CORS()

app = Flask(__name__)

logging.basicConfig(filename='error.log',level=logging.DEBUG)

app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLITE_DB_URI')
app.config['JWT_ACCESS_LIFESPAN'] = {'hours': 24}
app.config['JWT_REFRESH_LIFESPAN'] = {'days': 30}
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.getcwd(), environ.get('SQLITE_DB_NAME'))}"

database.init_app(app)
guard.init_app(app, User)
cors.init_app(app)

app.cli.add_command(init_database)
app.cli.add_command(add_user)


app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
