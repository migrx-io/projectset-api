import logging as log
from flask import Blueprint, render_template, request
from app.util.auth import jwt_required
from app.crds.projectsets import get_projectset, create_projectset

projectset_page = Blueprint('projectset_page', __name__)


@projectset_page.route('/', methods=['GET'])
@jwt_required(True)
def projectset():
    projectset_list = get_projectset()

    return render_template('projectset_page.html',
                           jsonschema={"type": "boolean"},
                           projectset_list=projectset_list)


@projectset_page.route('/create', methods=['GET', 'POST'])
@jwt_required(True)
def create():

    if request.method == 'POST':

        data = request.form.get('data')

        log.debug("create: data: %s", data)

        try:
            create_projectset(data)

        except Exception as e:
            return {"error": str(e)}
        # pass
        return {"status": "ok"}

    return render_template('modal_form_page.html')


@projectset_page.route('/edit', methods=['GET', 'POST'])
@jwt_required(True)
def edit():

    if request.method == 'POST':

        data = request.form.get('data')

        log.debug("create: data: %s", data)

        try:
            pass
        except Exception as e:
            return {"error": str(e)}
        # pass
        return {"status": "ok"}

    return render_template('modal_form_page.html')


@projectset_page.route('/delete', methods=['GET', 'POST'])
@jwt_required(True)
def delete():
    pass
