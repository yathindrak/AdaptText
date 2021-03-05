from flask import make_response, jsonify


def make_err_response(err: str, message: str, status_code):
    return make_response(jsonify({'error': err, 'message': message, 'status_code': status_code}), status_code)