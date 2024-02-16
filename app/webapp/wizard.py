from flask import Blueprint
# import app
# from app.util import log
from .sct_page import sct

wizard = Blueprint('wizard', __name__)


@wizard.route('/', methods=['GET'])
def index():
    tasks = _get_tasks()
    return render_template('sct_table.html',  tasks=tasks)



