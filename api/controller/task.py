import os

import flask_praetorian
from flask import Blueprint, jsonify, request, make_response, abort, Response
from flask_praetorian import auth_required
from sqlalchemy.exc import IntegrityError
import pandas as pd
import csv

from ..utils.logger import Logger
from ..websocket.pusher_publisher import PusherPublisher
from ..pipeline.adapt_text import AdaptText
from ..pipeline.evaluator.evaluator import Evaluator
from ..schemas.metainfo import MetaInfoSchema
from ..models.metainfo import MetaInfo
from ..schemas.task import TaskSchema
from ..models.user import User
from ..models.task import Task
from ..connection.initializers import database

task_controller = Blueprint('task', __name__)


@task_controller.route('/task', methods=['POST'])
@auth_required
def create():
    logger = Logger()
    logger.info('Initiating task...')
    json_obj = request.get_json()
    if not json_obj:
        return make_response(
            jsonify({'error': 'Bad Request', 'message': 'No valid entries provided', 'status_code': 400}), 400)
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
        logger.info('No valid entries provided')
        return make_response(
            jsonify({'error': 'Bad Request', 'message': 'No valid entries provided', 'status_code': 400}), 400)

    model_path = None
    current_user = User.lookup(flask_praetorian.current_user().username)

    get_task = Task(name=name, description=description, progress=progress, model_path=model_path,
                    user_id=current_user.id)

    try:
        database.session.add(get_task)
        database.session.commit()
    except IntegrityError:
        return make_response(
            jsonify({'error': 'Bad Request', 'message': 'Duplicated name entered', 'status_code': 400}), 400)

    meta_data = MetaInfo(ds_path=ds_path, ds_text_col=ds_text_col, ds_label_col=ds_label_col,
                         continuous_train=continuous_train, accuracy=accuracy,
                         task_id=get_task.id)

    try:
        database.session.add(meta_data)
        database.session.commit()
    except IntegrityError:
        return make_response(
            jsonify({'error': 'Bad Request', 'message': 'Duplicated name entered', 'status_code': 400}), 400)

    meta_info_schema = MetaInfoSchema()
    meta_data = meta_info_schema.dump(meta_data)

    logger.info('Completed initiating the task' + str(get_task.id))

    return make_response(jsonify({"meta_data": meta_data}), 201)


@task_controller.route('/task/upload', methods=['POST'])
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
        return make_response(
            jsonify({'error': 'Bad Request', 'message': 'Invalid file provided', 'status_code': 400}), 400)


def update_progress(task_id, progress):
    logger = Logger()
    logger.info('Progress updated for the task ' + str(task_id) + ' with progress of ' + str(progress))
    database.session.query(Task).filter_by(id=task_id).update({"progress": progress})
    database.session.commit()


@task_controller.route('/task/execute/<id>', methods=['POST'])
@auth_required
def execute(id):
    if not id:
        return make_response(
            jsonify({'error': 'Bad Request', 'message': 'No id provided', 'status_code': 400}), 400)

    meta_info = MetaInfo.query.filter_by(task_id=id).first()
    model_path = None

    logger = Logger()
    logger.info('Start execution of the task ' + str(id))

    lang = 'si'
    app_root = "/storage"
    bs = 128
    splitting_ratio = 0.1
    adapt_text = AdaptText(lang, app_root, bs, splitting_ratio, continuous_train=meta_info.continuous_train)

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

    web_socket = PusherPublisher()
    web_socket.publish_classifier_progress(id, 1)
    update_progress(id, 1)

    logger.info('Start building classification model')
    classifierModelFWD, classifierModelBWD, learn_ensemble, classes = adapt_text.build_classifier(df, text_name, label_name, id,
                                                                                  grad_unfreeze=False)

    evaluator = Evaluator()

    logger.info('Ensemble classifier analysis')

    metrics_dict = evaluator.evaluate(learn_ensemble)

    web_socket.publish_classifier_progress(id, 96)
    update_progress(id, 96)

    logger.info('Start updating metrics under Metainfo')

    try:
        meta_info = MetaInfo.query.filter_by(task_id=id).first()
        setattr(meta_info, 'accuracy', metrics_dict['acc'])
        setattr(meta_info, 'err', metrics_dict['err'])
        setattr(meta_info, 'classes', classes)
        setattr(meta_info, 'xlim', metrics_dict['xlim'])
        setattr(meta_info, 'ylim', metrics_dict['ylim'])
        setattr(meta_info, 'fpr', metrics_dict['fpr'])
        setattr(meta_info, 'tpr', metrics_dict['tpr'])
        setattr(meta_info, 'roc_auc', metrics_dict['roc_auc'])
        setattr(meta_info, 'conf_matrix', metrics_dict['conf_matrix_fig_url'])
        setattr(meta_info, 'roc_curve', metrics_dict['roc_curve_fig_url'])
        setattr(meta_info, 'macro_f1', metrics_dict['macro_f1'])
        setattr(meta_info, 'macro_precision', metrics_dict['macro_precision'])
        setattr(meta_info, 'macro_recall', metrics_dict['macro_recall'])
        setattr(meta_info, 'macro_support', metrics_dict['macro_support'])
        setattr(meta_info, 'weighted_f1', metrics_dict['weighted_f1'])
        setattr(meta_info, 'weighted_precision', metrics_dict['weighted_precision'])
        setattr(meta_info, 'weighted_recall', metrics_dict['weighted_recall'])
        setattr(meta_info, 'weighted_support', metrics_dict['weighted_support'])
        setattr(meta_info, 'matthews_corr_coef', metrics_dict['matthews_corr_coef'])

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


@task_controller.route('/task/<id>')
@auth_required
def get_by_id(id):
    get_task = Task.query.get(id)

    current_user = User.lookup(flask_praetorian.current_user().username)

    if get_task.user_id != current_user.id:
        return make_response(
            jsonify({'error': 'Bad Request', 'message': 'Task not found', 'status_code': 404}), 404)

    task_schema = TaskSchema()
    task = task_schema.dump(get_task)
    return make_response(jsonify({"task": task}))


@task_controller.route('/retrain', methods=['POST'])
@auth_required
def retrain_base_lm():
    logger = Logger()
    logger.info('Retraining the Pretrained Model')

    lang = 'si'
    app_root = "/storage"
    bs = 128
    splitting_ratio = 0.1
    adapt_text = AdaptText(lang, app_root, bs, splitting_ratio)

    web_socket = PusherPublisher()
    web_socket.publish_lm_progress(1)

    adapt_text.build_base_lm()

    web_socket = PusherPublisher()
    web_socket.publish_lm_progress(100)

    return make_response('', 204)


@task_controller.route('/tasks')
@auth_required
def get_all():
    """
    Get all tasks for a particular user
    :return: list of tasks
    :rtype: list
    """
    current_user = flask_praetorian.current_user().id

    get_tasks = Task.query.filter_by(user_id=current_user).all()

    task_schema = TaskSchema(many=True)
    tasks = task_schema.dump(get_tasks)

    return make_response(jsonify({"tasks": tasks}), 200)

