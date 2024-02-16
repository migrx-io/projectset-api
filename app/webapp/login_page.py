from flask import (Blueprint, render_template, request, 
                   redirect, url_for, make_response)

import logging as log

login_page = Blueprint('login_page', __name__)


@login_page.route('/', methods=['GET', 'POST'])
def login():

    error = None

    if request.method=='GET':

        access_token = request.cookies.get('access_token')

        if access_token is None:
            return render_template('login.html', error=error)
        else:
            return redirect(url_for('repo_page.repo'))

    else:
        email = request.form.get('email')
        password = request.form.get('password')

        if email=="" and password=="":
            error = 'Invalid Credentials. Please try again.'
            return render_template("login.html", error=error)

        log.debug("make response..")

        response = make_response(render_template('repos.html'))
        # set jwt cookie
        response.set_cookie('access_token', 'super')

        return response

        # return redirect(url_for('repo_page.repo'))

@login_page.route('/logout', methods=['GET', 'POST'])
def logout():

    # clear cookie

    if request.method=='GET':
        return redirect(url_for('login_page.login'))

    response = make_response(render_template('login.html'))
    response.set_cookie('access_token', '', expires=0)
    return response
