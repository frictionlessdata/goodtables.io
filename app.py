from flask import Flask
from goodtablesio.plugins.http.blueprint import api
from goodtablesio.plugins.github.blueprint import github

app = Flask(__name__)

# TODO: automate
app.register_blueprint(api)
app.register_blueprint(github)
