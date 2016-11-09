from flask import Flask
from goodtablesio.blueprints.api import api

app = Flask(__name__)
app.register_blueprint(api)
