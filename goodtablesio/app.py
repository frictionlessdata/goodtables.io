from flask import Flask
from .blueprints.api import api
from .blueprints.site import site
from .plugins.github.blueprint import github


# Module API

# Create instance
app = Flask(__name__)

# Register blueprints
app.register_blueprint(api)
app.register_blueprint(site)

# Register plugins
app.register_blueprint(github)
