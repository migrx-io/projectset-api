import logging as log
from flask import Blueprint, render_template, request
from app.util.auth import jwt_required
from app.crds.projectsets import get_projectset, create_projectset

projectset_page = Blueprint('projectset_page', __name__)


@projectset_page.route('/', methods=['GET'])
@jwt_required(True)
def projectset():
    projectset_list = get_projectset()


    jsonschema = {
                  "$schema": "http://json-schema.org/draft-03/schema#",
                  "type": "object",
                  "properties": {

                                "namespace": {
                                    "description": "Namespace name",
                                    "type": "string"
                                },
                                "annotations": {
                                    "additionalProperties": {
                                    "type": "string"
                                    },
                                    "description": "Custom namespace annotations",
                                    "type": "object"
                                },

                                "labels": {
                                    "additionalProperties": {
                                    "type": "string"
                                    },
                                    "description": "Custom namespace labels",
                                    "type": "object"
                                },

                                "groupPermissions": {
                                    "additionalProperties": {
                                    "items": {
                                        "properties": {
                                        "apiGroup": {
                                            "type": "string"
                                        },
                                        "kind": {
                                            "type": "string"
                                        },
                                        "name": {
                                            "type": "string"
                                        },
                                        "namespace": {
                                            "type": "string"
                                        }
                                        },
                                        "required": [
                                        "kind",
                                        "name"
                                        ],
                                        "type": "object",
                                    },
                                    "type": "array"
                                    },
                                    "description": "User permissions",
                                    "type": "object"
                                },

                                "limitRange": {
                                    "properties": {
                                    "limits": {
                                        "items": {
                                        "properties": {
                                            "default": {
                                            "additionalProperties": {
                                                "anyOf": [
                                                {
                                                    "type": "integer"
                                                },
                                                {
                                                    "type": "string"
                                                }
                                                ],
                                            },
                                            "type": "object"
                                            },
                                            "defaultRequest": {
                                            "additionalProperties": {
                                                "anyOf": [
                                                {
                                                    "type": "integer"
                                                },
                                                {
                                                    "type": "string"
                                                }
                                                ],
                                            },
                                            "type": "object"
                                            },
                                            "max": {
                                            "additionalProperties": {
                                                "anyOf": [
                                                {
                                                    "type": "integer"
                                                },
                                                {
                                                    "type": "string"
                                                }
                                                ],
                                            },
                                            "type": "object"
                                            },
                                            "maxLimitRequestRatio": {
                                            "additionalProperties": {
                                                "anyOf": [
                                                {
                                                    "type": "integer"
                                                },
                                                {
                                                    "type": "string"
                                                }
                                                ],
                                            },
                                            "type": "object"
                                            },
                                            "min": {
                                            "additionalProperties": {
                                                "anyOf": [
                                                {
                                                    "type": "integer"
                                                },
                                                {
                                                    "type": "string"
                                                }
                                                ],
                                            },
                                            "type": "object"
                                            },
                                            "type": {
                                            "type": "string"
                                            }
                                        },
                                        "required": [
                                            "type"
                                        ],
                                        "type": "object"
                                        },
                                        "type": "array"
                                    }
                                    },
                                    "type": "object"
                                },





                  }
                }

    return render_template('projectset_page.html',
                           jsonschema=jsonschema,
                           projectset_list=projectset_list)


@projectset_page.route('/create', methods=['GET', 'POST'])
@jwt_required(True)
def create():

    if request.method == 'POST':

        data = request.form.get('data')

        log.debug("create: data: %s", data)

        try:
            create_projectset(data)

        except Exception as e:
            return {"error": str(e)}
        # pass
        return {"status": "ok"}

    return render_template('modal_form_page.html')


@projectset_page.route('/edit', methods=['GET', 'POST'])
@jwt_required(True)
def edit():

    if request.method == 'POST':

        data = request.form.get('data')

        log.debug("create: data: %s", data)

        try:
            pass
        except Exception as e:
            return {"error": str(e)}
        # pass
        return {"status": "ok"}

    return render_template('modal_form_page.html')


@projectset_page.route('/delete', methods=['GET', 'POST'])
@jwt_required(True)
def delete():
    pass
