import logging as log
from flask import Blueprint, render_template, request, jsonify
from app.util.auth import jwt_required
import json

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

    text = data.get('data')
    user_input = text

    log.debug("user_input: %s", user_input)

    try:

        # conversation = ConversationChain(llm=llm,memory=memory)
        # output = conversation.predict(input=user_input)

        # memory.save_context({"input": user_input}, {"output": output})

        output = "response.."

        return jsonify({"response": True, "message": output}), 200

    except Exception as e:
        log.error(e)
        return jsonify({"message": f'Error: {str(e)}', "response": False}), 200
