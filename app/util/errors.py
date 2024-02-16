import logging as log
from flask import jsonify


def handle_internal_error(e):
    log.error(e)
    return jsonify({"error": str(e.original_exception)}), 500
