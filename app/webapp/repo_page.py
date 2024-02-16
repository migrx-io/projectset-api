from flask import Blueprint, render_template
from app.crds.repos import get_envs

repo_page = Blueprint('repo_page', __name__)


@repo_page.route('/', methods=['GET'])
def repo():
    repos = get_envs()
    return render_template('repos.html', repos=repos)
