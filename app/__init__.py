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

from app.api.auth import auth
from app.api.cluster import clstr

from app.util.errors import handle_internal_error

from app.webapp.repos import repoz

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

# Auth
app.register_blueprint(auth, url_prefix='/api/v1/')

# Cluster
app.register_blueprint(clstr, url_prefix='/api/v1/')

# Webapp
app.register_blueprint(repoz, url_prefix='/')
# app.register_blueprint(ps_page, url_prefix='/ps')
# app.register_blueprint(pst_page, url_prefix='/pst')

# Common errors
app.register_error_handler(500, handle_internal_error)
