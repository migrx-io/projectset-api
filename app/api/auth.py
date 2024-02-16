from flask import Blueprint, request, jsonify
from flask_jwt_extended import (create_access_token)
import logging as log
from app.util.auth import authenticate
from app.util.types import AuthCodes

auth = Blueprint('auth', __name__)


@auth.route('/auth', methods=['POST'])
def authz():
    """
    file: ../apispec/authz.yaml
    """
    data = request.get_json()

    log.debug("raw request: %s", data)

    username = data.get('username')
    password = data.get('password')

    user_data = {
        "user-agent": request.headers.get('user-agent'),
        "user-ip": request.remote_addr,
    }

    log.debug("user_data: %s", user_data)

    is_auth, auth_data = authenticate(username, password, user_data)

    log.debug("is_auth: %s / auth_data: %s", is_auth, auth_data)

    resp_code = 200

    if is_auth == AuthCodes.NO:
        return jsonify({"error": auth_data}), 500

    if is_auth == AuthCodes.YES:
        resp_code = 200

    additional_claims = {
        "login": username,
    }

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username,
                                       additional_claims=additional_claims)

    return jsonify(access_token=access_token, ), resp_code
