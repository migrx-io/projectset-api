from flask import Blueprint, jsonify
from app.util.auth import jwt_required

clstr = Blueprint('cluster', __name__)


@clstr.route('/cluster', methods=['GET'])
@jwt_required
def cluster_list():
    """
    file: ../apispec/cluster_list.yaml
    """

    cluster_lst = []

    return jsonify(cluster_lst), 200
