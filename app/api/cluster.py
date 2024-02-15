from flask import Blueprint, request, jsonify
from app.util.auth import token_required, jwt_required
from app.util.exec import run_shell

clstr = Blueprint('cluster', __name__)


@clstr.route('/cluster', methods=['GET'])
@jwt_required
def cluster_list():
    """
    file: ../apispec/cluster_list.yaml
    """

    cluster_lst = []

    return jsonify(cluster_lst), 200
