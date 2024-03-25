import logging as log
from flask import Blueprint, render_template, request, jsonify
from app.util.auth import jwt_required
from app.crds.chat import (
    chat_call, )

import json
from flask_jwt_extended import get_jwt_identity

chat_page = Blueprint('chat_page', __name__)


@chat_page.route('/', methods=['GET'])
@jwt_required(True)
def chat():

    log.debug("start chat page..")
    return render_template('chat_page.html')


@chat_page.route('/data', methods=['POST'])
@jwt_required(True)
def get_data():

    log.info("get chat message, request: %s, data: %s", request, request.data)

    data = json.loads(request.data)

    user_input = data.get('data')

    login = get_jwt_identity()

    log.info("login: %s, user_input: %s", login, user_input)

    try:

        output = chat_call(login, user_input)

        return jsonify({"response": True, "message": output}), 200

    except Exception as e:
        log.error(e)
        return jsonify({"message": f'Error: {str(e)}', "response": False}), 200
