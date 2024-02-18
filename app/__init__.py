from gevent import monkey

monkey.patch_all()

import logging as log
import sys
import os
import random
import string

from flask import Flask
from flask_jwt_extended import JWTManager

from flasgger import Swagger

from app.util.errors import handle_internal_error

from app.api.auth_api import auth_api
from app.api.projectset_api import projectset_api

from app.webapp.login_page import login_page
from app.webapp.repo_page import repo_page
from app.webapp.projectset_page import projectset_page

from app.util.pool import Pool
from app.util.workers import run_worker

app = Flask(
    __name__,
    template_folder="webapp/html/templates",
    static_folder="webapp/html/static",
)

log.basicConfig(
    stream=sys.stdout,
    level=os.environ.get("LOGLEVEL", "INFO"),
    format='[%(asctime)s] [%(threadName)s] %(levelname)s - %(message)s',
)

app.config['JWT_SECRET_KEY'] = "".join(
    random.choices(string.ascii_lowercase + string.digits, k=20))
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(
    os.environ.get("JWT_EXP", "31536000"))
app.config['JWT_HEADER_TYPE'] = os.environ.get("JWT_HEADER", "JWT")

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
    pool = Pool(int(os.environ.get("PWORKERS", "1")), run_worker, {})
    pool.start()

# Register blueprint(s)

# API

app.register_blueprint(auth_api, url_prefix='/api/v1/')
app.register_blueprint(projectset_api, url_prefix='/api/v1/')

# Webapp
app.register_blueprint(login_page, url_prefix='/')
app.register_blueprint(repo_page, url_prefix='/repo')
app.register_blueprint(projectset_page, url_prefix='/projectset')

# Common errors
app.register_error_handler(500, handle_internal_error)
