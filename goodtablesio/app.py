from flask import Flask
from .blueprints.api import api
from .blueprints.github import github
from . import config


# Module API

def create_app():

    # Create instance
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(api)
    app.register_blueprint(github)

    return app


# Main program

if __name__ == '__main__':
    app = create_app()
    app.run(port=config.APP_PORT)
