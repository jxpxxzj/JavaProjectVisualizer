import os
import sys
import logging

from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from Server.Api import apiBp
from Utils.NodeEncoder import NodeEncoder

def CreateApp():
    project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if project_path not in sys.path:
        sys.path.insert(0, project_path)

    app = Flask(__name__)

    @app.route('/<path:path>')
    def static_file(path):
        return app.send_static_file(path)

    app.debug = False
    app.json_encoder = NodeEncoder

    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.logger.addHandler(logging.StreamHandler()) 
    app.logger.setLevel(logging.ERROR)

    def registerBlueprint(app):
        app.register_blueprint(apiBp)

    registerBlueprint(app)
    return app
