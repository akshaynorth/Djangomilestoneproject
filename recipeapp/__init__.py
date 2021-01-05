import logging
from flask import Flask


def create_app():
    app = Flask(__name__)

    from . import recipeapp
    app.register_blueprint(recipeapp.bp)

    logging.basicConfig(level=logging.DEBUG)

    return app
