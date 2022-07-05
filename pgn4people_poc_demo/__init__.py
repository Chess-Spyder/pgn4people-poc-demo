import logging

from flask import Flask
from flask import render_template

from . constants import (LOGGING_LEVEL,
                         LOG_FILE_NAME,
                         LOGGING_FORMAT)
from . import traverse


from . __version__ import __version__


logging.basicConfig(level=LOGGING_LEVEL, filename=LOG_FILE_NAME, format=LOGGING_FORMAT)

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Establishes a secret key
    # See https://stackoverflow.com/a/30873279/8401379, https://stackoverflow.com/a/54433731/8401379
    # default value during development
    app.secret_key = 'C2tfLpxDtNdnpMdmcTdHwS2OKtc'
    # overridden if this file exists in the instance folder
    app.config.from_pyfile('config.py', silent=True)

    @app.route("/")
    def index():
        # Index has no independent function; it returns the tree-traversal, reset to 0.
        return traverse.promote_node_to_main_line(0)
    
    @app.route("/about")
    def about():
        # Index has no independent function; it returns the tree-traversal, reset to 0.
        return render_template("/about.html")

   
    app.register_blueprint(traverse.blueprint)

    return app
