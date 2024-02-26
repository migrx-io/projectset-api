from flask import Blueprint, jsonify, request
from app.util.auth import jwt_required
from app.crds.projectsets import get_projectset, create_projectset, delete_projectset, update_projectset

projectset_api = Blueprint('projectset_api', __name__)


@projectset_api.route('/projectset', methods=['GET'])
@jwt_required(False)
def projectset():
    """
    file: ../apispec/projectset_list.yaml
    """

    projectset_list = get_projectset()

    return jsonify(projectset_list), 200


@projectset_api.route('/projectset', methods=['POST'])
@jwt_required(False)
def projectset_create():
    """
    file: ../apispec/projectset_create.yaml
    """

    projectset_list = create_projectset(repo, name, data)

    return jsonify(projectset_list), 200


@projectset_api.route('/projectset/<uid>', methods=['PUT'])
@jwt_required(False)
def projectset_update(uid):
    """
    file: ../apispec/projectset_update.yaml
    """

    data = request.data

    projectset_list = update_projectset(uid, data)

    return jsonify("ok"), 200


@projectset_api.route('/projectset/<uid>', methods=['DELETE'])
@jwt_required(False)
def projectset_delete(uid):
    """
    file: ../apispec/projectset_delete.yaml
    """

    delete_projectset(uid)

    return jsonify("ok"), 200
