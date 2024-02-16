from flask import Blueprint, render_template, request, redirect, url_for

login_page = Blueprint('login_page', __name__)


@login_page.route('/', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':

        if request.form['username'] != 'admin' or request.form[
                'password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'

        else:
            return redirect(url_for('home'))

    return render_template('login.html', error=error)
