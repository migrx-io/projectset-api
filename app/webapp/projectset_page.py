from flask import Blueprint, render_template
# import app
# from app.util import log
from app.crds.projectsets import get_projectset

projectset_page = Blueprint('projectset_page', __name__)


@projectset_page.route('/', methods=['GET'])
def projectset():
    projectset_list = get_projectset()
    return render_template('projectset_page.html',
                           projectset_list=projectset_list)


@projectset_page.route('/create', methods=['GET', 'POST'])
def create():
    pass


