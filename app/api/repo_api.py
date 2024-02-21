import logging as log
from flask import Blueprint, jsonify
from app.util.auth import jwt_required
from app.crds.repos import get_envs

repo_api = Blueprint('repo_api', __name__)


@repo_api.route('/repo', methods=['GET'])
@jwt_required(False)
def repo():
    """
    file: ../apispec/repo_list.yaml
    """

    env_list = get_envs()

    log.debug("env_list: %s", env_list)

    return jsonify(env_list), 200
