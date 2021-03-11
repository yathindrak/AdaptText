import flask_praetorian
from flask import Blueprint, jsonify, request, make_response, abort
from flask_praetorian import auth_required
from sqlalchemy.exc import IntegrityError
import pandas as pd
import csv

from ..websocket.server import Server
from ..pipeline.adapt_text import AdaptText
from ..pipeline.evaluator.evaluator import Evaluator
from ..schemas.metainfo import MetaInfoSchema
from ..models.metainfo import MetaInfo
from ..schemas.task import TaskSchema
from ..models.user import User
from ..models.task import Task
from ..utils.http_utils import make_err_response
from ..connection.initializers import guard, database

from io import BytesIO
from flask import Flask, send_file
import numpy as np
from skimage.io import imsave
import matplotlib.pyplot as plt

task_routes = Blueprint('task', __name__)


@task_routes.route('/task/initiate', methods=['POST'])
@auth_required
def initiate():
    json_obj = request.get_json()
    if not json_obj:
        return make_err_response('Bad Request', 'No valid entries provided', 400)
    try:
        name = json_obj['name']
        description = json_obj['description']
        progress = 0
        model_path = None
        ds_path = json_obj['ds_path']
        ds_text_col = json_obj['ds_text_col']
        ds_label_col = json_obj['ds_label_col']
        continuous_train = json_obj['continuous_train']
        accuracy = None
        # task_id = id
    except:
        return make_err_response('Bad Request', 'No valid entries provided', 400)

    model_path = None
    current_user = User.lookup(flask_praetorian.current_user().username)

    get_task = Task(name=name, description=description, progress=progress, model_path=model_path,
                    user_id=current_user.id)

    try:
        database.session.add(get_task)
        database.session.commit()
    except IntegrityError:
        return make_err_response('Bad Request', 'Duplicated name entered', 400)

    meta_data = MetaInfo(ds_path=ds_path, ds_text_col=ds_text_col, ds_label_col=ds_label_col,
                         continuous_train=continuous_train, accuracy=accuracy, task_id=get_task.id)

    try:
        database.session.add(meta_data)
        database.session.commit()
    except IntegrityError:
        return make_err_response('Bad Request', 'Duplicated name entered', 400)

    meta_info_schema = MetaInfoSchema()
    meta_data = meta_info_schema.dump(meta_data)

    return make_response(jsonify({"meta_data": meta_data}), 201)


@task_routes.route('/task/upload', methods=['POST'])
@auth_required
def upload_csv():
    uploaded_file = request.files['filepond']

    if uploaded_file.filename != '':
        file_path = "resources/" + uploaded_file.filename
        uploaded_file.save(file_path)

        with open(file_path, encoding="utf8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            csv_column_names = []

            for row in csv_reader:
                # read only the first row
                csv_column_names.append(row)
                break

        return make_response(jsonify({"file_path": file_path, "column_names": csv_column_names[0]}), 201)

    else:
        return make_err_response('Bad Request', 'Invalid file provided', 400)


def update_progress(task_id, progress):
    database.session.query(Task).filter_by(id=task_id).update({"progress": progress})
    database.session.commit()


@task_routes.route('/task/execute/<id>', methods=['POST'])
@auth_required
def execute(id):
    if not id:
        return make_err_response('Bad Request', 'No id provided', 400)

    meta_info = MetaInfo.query.filter_by(task_id=id).first()
    model_path = None
    current_user = User.lookup(flask_praetorian.current_user().username)

    lang = 'si'
    app_root = "/storage"
    bs = 128
    splitting_ratio = 0.1
    adapt_text = AdaptText(lang, app_root, bs, splitting_ratio, continuous_train=meta_info.continuous_train)

    pd.set_option('display.max_colwidth', -1)
    # path_to_csv="sinhala-hate-speech-dataset.csv"
    path_to_csv = meta_info.ds_path
    df = pd.read_csv(path_to_csv)

    text_name = meta_info.ds_text_col
    label_name = meta_info.ds_label_col

    web_socket = Server()
    web_socket.publish(id, 1)
    update_progress(id, 1)

    print("Start building classification model")
    classifierModelFWD, classifierModelBWD, classes = adapt_text.build_classifier(df, text_name, label_name, id,
                                                                                  grad_unfreeze=False)

    evaluator = Evaluator()

    print("Ensemble classifier analysis")
    accuracy, err, xlim, ylim, fpr, tpr, roc_auc, conf_matrix, macro_f1, macro_precision, macro_recall, macro_support, \
    weighted_f1, weighted_precision, weighted_recall, weighted_support = evaluator.evaluate_ensemble(
        classifierModelFWD, classifierModelBWD)

    print('accuracy : ' + accuracy)
    print('err : ' + err)
    print('roc auc : ' + roc_auc)
    print(conf_matrix)

    database.session.query(MetaInfo).filter_by(task_id=id).update(
        {"accuracy": accuracy, "err": err, "xlim": xlim, "ylim": ylim, "fpr": fpr, "tpr": tpr, "roc_auc": roc_auc,
         "conf_matrix": conf_matrix, "macro_f1": macro_f1, "macro_precision": macro_precision, "macro_recall": macro_recall,
         "macro_support": macro_support, "weighted_f1": weighted_f1, "weighted_precision": weighted_precision,
         "weighted_recall": weighted_recall, "weighted_support": weighted_support})

    database.session.commit()

    # return make_response(jsonify({"accuracy": accuracy, "err": err}), 201)
    return make_response('', 204)

    # clear below part of this func

    # //////////////////////////////////////////////////////////

    # json_obj = request.get_json()
    # if not json_obj:
    #     return make_err_response('Bad Request', 'No valid entries provided', 400)
    # try:
    #     db_text_col = json_obj['db_text_col']
    #     db_label_col = json_obj['db_label_col']
    #     accuracy = json_obj["accuracy"]
    #     task_id = id
    # except:
    #     return make_err_response('Bad Request', 'No valid entries provided', 400)
    #
    # get_meta_data = MetaData(db_text_col=db_text_col, db_label_col=db_label_col, accuracy=accuracy, task_id=task_id)
    #
    # try:
    #     database.session.add(get_meta_data)
    #     database.session.commit()
    # except IntegrityError:
    #     return make_err_response('Bad Request', 'Duplicated name entered', 400)
    #
    # meta_data_schema = MetaDataSchema()
    # meta_data = meta_data_schema.dump(get_meta_data)
    #
    # return make_response(jsonify({"meta_data": meta_data}), 201)


# percentage = 0
# task_id = 0
# pusher_client.trigger('upload', 'progress',
#                       {
#                           'percentage': percentage,
#                           'task_id': task_id
#                       })


@task_routes.route('/task/<id>')
@auth_required
def get_by_id(id):
    get_task = Task.query.get(id)

    current_user = User.lookup(flask_praetorian.current_user().username)

    if get_task.user_id == current_user.id:
        return make_err_response('Not found', 'Task not found', 404)

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

@task_routes.route('/plot')
def generate_plot():
    """
    Return a matplotlib plot as a png by
    saving it into a StringIO and using send_file.
    """

    def using_matplotlib():
        fig = plt.figure(figsize=(6, 6), dpi=300)
        ax = fig.add_subplot(111)
        x = np.random.randn(500)
        y = np.random.randn(500)
        ax.plot(x, y, '.', color='r', markersize=10, alpha=0.2)
        ax.set_title('Behold')

        # strIO = StringIO()
        strIO = BytesIO()
        plt.savefig(strIO, dpi=fig.dpi)
        strIO.seek(0)
        return strIO

    strIO = using_matplotlib()
    # img = Image.open
    return send_file(strIO, mimetype='image/png')
