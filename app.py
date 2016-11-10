from flask import Flask
from goodtablesio.blueprints.api import api

from goodtablesio.blueprints.github import github

app = Flask(__name__)

app.register_blueprint(api)
app.register_blueprint(github)
