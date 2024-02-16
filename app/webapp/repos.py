from flask import Blueprint, render_template
from app.crds.repos import get_envs

repoz = Blueprint('repoz', __name__)


@repoz.route('/', methods=['GET'])
def index():
    repos = get_envs()
    return render_template('repos.html', repos=repos)
