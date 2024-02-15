from flask import jsonify
import logging as log


def handle_internal_error(e):
    log.error(e)
    return jsonify({"error": str(e.original_exception)}), 500
