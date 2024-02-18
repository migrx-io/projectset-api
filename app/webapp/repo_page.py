from flask import Blueprint, render_template
from app.crds.repos import get_envs
from app.util.auth import jwt_required

repo_page = Blueprint('repo_page', __name__)


@repo_page.route('/', methods=['GET'])
@jwt_required(True)
def repo():
    env_list = get_envs()
    return render_template('repo_page.html', env_list=env_list)
