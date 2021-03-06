import flask_praetorian
from flask import Blueprint, jsonify, request, make_response
from flask_praetorian import auth_required
from sqlalchemy.exc import IntegrityError

from ..schemas.task import TaskSchema
from ..models.user import User
from ..models.task import Task
from ..utils.http_utils import make_err_response
from ..connection.initializers import guard, database

task_routes = Blueprint('task', __name__)


@task_routes.route('/task', methods=['POST'])
@auth_required
def create():
    json_obj = request.get_json()
    if not json_obj:
        return make_err_response('Bad Request', 'No valid entries provided', 400)
    try:
        name = json_obj['name']
        description = json_obj['description']
        progress = json_obj["progress"]
        model_path = None
    except:
        return make_err_response('Bad Request', 'No valid entries provided', 400)

    current_user = User.lookup(flask_praetorian.current_user().username)

    task = Task(name=name, description=description, progress=progress, model_path=model_path, user_id=current_user.id)

    try:
        database.session.add(task)
        database.session.commit()
    except IntegrityError:
        return make_err_response('Bad Request', 'Duplicated name entered', 400)

    return '', 201


@task_routes.route('/task/<id>')
@auth_required
def get_by_id(id):
    get_task = Task.query.get(id)
    task_schema = TaskSchema()
    task = task_schema.dump(get_task)
    return make_response(jsonify({"task": task}))

@task_routes.route('/task/user/<uid>')
@auth_required
def get_by_username(uid):
    get_tasks = Task.query.filter_by(user_id=uid).all()
    task_schema = TaskSchema(many=True)
    tasks = task_schema.dump(get_tasks)
    return make_response(jsonify({"task": tasks}), 200)


@task_routes.route('/tasks')
@auth_required
def get_all():
    current_user = flask_praetorian.current_user().id

    get_tasks = Task.query.filter_by(user_id=current_user).all()

    task_schema = TaskSchema(many=True)
    tasks = task_schema.dump(get_tasks)

    return make_response(jsonify({"tasks": tasks}), 200)


@task_routes.route('/task/<id>', methods=['PUT'])
@auth_required
def update_by_id(id):
    data = request.get_json()
    get_task = Task.query.get(id)

    progress = data.get('progress')
    model_path = data.get('model_path')

    if progress and model_path:
        database.session.query(Task).filter_by(id=id).update({"progress": progress, "model_path": model_path})
    elif progress:
        database.session.query(Task).filter_by(id=id).update({"progress": progress})
    elif model_path:
        database.session.query(Task).filter_by(id=id).update({"model_path": model_path})

    database.session.commit()

    task_schema = TaskSchema()
    task = task_schema.dump(get_task)
    return make_response(jsonify({"task": task}))

# @task_routes.route('/protected')
# @auth_required
# def protected():
#     return jsonify({'result': 'You are in a special area!'}), 200
#
#
# @task_routes.route('/refresh', methods=['POST'])
# def refresh():
#     json_data = request.get_json()
#
#     if not json_data:
#         return make_err_response('Bad Request', 'Token not found', 400)
#
#     prev_token = json_data['token']
#     if not prev_token:
#         return make_err_response('Bad Request', 'Token not found', 400)
#
#     token = guard.refresh_jwt_token(prev_token)
#     return jsonify({'access_token': token})
