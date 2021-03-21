import os
from os import environ
from flask import Flask
import flask_cors
from prometheus_flask_exporter import PrometheusMetrics

from .utils.logger import Logger
from .routes.prediction import prediction_routes
from .commands import init_database, add_user
from .connection.initializers import database, guard
from .models.user import User
from .routes.auth import auth_routes
from .routes.task import task_routes

cors = flask_cors.CORS()

app = Flask(__name__)

metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Application info', version='1.0.3')

# formatter = json_log_formatter.JSONFormatter()
# json_handler = logging.FileHandler(filename='/var/log/adapttext.json')
# json_handler.setFormatter(formatter)
# logger = logging.getLogger('adapttext')
# logger.addHandler(json_handler)
# logger.setLevel(logging.INFO)

# logging.basicConfig(filename='error.log',level=logging.DEBUG)

# app.config['FLASK_APP'] = '/var/adapttext/api/api.py'
app.config['DATADOG_ENV'] = 'development'
app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLITE_DB_URI')
app.config['JWT_ACCESS_LIFESPAN'] = {'hours': 24}
app.config['JWT_REFRESH_LIFESPAN'] = {'days': 30}
# app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.getcwd(), environ.get('SQLITE_DB_NAME'))}"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://spubxaae:mDLa_tbGGv7jQAWQy8J5UCr5kh_L84_H@rosie.db.elephantsql.com:5432/spubxaae"

database.init_app(app)

guard.init_app(app, User)
cors.init_app(app)

app.cli.add_command(init_database)
app.cli.add_command(add_user)


app.register_blueprint(auth_routes, url_prefix='/api')
app.register_blueprint(task_routes, url_prefix='/api')
app.register_blueprint(prediction_routes, url_prefix='/api')

# provide app's version and deploy environment/config name to set a gauge metric
# register_metrics(app, app_version="v0.1.2", app_config="development")

# Plug metrics WSGI app to your main app with dispatcher
# dispatcher = DispatcherMiddleware(app.wsgi_app, {"/metrics": make_wsgi_app()})
logger = Logger()
if __name__ == '__main__':
    app.run(debug=True)
    logger.info('Server started...')
    # run_simple(hostname="0.0.0.0", port=5000, application=dispatcher)
