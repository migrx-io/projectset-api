from flask import (Blueprint, render_template, request, redirect, url_for,
                   make_response)

from flask_jwt_extended import get_jwt, verify_jwt_in_request, decode_token
import yaml

import logging as log
import os
from app.util.auth import authenticate, jwt_required

login_page = Blueprint('login_page', __name__)


@login_page.route('/', methods=['GET', 'POST'])
def login():

    def is_only_chat(claims):

        log.debug("is_only_chat: %s", claims)
        chat_only = ""
        with open(os.environ.get("APP_CONF", "app.yaml"),
                  'r',
                  encoding="utf-8") as file:

            data = yaml.safe_load(file)

            chat_only = data.get("chat_only", "")

        if chat_only in claims.get("groups", []):
            return True

        return False

    error = None

    if request.method == 'GET':

        if request.args.get('error'):
            return render_template('login_page.html',
                                   error=request.args.get("error"))

        access_token = request.cookies.get('access_token_cookie')

        if access_token is None:
            return render_template('login_page.html', error=error)

        verify_jwt_in_request()
        if is_only_chat(get_jwt()):
            return redirect(url_for('chat_page.chat'))

        return redirect(url_for('repo_page.repo'))

    # POST form
    email = request.form.get('email')
    password = request.form.get('password')

    is_auth, data = authenticate(email, password)

    if not is_auth:
        return render_template("login_page.html", error=data)

    log.debug("make response..")

    if is_only_chat(decode_token(data)):
        response = make_response(redirect(url_for('chat_page.chat')))
    else:
        response = make_response(
            redirect(url_for('projectset_page.projectset')))

    # set jwt cookie
    response.set_cookie('access_token_cookie', data)

    return response


@login_page.route('/logout', methods=['GET', 'POST'])
@jwt_required(True)
def logout():

    response = make_response(redirect(url_for('login_page.login')))
    response.set_cookie('access_token_cookie', '', expires=0)
    return response
