from flask import Blueprint, jsonify, request
from flask_praetorian import auth_required

from ..utils.http_utils import make_err_response
from ..connection.initializers import guard

api = Blueprint('auth', __name__)


@api.route('/login', methods=['POST'])
def login():
    json_obj = request.get_json()
    if not json_obj:
        return make_err_response('Bad Request', 'No credentials provided', 400)
    user_name = json_obj['username']
    password = json_obj['password']

    user = guard.authenticate(user_name, password)
    token = guard.encode_jwt_token(user)

    return jsonify({'access_token': token}), 200


@api.route('/protected')
@auth_required
def protected():
    return jsonify({'result': 'You are in a special area!'}), 200


@api.route('/refresh', methods=['POST'])
def refresh():
    json_data = request.get_json()

    if not json_data:
        return make_err_response('Bad Request', 'Token not found', 400)

    prev_token = json_data['token']
    if not prev_token:
        return make_err_response('Bad Request', 'Token not found', 400)

    token = guard.refresh_jwt_token(prev_token)
    return jsonify({'access_token': token})
