from functools import wraps
import os
import logging as log

from flask_jwt_extended import (verify_jwt_in_request, get_jwt_identity,
                                get_jwt, create_access_token)
from flask import request, jsonify, redirect, url_for
from werkzeug.datastructures import Headers
from app.util.ldapx import ldap_auth
import yaml
import re


def authenticate(username, password):

    ok, data = auth_call(username, password)

    log.info("auth_call: status: %s / text %s", ok, data)

    if not ok:
        return False, data

    # create access token
    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username,
                                       additional_claims=data)

    return True, access_token


def auth_call(email, password):

    log.debug("auth_call: email: %s / password %s", email, password)

    if email == "" and password == "":
        return False, "Invalid credentials"

    # if user admin - all perms
    if email == "admin" and password == os.environ.get("ADMIN_PASSWD", "") and \
            os.environ.get("ADMIN_DISABLE", "n") == "n":
        return True, {"session": ""}

    # Auth logic here

    ok, data = ldap_auth(email, password)

    log.info("ldap_auth: ok: %s, data: %s", ok, data)

    if not ok:
        return False, data

    return True, data


def check_spec(data, allow):

    log.info("check_spec: data: %s, allow: %s", data, allow)

    if allow is not None and allow != ["all"] and data is not None:
        log.info("allow: %s", allow)

        # check attributes
        for k in data.get("spec", {}).keys():
            log.info("spec attrs: %s not in allow: %s", k, allow)
            if k not in allow:
                return False, "Permission denied attr: {}, allow attribute: {}".format(k, allow)

    return True, None


def check_permissions(login, claims, req):

    # check user permission

    log.info("check_permissions: login: %s / claims: %s / req: %s", login,
             claims, req)

    log.info("check_permissions: path: %s, data: %s form: %s", req.path,
             req.data, req.form)

    ydata = req.form.get("data", None)
    if ydata is None:
        ydata = req.data.decode("utf-8")

    ydata = yaml.safe_load(ydata)

    log.info("received data: %s", ydata)

    roles = []
    with open(os.environ.get("APP_CONF", "app.yaml"), 'r',
              encoding="utf-8") as file:

        data = yaml.safe_load(file)

        log.debug("get_envs: data: %s", data)

        roles = data.get("roles", {})

    for g in claims["groups"]:

        verbs = roles.get(g, {})

        log.info("verbs: %s", verbs)

        for k, v in verbs.items():

            log.info("check verb: %s, %s", req.path, k)

            if re.search(r'{}'.format(k), req.path) is not None:
                log.info("data: %s", data)
                log.info("ydata: %s", ydata)

                log.info("data: g %s -> %s", g, k)
                allow = v

                return check_spec(ydata, allow)

    return False, "Permission denied"


def jwt_required(page=False):

    def jwt_required_root(fn):

        @wraps(fn)
        def wrapper(*args, **kwargs):

            # check APIKEY if exists
            api_key = request.headers.get('X-API-KEY')
            if api_key is not None:

                if api_key != os.environ.get("X_API_KEY"):
                    raise Exception("A valid API KEY is missing")

                return fn(*args, **kwargs)

            # verify JWT token
            try:

                cookie = request.cookies.get("access_token_cookie")
                if cookie is not None:
                    # Create a new headers object with additional headers
                    new_headers = Headers(request.headers)
                    new_headers.add("Authorization", f"JWT {cookie}")
                    request.headers = new_headers

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

                return fn(*args, **kwargs)

            except Exception as e:
                if page:
                    # return render_template("error_page.html", error=str(e))
                    return redirect(url_for('login_page.login', error=str(e)))
                raise e

        return wrapper

    return jwt_required_root
