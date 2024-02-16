from functools import wraps
import os
import logging as log

from flask_jwt_extended import (verify_jwt_in_request, get_jwt_identity,
                                get_jwt)
from flask import request, jsonify
from app.util.types import AuthCodes


def authenticate(username, password, user_data):

    # if user admin - all perms
    if username == "admin" and password == os.environ["ADMIN_PASSWD"] and \
            os.environ.get("ADMIN_DISABLE", "n") == "n":
        return AuthCodes.YES, {"session": ""}

    status, data = auth_call(username, password, user_data)

    log.debug("auth_call: status: %s / text %s", status, data)

    if status != 200:
        log.error(data)
        return AuthCodes.NO, data

    return AuthCodes.YES, data


def auth_call(login, password, user_data):

    log.debug("auth_call: login: %s / password %s / data: %s", login, password,
              user_data)

    # Auth logic here
    status, data = 200, {"session": ""}

    return status, data


def check_permissions(login, claims, req):

    # check user permission

    log.debug("check_permissions: login: %s / claims: %s / req: %s", login,
              claims, req)

    # retunr False, data

    return True, "ok"


def jwt_required(fn):

    @wraps(fn)
    def wrapper(*args, **kwargs):

        # check APIKEY if exists

        api_key = request.headers.get('X-API-KEY')
        if api_key is not None:

            if api_key != os.environ.get("X_API_KEY"):
                raise Exception("A valid API KEY is missing")

            return fn(*args, **kwargs)

        # verify JWT token

        verify_jwt_in_request()

        login = get_jwt_identity()
        claims = get_jwt()

        is_checked, data = check_permissions(login, claims, request)

        if login == "admin" and os.environ["ADMIN_DISABLE"] == "n":
            return fn(*args, **kwargs)

        if not is_checked:
            return jsonify(error=data), 403

        # add context perm to func
        log.debug("kwargs data: %s", data)

        response, code = fn(*args, **kwargs)

        return response, code

    return wrapper
