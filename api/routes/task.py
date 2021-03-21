import os

import flask_praetorian
from flask import Blueprint, jsonify, request, make_response, abort, Response
from flask_praetorian import auth_required
from sqlalchemy.exc import IntegrityError
import pandas as pd
import csv

from ..utils.logger import Logger
from ..websocket.server import Server
from ..pipeline.adapt_text import AdaptText
from ..pipeline.evaluator.evaluator import Evaluator
from ..schemas.metainfo import MetaInfoSchema
from ..models.metainfo import MetaInfo
from ..schemas.task import TaskSchema
from ..models.user import User
from ..models.task import Task
from ..utils.http_utils import make_err_response
from ..connection.initializers import database

task_routes = Blueprint('task', __name__)


@task_routes.route('/task/initiate', methods=['POST'])
@auth_required
def initiate():
    logger = Logger()
    logger.info('Initiating task...')
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
        is_imbalanced = json_obj['is_imbalanced']
        accuracy = None
        # task_id = id
    except:
        logger.info('No valid entries provided')
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
                         continuous_train=continuous_train, is_imbalanced=is_imbalanced, accuracy=accuracy,
                         task_id=get_task.id)

    try:
        database.session.add(meta_data)
        database.session.commit()
    except IntegrityError:
        return make_err_response('Bad Request', 'Duplicated name entered', 400)

    meta_info_schema = MetaInfoSchema()
    meta_data = meta_info_schema.dump(meta_data)

    logger.info('Completed initiating the task' + str(get_task.id))

    return make_response(jsonify({"meta_data": meta_data}), 201)


@task_routes.route('/task/upload', methods=['POST'])
@auth_required
def upload_csv():
    logger = Logger()
    logger.info('Uploading csv file...')
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

        logger.info('Completed uploading csv file...')

        return make_response(jsonify({"file_path": file_path, "column_names": csv_column_names[0]}), 201)

    else:
        return make_err_response('Bad Request', 'Invalid file provided', 400)


def update_progress(task_id, progress):
    logger = Logger()
    logger.info('Progress updated for the task ' + str(task_id) + ' with progress of ' + str(progress))
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

    logger = Logger()
    logger.info('Start execution of the task ' + str(id))

    lang = 'si'
    app_root = "/storage"
    bs = 128
    splitting_ratio = 0.1
    adapt_text = AdaptText(lang, app_root, bs, splitting_ratio, continuous_train=meta_info.continuous_train,
                           is_imbalanced=meta_info.is_imbalanced)

    pd.set_option('display.max_colwidth', -1)
    # path_to_csv="sinhala-hate-speech-dataset.csv"
    path_to_csv = meta_info.ds_path

    df = None
    df_comma_separated = pd.read_csv(path_to_csv, nrows=1, sep=",")
    df_semi_colon_separated = pd.read_csv(path_to_csv, nrows=1, sep=";")

    if df_comma_separated.shape[1] < df_semi_colon_separated.shape[1]:
        df = pd.read_csv(path_to_csv, sep=";")
    else:
        df = pd.read_csv(path_to_csv)

    text_name = meta_info.ds_text_col
    label_name = meta_info.ds_label_col

    web_socket = Server()
    web_socket.publish_classifier_progress(id, 1)
    update_progress(id, 1)

    logger.info('Start building classification model')
    classifierModelFWD, classifierModelBWD, classes = adapt_text.build_classifier(df, text_name, label_name, id,
                                                                                  grad_unfreeze=False)

    evaluator = Evaluator()

    logger.info('Ensemble classifier analysis')
    accuracy, err, xlim, ylim, fpr, tpr, roc_auc, macro_f1, macro_precision, macro_recall, macro_support, \
    weighted_f1, weighted_precision, weighted_recall, weighted_support, matthews_corr_coef, conf_matrix_fig_url, roc_curve_fig_url = evaluator.evaluate_ensemble(
        classifierModelFWD, classifierModelBWD)

    web_socket.publish_classifier_progress(id, 96)
    update_progress(id, 96)

    logger.info('Start updating metrics under Metainfo')

    try:
        meta_info = MetaInfo.query.filter_by(task_id=id).first()
        # setattr(meta_info, 'ds_path', 'aassdaasd')
        setattr(meta_info, 'accuracy', accuracy.item())
        setattr(meta_info, 'err', err.item())
        setattr(meta_info, 'classes', classes)
        setattr(meta_info, 'xlim', xlim)
        setattr(meta_info, 'ylim', ylim)
        setattr(meta_info, 'fpr', fpr.tolist())
        setattr(meta_info, 'tpr', tpr.tolist())
        setattr(meta_info, 'roc_auc', roc_auc.item())
        setattr(meta_info, 'conf_matrix', conf_matrix_fig_url)
        setattr(meta_info, 'roc_curve', roc_curve_fig_url)
        setattr(meta_info, 'macro_f1', macro_f1)
        setattr(meta_info, 'macro_precision', macro_precision)
        setattr(meta_info, 'macro_recall', macro_recall)
        setattr(meta_info, 'macro_support', macro_support)
        setattr(meta_info, 'weighted_f1', weighted_f1)
        setattr(meta_info, 'weighted_precision', weighted_precision)
        setattr(meta_info, 'weighted_recall', weighted_recall)
        setattr(meta_info, 'weighted_support', weighted_support)
        setattr(meta_info, 'matthews_corr_coef', matthews_corr_coef)

        meta_info = database.session.merge(meta_info)
        database.session.commit()
    except Exception as e:
        print(e)
    finally:
        database.session.close()

    logger.info('Commiting updating metrics under Metainfo')

    web_socket.publish_classifier_progress(id, 100)
    update_progress(id, 100)

    logger.info('Done updating metrics under Metainfo')

    return make_response('', 204)


@task_routes.route('/task/<id>')
@auth_required
def get_by_id(id):
    get_task = Task.query.get(id)

    current_user = User.lookup(flask_praetorian.current_user().username)

    if get_task.user_id != current_user.id:
        return make_err_response('Not found', 'Task not found', 404)

    task_schema = TaskSchema()
    task = task_schema.dump(get_task)
    return make_response(jsonify({"task": task}))


@task_routes.route('/retrain', methods=['POST'])
@auth_required
def retrain_base_lm():
    logger = Logger()
    logger.info('Retraining the Pretrained Model')

    lang = 'si'
    app_root = "/storage"
    bs = 128
    splitting_ratio = 0.1
    adapt_text = AdaptText(lang, app_root, bs, splitting_ratio)

    web_socket = Server()
    web_socket.publish_lm_progress(1)

    adapt_text.build_base_lm()

    web_socket = Server()
    web_socket.publish_lm_progress(100)

    return make_response('', 204)


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

# @task_routes.route('/plot_roc/<id>')
# def plot_roc(id):
#     meta_info = MetaInfo.query.filter_by(task_id=id).first()
#
#     evaluator = Evaluator()
#     roc_figure = evaluator.draw_roc_curve(meta_info.xlim, meta_info.ylim, meta_info.fpr, meta_info.tpr, meta_info.roc_auc)
#     bytes = BytesIO()
#     plt.savefig(bytes, dpi=roc_figure.dpi)
#     bytes.seek(0)
#
#     return send_file(bytes, mimetype='image/png')
