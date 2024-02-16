from flask import Blueprint, render_template, request
# import app
# from app.util import log
from app.crds.ps import get_ps
from app.crds.ps import create as create_ps
from app.crds.ps import delete as delete_ps

ps_page = Blueprint('ps_page', __name__)


@ps_page.route('/', methods=['GET'])
def ps():
    ps_list = get_ps()
    return render_template('ps_table.html', ps=ps_list)


@ps_page.route('/create_ps', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':

        # name = request.form.get('name', "x")

        try:
            create_ps()

        except Exception as e:
            return {"error": str(e)}
        # pass
        return {"status": "ok"}

    return render_template('ps_create.html')


@ps_page.route('/delete_ps', methods=['GET', 'POST'])
def delete():

    if request.method == 'POST':

        # name = request.form.get('name', "x")

        try:
            delete_ps()

        except Exception as e:
            return {"error": str(e)}
        # pass
        return {"status": "ok"}

    return render_template('ps_delete.html')
