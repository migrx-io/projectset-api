from flask import Blueprint, request, jsonify
import logging as log
from app.util.auth import authenticate

auth_api = Blueprint('auth_api', __name__)


@auth_api.route('/auth', methods=['POST'])
def authz():
    """
    file: ../apispec/authz.yaml
    """
    data = request.get_json()

    log.debug("raw request: %s", data)

    username = data.get('username')
    password = data.get('password')

    is_auth, data = authenticate(username, password)

    log.debug("is_auth: %s / err: %s", is_auth, data)

    if not is_auth:
        return jsonify({"error": data}), 500

    return jsonify(access_token=data, ), 200
