from flask import Blueprint, jsonify
from app.util.auth import jwt_required
from app.crds.projectsets import get_projectset

projectset_api = Blueprint('projectset_api', __name__)


@projectset_api.route('/projectset', methods=['GET'])
@jwt_required
def projectset():
    """
    file: ../apispec/projectset_list.yaml
    """

    projectset_list = get_projectset()

    return jsonify(projectset_list), 200
