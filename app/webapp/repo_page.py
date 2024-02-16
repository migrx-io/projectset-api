from flask import Blueprint, render_template
from app.crds.repos import get_envs

repo_page = Blueprint('repoz', __name__)


@repo_page.route('/', methods=['GET'])
def index():
    repos = get_envs()
    return render_template('repos.html', repos=repos)
