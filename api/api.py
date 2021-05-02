import os
from os import environ
from flask import Flask
import flask_cors
from prometheus_flask_exporter import PrometheusMetrics

from .utils.logger import Logger
from .commands import init_database, add_user
from .connection.initializers import database, guard
from .models.user import User
from .controller.auth import auth_controller
from .controller.task import task_controller
from .controller.prediction import prediction_controller

cors = flask_cors.CORS()

app = Flask(__name__)

metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Application info', version='1.0.3')

app.config['DATADOG_ENV'] = 'development'
app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
app.config['JWT_ACCESS_LIFESPAN'] = {'hours': 24}
app.config['JWT_REFRESH_LIFESPAN'] = {'days': 30}
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://spubxaae:mDLa_tbGGv7jQAWQy8J5UCr5kh_L84_H@rosie.db.elephantsql.com:5432/spubxaae"

database.init_app(app)

guard.init_app(app, User)
cors.init_app(app)

app.cli.add_command(init_database)
app.cli.add_command(add_user)


app.register_blueprint(auth_controller, url_prefix='/api')
app.register_blueprint(task_controller, url_prefix='/api')
app.register_blueprint(prediction_controller, url_prefix='/api')

logger = Logger()
if __name__ == '__main__':
    app.run(debug=True, port=8080)
    logger.info('Server started...')
