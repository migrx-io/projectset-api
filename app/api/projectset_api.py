from flask import Blueprint, jsonify, request
from app.util.auth import jwt_required
from app.crds.projectsets import (get_projectset, create_projectset,
                                  delete_projectset, update_projectset)

projectset_api = Blueprint('projectset_api', __name__)


@projectset_api.route('/projectset', methods=['GET'])
@jwt_required(False)
def projectset():
    """
    file: ../apispec/projectset_list.yaml
    """

    projectset_list = get_projectset("projectset")

    return jsonify(projectset_list), 200


@projectset_api.route('/projectset', methods=['POST'])
@jwt_required(False)
def projectset_create():
    """
    file: ../apispec/projectset_create.yaml
    """

    data = request.get_json()

    create_projectset("projectset", data.get("repo"), data.get("name"),
                      data.get("data"), [])

    return jsonify("ok"), 200


@projectset_api.route('/projectset/<uid>', methods=['PUT'])
@jwt_required(False)
def projectset_update(uid):
    """
    file: ../apispec/projectset_update.yaml
    """

    data = request.data.decode("utf-8")

    update_projectset("projectset", uid, data)

    return jsonify("ok"), 200


@projectset_api.route('/projectset/<uid>', methods=['DELETE'])
@jwt_required(False)
def projectset_delete(uid):
    """
    file: ../apispec/projectset_delete.yaml
    """

    delete_projectset("projectset", uid)

    return jsonify("ok"), 200


@projectset_api.route('/projectsettemplate', methods=['GET'])
@jwt_required(False)
def projectsettemplate():
    """
    file: ../apispec/projectsettemplate_list.yaml
    """

    projectset_list = get_projectset("projectset_template")

    return jsonify(projectset_list), 200


@projectset_api.route('/projectsettemplate', methods=['POST'])
@jwt_required(False)
def projectsettemplate_create():
    """
    file: ../apispec/projectsettemplate_create.yaml
    """

    data = request.get_json()

    create_projectset("projectset_template", data.get("repo"),
                      data.get("name"), data.get("data"), [])

    return jsonify("ok"), 200


@projectset_api.route('/projectsettemplate/<uid>', methods=['PUT'])
@jwt_required(False)
def projectsettemplate_update(uid):
    """
    file: ../apispec/projectsettemplate_update.yaml
    """

    data = request.data.decode("utf-8")

    update_projectset("projectset_template", uid, data)

    return jsonify("ok"), 200


@projectset_api.route('/projectsettemplate/<uid>', methods=['DELETE'])
@jwt_required(False)
def projectsettemplate_delete(uid):
    """
    file: ../apispec/projectsettemplate_delete.yaml
    """

    delete_projectset("projectset_template", uid)

    return jsonify("ok"), 200
