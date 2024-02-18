from flask import (Blueprint, render_template, request, redirect, url_for,
                   make_response)

import logging as log
from app.util.auth import authenticate, jwt_required

login_page = Blueprint('login_page', __name__)


@login_page.route('/', methods=['GET', 'POST'])
def login():

    error = None

    if request.method == 'GET':

        if request.args.get('error'):
            return render_template('login_page.html',
                                   error=request.args.get("error"))

        access_token = request.cookies.get('access_token_cookie')

        if access_token is None:
            return render_template('login_page.html', error=error)

        return redirect(url_for('repo_page.repo'))

    # POST form
    email = request.form.get('email')
    password = request.form.get('password')

    is_auth, data = authenticate(email, password)

    if not is_auth:
        return render_template("login_page.html", error=data)

    log.debug("make response..")

    response = make_response(redirect(url_for('repo_page.repo')))
    # set jwt cookie
    response.set_cookie('access_token_cookie', data)

    return response


@login_page.route('/logout', methods=['GET', 'POST'])
@jwt_required(True)
def logout():

    response = make_response(redirect(url_for('login_page.login')))
    response.set_cookie('access_token_cookie', '', expires=0)
    return response
