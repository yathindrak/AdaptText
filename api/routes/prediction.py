from pathlib import Path

import flask_praetorian
from flask import Blueprint, make_response, jsonify
from flask_praetorian import auth_required

from ..pipeline.fastai1.basic_train import load_learner
from ..pipeline.predictor.predictor import Predictor
from ..pipeline.utils.dropbox_handler import DropboxHandler
from ..pipeline.utils.zip_handler import ZipHandler
from ..models.metainfo import MetaInfo
from ..models.user import User
from ..models.task import Task
from ..utils.http_utils import make_err_response

prediction_routes = Blueprint('prediction', __name__)


@prediction_routes.route('/prediction/<id>')
@auth_required
def load_classifier(id):
    get_task = Task.query.get(id)

    current_user = User.lookup(flask_praetorian.current_user().username)

    if get_task.user_id != current_user.id:
        return make_err_response('Not found', 'Model not found', 404)

    model_path = get_task.model_path

    model_file_name = model_path.split("/")[-1]
    classifier_root = "/classification/"

    if Path(classifier_root + model_file_name).exists():
        return make_response('model already exists', 200)

    print("classification model {} not found locally; try downloading...", model_file_name)

    dropbox_handler = DropboxHandler(classifier_root)
    destination = classifier_root + model_file_name
    dropbox_handler.download_clasifier_model(model_file_name, destination)

    # unzip
    zipHandler = ZipHandler()
    zipHandler.unzip(destination, destination=classifier_root)

    return make_response('model downloaded', 201)


@prediction_routes.route('/predict/<task_id>/<text>')
@auth_required
def predict(task_id, text):
    get_task = Task.query.get(task_id)

    current_user = User.lookup(flask_praetorian.current_user().username)

    if get_task.user_id != current_user.id:
        return make_err_response('Not found', 'Model not found', 404)

    meta_info = MetaInfo.query.filter_by(task_id=task_id).first()

    classifier_dir = "/classification/models/"
    classifiers_store_path = ["fwd-export", "bwd-export", "ensemble-export"]

    learn_classifier_fwd = load_learner(classifier_dir, classifiers_store_path[0] + str(get_task.id) + ".pkl")
    learn_classifier_bwd = load_learner(classifier_dir, classifiers_store_path[1] + str(get_task.id) + ".pkl")
    learn_classifier_ensemble = load_learner(classifier_dir, classifiers_store_path[2] + str(get_task.id) + ".pkl")

    predictor = Predictor(learn_classifier_fwd, learn_classifier_bwd, learn_classifier_ensemble, meta_info.classes)

    prediction = predictor.predict(text)

    return jsonify({'predicted_label': prediction}), 200
