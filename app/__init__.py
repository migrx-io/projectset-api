from gevent import monkey

monkey.patch_all()

from flask import Flask
from flask_jwt_extended import JWTManager

from flasgger import Swagger

from app.api.auth import auth
from app.api.cluster import clstr

from app.util.errors import handle_internal_error

import logging as log
import sys

from app.util.pool import Pool
from app.util.workers import run_worker

import os


app = Flask(__name__)

log.basicConfig(
    stream=sys.stdout,
    level=os.environ.get("LOGLEVEL", "INFO"),
    format='[%(asctime)s] [%(threadName)s] %(levelname)s - %(message)s',
)

app.config['JWT_SECRET_KEY'] = os.environ["JWT_SECRET_KEY"]
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = os.environ["JWT_EXP"]
app.config['JWT_HEADER_TYPE'] = os.environ["JWT_HEADER"]

swag_conf = {
    "swagger": "2.0",
    "info": {
        "title": "ProjectSet API",
        "description": "API for ProjectSet Project",
        "contact": {
            "responsibleOrganization": "migrx.io",
            "email": "support@migrx.io",
        },
        "version": "1.0.0"
    },
    "schemes": ["http", "https"],
    "securityDefinitions": {
        "JWT": {
            "type":
            "apiKey",
            "name":
            "Authorization",
            "in":
            "header",
            "description":
            "JWT Authorization header. Example: \"Authorization: JWT {token}\""
        }
    },
    "security": [{
        "JWT": []
    }]
}

swag_config = {
    "headers": [],
    "specs": [{
        "endpoint": "apispec_1",
        "route": "/api/v1/apidocs/apispec_1.json",
        "rule_filter": lambda rule: True,  # all in
        "model_filter": lambda tag: True,  # all in
    }],
    "static_url_path":
    "/flasgger_static",
    "swagger_ui":
    True,
    "specs_route":
    "/api/v1/apidocs"
}

Swagger(app, template=swag_conf, config=swag_config)

with app.app_context():

    jwt = JWTManager(app)
    # db = DB()

    # Gateway worker
    # q = queue.Queue()
    pool = Pool(int(os.environ["PWORKERS"]), run_worker, {})
    pool.start()

# Register blueprint(s)

# Auth
app.register_blueprint(auth, url_prefix='/api/v1/')

# Cluster
app.register_blueprint(clstr, url_prefix='/api/v1/')

# Common errors
app.register_error_handler(500, handle_internal_error)
