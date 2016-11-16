from flask import Flask
from .blueprints import api
from .plugins.github.blueprint import github
from . import config


# Module API

# Create instance
app = Flask(__name__)

# Register blueprints
app.register_blueprint(api)
app.register_blueprint(github)
